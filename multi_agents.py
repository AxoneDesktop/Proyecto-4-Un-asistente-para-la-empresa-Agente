"""
Sistema Multi-Agente para el restaurante
Define agentes especializados y el orquestador que los coordina
"""
import os
import google.generativeai as genai
from typing import Dict, Any, List, Optional
from agent_runner import AgentRunner, MultiAgentRunner, AgentType
from mcp_tools import TOOLS_DEFINITIONS
import logging

logger = logging.getLogger(__name__)

# Configuración de modelos
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# ============= PROMPTS DE AGENTES ESPECIALIZADOS =============

RESERVAS_AGENT_PROMPT = """Eres el **Agente de Reservas** del restaurante, especializado en:

**TU RESPONSABILIDAD**:
1. Crear nuevas reservas
2. Modificar fechas de reservas existentes
3. Cancelar reservas
4. Consultar estado de reservas

**IMPORTANTE AL CREAR RESERVAS**:
- DEBES obtener TODOS los datos antes de usar la herramienta:
  * Nombre completo
  * Teléfono (9-15 dígitos)
  * Email válido
  * Fecha y hora (formato YYYY-MM-DDTHH:mm)
  * Número de personas (1-20)
- El horario del restaurante es 9:00 AM - 11:00 PM
- Pregunta amablemente si falta algún dato

**FORMATO DE FECHAS**:
- Convierte lenguaje natural a formato YYYY-MM-DDTHH:mm
- Ejemplo: "mañana a las 8 PM" → "2025-11-25T20:00"

**TOKENS**:
- Al crear una reserva, el sistema devuelve un token único
- Explica que deben guardarlo para modificar/cancelar/consultar
- El token también se envía por email

**HERRAMIENTAS DISPONIBLES**:
- crear_reserva: Crea una nueva reserva (requiere todos los datos)
- modificar_fecha_reserva: Cambia la fecha de una reserva (requiere token)
- cancelar_reserva: Cancela una reserva (requiere token)
- consultar_reserva: Verifica estado de una reserva (requiere token)

Sé amable, confirma datos antes de ejecutar acciones, y maneja errores con empatía.
"""

MENUS_AGENT_PROMPT = """Eres el **Agente de Menús** del restaurante, especializado en:

**TU RESPONSABILIDAD**:
1. Proporcionar información sobre menús disponibles
2. Recomendar el menú más valorado
3. Describir platos y precios
4. Responder consultas sobre disponibilidad de menús

**HERRAMIENTAS DISPONIBLES**:
- get_menu_mas_valorado: Obtiene el menú con mejor valoración
- listar_menus_disponibles: Lista todos los menús disponibles

**ESTILO**:
- Describe los menús de manera apetitosa y atractiva
- Menciona valoraciones cuando sea relevante
- Ayuda a los clientes a elegir según sus preferencias
- Si preguntan por reservas, indica que otro agente puede ayudarlos

Sé entusiasta y conocedor de la oferta gastronómica.
"""

INFO_AGENT_PROMPT = """Eres el **Agente de Información General** del restaurante, especializado en:

**TU RESPONSABILIDAD**:
1. Información sobre horarios: 9:00 AM - 11:00 PM todos los días
2. Ubicación y cómo llegar
3. Ambiente y servicios del restaurante
4. Políticas generales
5. Preguntas frecuentes

**INFORMACIÓN DEL RESTAURANTE**:
- Horario: 9:00 AM - 11:00 PM
- Ambiente: Acogedor y familiar
- Especialidad: Cocina variada con menús valorados por clientes
- Servicios: Reservas en línea, consulta de menús, atención personalizada

**ESTILO**:
- Amable y acogedor
- Proporciona información clara y precisa
- Si preguntan sobre reservas o menús específicos, sugiere que otro agente puede ayudarlos mejor

Sé cálido y hospitalario, representa bien la imagen del restaurante.
"""

ORCHESTRATOR_PROMPT = """Eres el **Orquestador Principal** del sistema multi-agente del restaurante.

**TU RESPONSABILIDAD**:
Analizar cada consulta del usuario y determinar qué agente(s) debe(n) responder:

**AGENTES DISPONIBLES**:
1. **reservas_agent**: Maneja todo lo relacionado con reservas (crear, modificar, cancelar, consultar)
2. **menus_agent**: Información sobre menús, platos, precios, recomendaciones
3. **info_agent**: Información general (horarios, ubicación, ambiente, políticas)

**REGLAS DE ROUTING**:
- Si mencionan "reserva", "reservar", "modificar reserva", "cancelar", "token" → reservas_agent
- Si mencionan "menú", "platos", "comida", "precio", "recomendación" → menus_agent
- Si mencionan "horario", "ubicación", "cómo llegar", "información general" → info_agent
- Si la consulta es ambigua o general → info_agent (da bienvenida y explica servicios)
- Puedes invocar múltiples agentes si la consulta requiere información de varios

**RESPUESTA**:
Debes responder SIEMPRE en formato JSON con esta estructura:
```json
{
  "agents": ["agent_id1", "agent_id2"],
  "reasoning": "Breve explicación de por qué elegiste estos agentes"
}
```

**EJEMPLOS**:
Usuario: "Quiero hacer una reserva para mañana"
→ {"agents": ["reservas_agent"], "reasoning": "Consulta sobre crear una reserva"}

Usuario: "¿Qué menú recomiendan y cuál es el horario?"
→ {"agents": ["menus_agent", "info_agent"], "reasoning": "Necesita info de menús y horarios"}

Usuario: "Hola"
→ {"agents": ["info_agent"], "reasoning": "Saludo inicial, dar bienvenida general"}

Sé preciso en tu análisis y routing de consultas.
"""

# ============= FACTORY DE AGENTES =============

class AgentFactory:
    """Factory para crear agentes especializados"""
    
    @staticmethod
    def create_reservas_agent(agent_id: str = "reservas_agent") -> AgentRunner:
        """Crea el agente de reservas"""
        # Tools relacionadas con reservas
        reservas_tools = [
            tool for tool in TOOLS_DEFINITIONS
            if tool['name'] in ['crear_reserva', 'modificar_fecha_reserva', 'cancelar_reserva', 'consultar_reserva']
        ]
        
        tools_for_gemini = []
        for tool_def in reservas_tools:
            func_declaration = {
                "name": tool_def["name"],
                "description": tool_def["description"]
            }
            if tool_def.get("parameters"):
                func_declaration["parameters"] = tool_def["parameters"]
            tools_for_gemini.append(func_declaration)
        
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
            system_instruction=RESERVAS_AGENT_PROMPT,
            tools=[{"function_declarations": tools_for_gemini}]
        )
        
        return AgentRunner(agent_id, AgentType.RESERVAS, model, reservas_tools)
    
    @staticmethod
    def create_menus_agent(agent_id: str = "menus_agent") -> AgentRunner:
        """Crea el agente de menús"""
        # Tools relacionadas con menús
        menus_tools = [
            tool for tool in TOOLS_DEFINITIONS
            if tool['name'] in ['get_menu_mas_valorado', 'listar_menus_disponibles']
        ]
        
        tools_for_gemini = []
        for tool_def in menus_tools:
            func_declaration = {
                "name": tool_def["name"],
                "description": tool_def["description"]
            }
            if tool_def.get("parameters"):
                func_declaration["parameters"] = tool_def["parameters"]
            tools_for_gemini.append(func_declaration)
        
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
            system_instruction=MENUS_AGENT_PROMPT,
            tools=[{"function_declarations": tools_for_gemini}]
        )
        
        return AgentRunner(agent_id, AgentType.MENUS, model, menus_tools)
    
    @staticmethod
    def create_info_agent(agent_id: str = "info_agent") -> AgentRunner:
        """Crea el agente de información general"""
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS,
            system_instruction=INFO_AGENT_PROMPT,
            tools=[]  # No necesita tools, solo información
        )
        
        return AgentRunner(agent_id, AgentType.INFO, model, [])
    
    @staticmethod
    def create_orchestrator(agent_id: str = "orchestrator") -> AgentRunner:
        """Crea el agente orquestador"""
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config={
                "temperature": 0.3,  # Más determinístico para routing
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 512,
            },
            safety_settings=SAFETY_SETTINGS,
            system_instruction=ORCHESTRATOR_PROMPT,
            tools=[]
        )
        
        return AgentRunner(agent_id, AgentType.ORCHESTRATOR, model, [])

# ============= SISTEMA MULTI-AGENTE =============

class RestauranteMultiAgentSystem:
    """Sistema completo multi-agente para el restaurante"""
    
    def __init__(self):
        self.runner = MultiAgentRunner()
        self._initialize_agents()
        logger.info("🎯 Sistema Multi-Agente del Restaurante inicializado")
    
    def _initialize_agents(self):
        """Inicializa todos los agentes del sistema"""
        # Crear agentes especializados
        reservas_agent = AgentFactory.create_reservas_agent()
        menus_agent = AgentFactory.create_menus_agent()
        info_agent = AgentFactory.create_info_agent()
        orchestrator = AgentFactory.create_orchestrator()
        
        # Registrar agentes
        self.runner.register_agent(reservas_agent)
        self.runner.register_agent(menus_agent)
        self.runner.register_agent(info_agent)
        self.runner.register_agent(orchestrator)
        
        logger.info("✅ Todos los agentes inicializados y registrados")
    
    async def process_message(
        self,
        user_message: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Procesa un mensaje del usuario usando el sistema multi-agente
        
        Args:
            user_message: Mensaje del usuario
            session_id: ID de sesión opcional
            
        Returns:
            Respuesta coordinada del sistema
        """
        try:
            # 1. Usar el orquestador para determinar qué agente(s) usar
            orchestrator_result = await self.runner.execute_agent(
                "orchestrator",
                f"Analiza esta consulta y determina qué agente(s) deben responder:\n\n{user_message}"
            )
            
            if not orchestrator_result.get("success"):
                # Fallback: usar info_agent si el orquestador falla
                logger.warning("⚠️ Orquestador falló, usando info_agent como fallback")
                selected_agents = ["info_agent"]
                reasoning = "Fallback a agente de información general"
            else:
                # Parsear respuesta del orquestador
                import json
                import re
                
                orchestrator_response = orchestrator_result.get("response", "")
                
                # Extraer JSON de la respuesta
                json_match = re.search(r'\{[^}]+\}', orchestrator_response)
                if json_match:
                    routing_decision = json.loads(json_match.group())
                    selected_agents = routing_decision.get("agents", ["info_agent"])
                    reasoning = routing_decision.get("reasoning", "")
                else:
                    selected_agents = ["info_agent"]
                    reasoning = "No se pudo parsear decisión del orquestador"
                
                logger.info(f"🎯 Orquestador eligió: {selected_agents} - {reasoning}")
            
            # 2. Ejecutar los agentes seleccionados
            if len(selected_agents) == 1:
                # Ejecutar un solo agente
                result = await self.runner.execute_agent(
                    selected_agents[0],
                    user_message
                )
                
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "agents_used": selected_agents,
                    "routing_reasoning": reasoning,
                    "session_id": session_id
                }
            else:
                # Ejecutar múltiples agentes en paralelo
                tasks = [
                    {"agent_id": agent_id, "message": user_message}
                    for agent_id in selected_agents
                ]
                
                results = await self.runner.execute_parallel(tasks)
                
                # Combinar respuestas
                combined_response = self._combine_responses(results, selected_agents)
                
                return {
                    "success": True,
                    "response": combined_response,
                    "agents_used": selected_agents,
                    "routing_reasoning": reasoning,
                    "session_id": session_id
                }
        
        except Exception as e:
            logger.error(f"❌ Error en sistema multi-agente: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }
    
    def _combine_responses(
        self,
        results: List[Dict[str, Any]],
        agent_ids: List[str]
    ) -> str:
        """Combina respuestas de múltiples agentes"""
        combined = []
        
        for i, result in enumerate(results):
            if isinstance(result, dict) and result.get("success"):
                agent_name = agent_ids[i].replace("_agent", "").title()
                response = result.get("response", "")
                combined.append(f"**{agent_name}**: {response}")
        
        if not combined:
            return "Lo siento, no pude procesar tu consulta en este momento."
        
        return "\n\n".join(combined)
    
    def reset_session(self, session_id: Optional[str] = None):
        """Reinicia una sesión (todos los agentes)"""
        self.runner.reset_all()
        logger.info(f"🔄 Sesión reiniciada: {session_id}")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado del sistema"""
        return self.runner.get_system_status()
