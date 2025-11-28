"""
Test simple para verificar la conexión con Google Gemini
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Cargar variables de entorno
load_dotenv()

def test_gemini_connection():
    """Prueba la conexión con Google Gemini"""
    
    print("🔍 Verificando configuración...")
    
    # Obtener API Key
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY no está configurada en el archivo .env")
        return False
    
    print(f"✅ API Key encontrada: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        # Configurar Gemini
        genai.configure(api_key=api_key)
        print("✅ API Key configurada correctamente")
        
        # Listar modelos disponibles
        print("\n📋 Listando modelos disponibles...")
        models = genai.list_models()
        available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            print("❌ No hay modelos disponibles con tu API Key")
            return False
        
        print(f"✅ Modelos disponibles: {len(available_models)}")
        
        # Buscar modelo flash (más disponible)
        flash_models = [m for m in available_models if 'flash' in m.lower()]
        if flash_models:
            model_to_use = flash_models[0].replace('models/', '')
            print(f"   ✓ Usando modelo Flash: {model_to_use}")
        else:
            model_to_use = available_models[0].replace('models/', '')
            print(f"   ✓ Usando primer modelo disponible: {model_to_use}")
        
        for i, model_name in enumerate(available_models[:5], 1):
            marker = "👉" if model_name.replace('models/', '') == model_to_use else "  "
            print(f"   {marker} {i}. {model_name}")
        
        print(f"\n🤖 Creando modelo: {model_to_use}")
        model = genai.GenerativeModel(model_to_use)
        print("✅ Modelo creado exitosamente")
        
        # Hacer una prueba simple
        print("\n💬 Enviando mensaje de prueba...")
        response = model.generate_content("Di 'Hola' en una sola palabra")
        
        print("✅ Respuesta recibida:")
        print(f"   {response.text}")
        
        # Prueba con el prompt del restaurante
        print("\n🍽️ Probando con contexto del restaurante...")
        chat = model.start_chat(history=[])
        
        message = """Eres un asistente del restaurante. Responde brevemente: 
        ¿Cuál es el horario del restaurante? (El horario es 9:00 AM - 11:00 PM)"""
        
        response = chat.send_message(message)
        print("✅ Respuesta del agente:")
        print(f"   {response.text}")
        
        print("\n✅✅✅ ¡Conexión con Gemini funcionando perfectamente! ✅✅✅")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR al conectar con Gemini:")
        print(f"   {str(e)}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que tu API Key sea correcta")
        print("   2. Asegúrate de tener acceso a Gemini API")
        print("   3. Revisa tu conexión a internet")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TEST DE CONEXIÓN CON GOOGLE GEMINI")
    print("=" * 60)
    print()
    
    success = test_gemini_connection()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ PRUEBA EXITOSA - El agente está listo para usar")
    else:
        print("❌ PRUEBA FALLIDA - Revisa la configuración")
    print("=" * 60)
