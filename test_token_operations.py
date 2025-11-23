"""
Test rápido de cancelar y modificar reserva con token
"""
import asyncio
from mcp_tools import restaurante_tools

async def test_operations():
    """Prueba las operaciones con el token real"""
    
    token = "72FF07E74B9E051A5704EBE96DA4095F"
    
    print("=" * 60)
    print("🧪 TEST DE OPERACIONES CON TOKEN")
    print("=" * 60)
    
    # 1. Consultar reserva
    print(f"\n1. Consultando reserva con token: {token}")
    result = await restaurante_tools.consultar_reserva(token)
    print(f"   Resultado: {result}")
    
    if result.get("success"):
        reserva = result.get("reserva")
        print(f"   Estado actual: {reserva.get('estado')}")
        print(f"   Fecha actual: {reserva.get('fecha_reserva')}")
        print(f"   Cliente: {reserva.get('nombre_cliente')}")
    
    # 2. Modificar fecha (prueba)
    print(f"\n2. Intentando modificar fecha...")
    nueva_fecha = "2025-11-25T19:00"
    result = await restaurante_tools.modificar_fecha_reserva(token, nueva_fecha)
    print(f"   Resultado: {result}")
    
    # 3. Consultar de nuevo para ver cambios
    if result.get("success"):
        print(f"\n3. Verificando cambio...")
        result = await restaurante_tools.consultar_reserva(token)
        if result.get("success"):
            reserva = result.get("reserva")
            print(f"   Nueva fecha: {reserva.get('fecha_reserva')}")
    
    # NOTA: Comentado para no cancelar la reserva real
    # print(f"\n4. Cancelando reserva...")
    # result = await restaurante_tools.cancelar_reserva(token)
    # print(f"   Resultado: {result}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_operations())
