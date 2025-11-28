"""
Agent Runner - Sistema base para ejecutar agentes IA
Proporciona la infraestructura para manejar múltiples agentes especializados
"""
import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import google.generativeai as genai

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Estados posibles de un agente"""
    IDLE = "idle"
    RUNNING = "running"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"

class AgentType(Enum):
    """Tipos de agentes disponibles"""
    RESERVAS = "reservas"
    MENUS = "menus"
    INFO = "info"
    ORCHESTRATOR = "orchestrator"

class AgentRunner:
    """
    Clase base para ejecutar agentes IA
    Maneja el ciclo de vida, estado y ejecución de un agente
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_type: AgentType,
        model: genai.GenerativeModel,
        tools: Optional[List[Dict]] = None
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.model = model
        self.tools = tools or []
        self.status = AgentStatus.IDLE
        self.chat_history = []
        self.execution_count = 0
        self.created_at = datetime.now()
        self.last_execution = None
        
        logger.info(f"✨ Agent {agent_id} ({agent_type.value}) inicializado")
    
    async def execute(
        self,
        user_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta el agente con un mensaje de usuario
        
        Args:
            user_message: Mensaje del usuario
            context: Contexto adicional para el agente
            
        Returns:
            Respuesta del agente con metadata
        """
        self.status = AgentStatus.RUNNING
        self.execution_count += 1
        self.last_execution = datetime.now()
        
        try:
            logger.info(f"🏃 Agent {self.agent_id} ejecutando mensaje #{self.execution_count}")
            
            # Crear o continuar chat
            if not hasattr(self, 'chat'):
                self.chat = self.model.start_chat(
                    history=self.chat_history,
                    enable_automatic_function_calling=True
                )
            
            # Agregar contexto si existe
            if context:
                user_message = self._add_context_to_message(user_message, context)
            
            # Enviar mensaje
            response = self.chat.send_message(user_message)
            
            # Manejar llamadas a funciones
            response = await self._handle_function_calls(response)
            
            # Guardar en historial
            self.chat_history.append({
                "role": "user",
                "parts": [user_message]
            })
            self.chat_history.append({
                "role": "model",
                "parts": [response.text]
            })
            
            self.status = AgentStatus.COMPLETED
            
            result = {
                "success": True,
                "agent_id": self.agent_id,
                "agent_type": self.agent_type.value,
                "response": response.text,
                "execution_count": self.execution_count,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info(f"✅ Agent {self.agent_id} completó ejecución #{self.execution_count}")
            return result
            
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"❌ Error en agent {self.agent_id}: {str(e)}")
            
            return {
                "success": False,
                "agent_id": self.agent_id,
                "agent_type": self.agent_type.value,
                "error": str(e),
                "execution_count": self.execution_count,
                "timestamp": datetime.now().isoformat()
            }
    
    async def _handle_function_calls(self, response) -> Any:
        """Maneja llamadas a funciones del agente"""
        # Importar tools aquí para evitar circular import
        from mcp_tools import restaurante_tools
        
        while response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = dict(function_call.args)
            
            logger.info(f"🔧 Agent {self.agent_id} llamando función: {function_name}")
            
            # Ejecutar la función
            if hasattr(restaurante_tools, function_name):
                func = getattr(restaurante_tools, function_name)
                function_response = await func(**function_args)
            else:
                function_response = {"error": f"Función {function_name} no encontrada"}
            
            # Enviar resultado al modelo
            response = self.chat.send_message(
                genai.protos.Content(
                    parts=[genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"result": function_response}
                        )
                    )]
                )
            )
        
        return response
    
    def _add_context_to_message(self, message: str, context: Dict[str, Any]) -> str:
        """Agrega contexto al mensaje del usuario"""
        context_str = "\n".join([f"{k}: {v}" for k, v in context.items()])
        return f"[Contexto: {context_str}]\n\n{message}"
    
    def reset(self):
        """Reinicia el estado del agente"""
        self.chat_history = []
        self.status = AgentStatus.IDLE
        if hasattr(self, 'chat'):
            delattr(self, 'chat')
        logger.info(f"🔄 Agent {self.agent_id} reiniciado")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del agente"""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "status": self.status.value,
            "execution_count": self.execution_count,
            "created_at": self.created_at.isoformat(),
            "last_execution": self.last_execution.isoformat() if self.last_execution else None,
            "history_length": len(self.chat_history)
        }

class MultiAgentRunner:
    """
    Gestor de múltiples agentes
    Coordina la ejecución de varios agentes especializados
    """
    
    def __init__(self):
        self.agents: Dict[str, AgentRunner] = {}
        self.execution_queue = asyncio.Queue()
        logger.info("🚀 MultiAgentRunner inicializado")
    
    def register_agent(self, agent: AgentRunner):
        """Registra un nuevo agente en el sistema"""
        self.agents[agent.agent_id] = agent
        logger.info(f"📝 Agent {agent.agent_id} registrado")
    
    def get_agent(self, agent_id: str) -> Optional[AgentRunner]:
        """Obtiene un agente por su ID"""
        return self.agents.get(agent_id)
    
    def get_agents_by_type(self, agent_type: AgentType) -> List[AgentRunner]:
        """Obtiene todos los agentes de un tipo específico"""
        return [
            agent for agent in self.agents.values()
            if agent.agent_type == agent_type
        ]
    
    async def execute_agent(
        self,
        agent_id: str,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Ejecuta un agente específico"""
        agent = self.get_agent(agent_id)
        if not agent:
            return {
                "success": False,
                "error": f"Agente {agent_id} no encontrado"
            }
        
        return await agent.execute(message, context)
    
    async def execute_parallel(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Ejecuta múltiples agentes en paralelo
        
        Args:
            tasks: Lista de diccionarios con {agent_id, message, context}
        """
        logger.info(f"⚡ Ejecutando {len(tasks)} agentes en paralelo")
        
        async_tasks = [
            self.execute_agent(
                task['agent_id'],
                task['message'],
                task.get('context')
            )
            for task in tasks
        ]
        
        results = await asyncio.gather(*async_tasks, return_exceptions=True)
        return results
    
    def reset_agent(self, agent_id: str):
        """Reinicia un agente específico"""
        agent = self.get_agent(agent_id)
        if agent:
            agent.reset()
    
    def reset_all(self):
        """Reinicia todos los agentes"""
        for agent in self.agents.values():
            agent.reset()
        logger.info("🔄 Todos los agentes reiniciados")
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado de todo el sistema multiagente"""
        return {
            "total_agents": len(self.agents),
            "agents": {
                agent_id: agent.get_status()
                for agent_id, agent in self.agents.items()
            },
            "timestamp": datetime.now().isoformat()
        }
