"""
Script de prueba para el sistema multi-agente
Prueba diferentes consultas y verifica el routing de agentes
"""
import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai
from multi_agents import RestauranteMultiAgentSystem

# Cargar variables de entorno
load_dotenv()

# Configurar Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no configurada")

genai.configure(api_key=GEMINI_API_KEY)

async def test_multiagent_system():
    """Prueba el sistema multi-agente con diferentes consultas"""
    
    print("=" * 70)
    print("🧪 PRUEBA DEL SISTEMA MULTI-AGENTE")
    print("=" * 70)
    
    # Inicializar sistema
    system = RestauranteMultiAgentSystem()
    
    # Consultas de prueba
    test_queries = [
        {
            "query": "Hola, buenos días",
            "expected_agent": "info_agent",
            "description": "Saludo inicial"
        },
        {
            "query": "¿Cuál es el horario del restaurante?",
            "expected_agent": "info_agent",
            "description": "Consulta de información general"
        },
        {
            "query": "¿Qué menú me recomiendas?",
            "expected_agent": "menus_agent",
            "description": "Consulta sobre menús"
        },
        {
            "query": "Quiero hacer una reserva para mañana",
            "expected_agent": "reservas_agent",
            "description": "Solicitud de reserva"
        },
        {
            "query": "¿Cuál es el menú más valorado y cuál es el horario?",
            "expected_agent": ["menus_agent", "info_agent"],
            "description": "Consulta múltiple (requiere 2 agentes)"
        },
        {
            "query": "Necesito cancelar mi reserva con token ABC123",
            "expected_agent": "reservas_agent",
            "description": "Cancelación de reserva"
        }
    ]
    
    # Ejecutar pruebas
    for i, test in enumerate(test_queries, 1):
        print(f"\n{'='*70}")
        print(f"📝 PRUEBA {i}: {test['description']}")
        print(f"{'='*70}")
        print(f"👤 Usuario: {test['query']}")
        print(f"🎯 Agente(s) esperado(s): {test['expected_agent']}")
        print(f"\n⏳ Procesando...")
        
        try:
            # Procesar mensaje
            result = await system.process_message(test['query'])
            
            if result.get("success"):
                agents_used = result.get("agents_used", [])
                response = result.get("response", "")
                reasoning = result.get("routing_reasoning", "")
                
                print(f"\n✅ Respuesta exitosa")
                print(f"🤖 Agentes utilizados: {agents_used}")
                print(f"💭 Razonamiento: {reasoning}")
                print(f"\n📨 RESPUESTA:")
                print("-" * 70)
                print(response)
                print("-" * 70)
                
                # Verificar si el routing fue correcto
                if isinstance(test['expected_agent'], list):
                    correct = set(test['expected_agent']) == set(agents_used)
                else:
                    correct = test['expected_agent'] in agents_used
                
                status = "✅ CORRECTO" if correct else "⚠️ DIFERENTE AL ESPERADO"
                print(f"\n{status}")
            else:
                print(f"\n❌ Error: {result.get('error')}")
        
        except Exception as e:
            print(f"\n❌ Excepción: {str(e)}")
        
        # Pausa entre pruebas
        await asyncio.sleep(1)
    
    # Estado final del sistema
    print(f"\n{'='*70}")
    print("📊 ESTADO FINAL DEL SISTEMA")
    print(f"{'='*70}")
    
    status = system.get_system_status()
    print(f"\n📈 Total de agentes: {status['total_agents']}")
    
    for agent_id, agent_status in status['agents'].items():
        print(f"\n🤖 {agent_id}:")
        print(f"   - Tipo: {agent_status['agent_type']}")
        print(f"   - Estado: {agent_status['status']}")
        print(f"   - Ejecuciones: {agent_status['execution_count']}")
        print(f"   - Historial: {agent_status['history_length']} mensajes")
    
    print(f"\n{'='*70}")
    print("✅ PRUEBAS COMPLETADAS")
    print(f"{'='*70}")

if __name__ == "__main__":
    asyncio.run(test_multiagent_system())
