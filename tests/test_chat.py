"""
Script de prueba para el agente IA
"""
import httpx
import asyncio

BASE_URL = "http://localhost:8000"

async def test_chat():
    """Prueba básica del endpoint de chat"""
    
    messages = [
        {
            "messages": [
                {"role": "user", "content": "Hola, ¿cuál es el horario del restaurante?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Hola, ¿cuál es el horario del restaurante?"},
                {"role": "assistant", "content": "El restaurante está abierto de 9:00 AM a 11:00 PM todos los días."},
                {"role": "user", "content": "¿Y cómo puedo hacer una reserva?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "¿Qué pasa si pierdo mi token de reserva?"}
            ]
        }
    ]
    
    async with httpx.AsyncClient() as client:
        print("🤖 Probando agente IA...\n")
        
        for i, message_data in enumerate(messages, 1):
            print(f"--- Prueba {i} ---")
            user_msg = message_data["messages"][-1]["content"]
            print(f"👤 Usuario: {user_msg}")
            
            try:
                response = await client.post(
                    f"{BASE_URL}/chat",
                    json=message_data,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"🤖 Agente: {data['response']}\n")
                else:
                    print(f"❌ Error {response.status_code}: {response.text}\n")
                    
            except Exception as e:
                print(f"❌ Error: {str(e)}\n")

async def test_health():
    """Verifica que el servicio esté funcionando"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Servicio funcionando correctamente")
                return True
            else:
                print("❌ Servicio no responde correctamente")
                return False
        except Exception as e:
            print(f"❌ No se puede conectar al servicio: {str(e)}")
            return False

async def main():
    print("=== Test del Agente IA ===\n")
    
    # Verificar health
    if await test_health():
        print()
        # Hacer pruebas de chat
        await test_chat()
    else:
        print("\n⚠️ Asegúrate de que el servicio esté corriendo en http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(main())
