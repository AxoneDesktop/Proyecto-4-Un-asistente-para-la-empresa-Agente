"""
Test completo del MCP con tools
"""
import asyncio
import httpx
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

async def test_chat_with_tools():
    """Prueba el chat con diferentes funcionalidades de tools"""
    
    print("🧪 PRUEBAS DEL AGENTE CON MCP TOOLS")
    print("=" * 60)
    
    tests = [
        {
            "nombre": "Consultar menú más valorado",
            "mensaje": "¿Cuál es el menú más valorado del restaurante?"
        },
        {
            "nombre": "Listar menús disponibles",
            "mensaje": "¿Qué menús tenéis disponibles?"
        },
        {
            "nombre": "Crear reserva (recopilar datos)",
            "mensaje": "Quiero hacer una reserva para mañana"
        },
        {
            "nombre": "Consultar horarios",
            "mensaje": "¿A qué hora abrís?"
        }
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i, test in enumerate(tests, 1):
            print(f"\n--- Test {i}: {test['nombre']} ---")
            print(f"👤 Usuario: {test['mensaje']}")
            
            try:
                response = await client.post(
                    f"{BASE_URL}/chat",
                    json={
                        "messages": [
                            {"role": "user", "content": test["mensaje"]}
                        ]
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"🤖 Agente: {data['response']}")
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            # Pequeña pausa entre tests
            await asyncio.sleep(1)

async def test_create_reservation_full():
    """Prueba crear una reserva completa con todos los datos"""
    
    print("\n" + "=" * 60)
    print("🎯 TEST ESPECIAL: Crear Reserva Completa")
    print("=" * 60)
    
    # Calcular fecha de mañana a las 20:00
    tomorrow = datetime.now() + timedelta(days=1)
    fecha_reserva = tomorrow.replace(hour=20, minute=0).strftime("%Y-%m-%dT%H:%M")
    
    messages = [
        {"role": "user", "content": "Quiero hacer una reserva"},
        {"role": "assistant", "content": "¡Perfecto! Para crear tu reserva necesito algunos datos. ¿Cuántas personas seréis?"},
        {"role": "user", "content": "Seremos 4 personas"},
        {"role": "assistant", "content": "Genial, 4 personas. ¿Para qué día y hora te gustaría reservar?"},
        {"role": "user", "content": f"Para mañana a las 8 de la noche"},
        {"role": "assistant", "content": "Perfecto. ¿Cuál es tu nombre completo?"},
        {"role": "user", "content": "Juan Pérez García"},
        {"role": "assistant", "content": "Gracias Juan. ¿Me das tu número de teléfono?"},
        {"role": "user", "content": "666777888"},
        {"role": "assistant", "content": "Perfecto. Por último, ¿cuál es tu email?"},
        {"role": "user", "content": "juan.perez@example.com"}
    ]
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            print("\n📝 Enviando conversación completa para crear reserva...")
            print(f"   Nombre: Juan Pérez García")
            print(f"   Teléfono: 666777888")
            print(f"   Email: juan.perez@example.com")
            print(f"   Fecha: {fecha_reserva}")
            print(f"   Personas: 4")
            
            response = await client.post(
                f"{BASE_URL}/chat",
                json={"messages": messages}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n✅ Respuesta del agente:")
                print(f"   {data['response']}")
            else:
                print(f"\n❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

async def test_menu_mas_valorado_directo():
    """Prueba directa de la tool de menú más valorado"""
    
    print("\n" + "=" * 60)
    print("🔧 TEST DIRECTO: Tool get_menu_mas_valorado")
    print("=" * 60)
    
    from mcp_tools import restaurante_tools
    
    try:
        result = await restaurante_tools.get_menu_mas_valorado()
        print(f"\n✅ Resultado:")
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

async def main():
    print("\n🚀 Iniciando tests del MCP...")
    print()
    
    # Verificar que el servicio está corriendo
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Servicio en línea\n")
            else:
                print("❌ Servicio no responde correctamente")
                return
    except Exception as e:
        print(f"❌ No se puede conectar al servicio: {str(e)}")
        print("   Asegúrate de que el servicio esté corriendo en http://localhost:8000")
        return
    
    # Ejecutar tests
    await test_chat_with_tools()
    await test_menu_mas_valorado_directo()
    # await test_create_reservation_full()  # Comentado para no crear reservas reales
    
    print("\n" + "=" * 60)
    print("✅ TESTS COMPLETADOS")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
