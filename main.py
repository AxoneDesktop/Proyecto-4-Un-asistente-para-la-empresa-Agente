"""
Microservicio de Agente IA para el restaurante
Usa Google Gemini Flash para conversaciones con clientes
Con integración de MCP Tools para ejecutar acciones reales
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import httpx
import json
from mcp_tools import (
    restaurante_tools, 
    TOOLS_DEFINITIONS
)

# Cargar variables de entorno
load_dotenv()

# Configurar Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")

genai.configure(api_key=GEMINI_API_KEY)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Agente IA Restaurante",
    description="Microservicio de agente conversacional con Google Gemini",
    version="1.0.0"
)

# Configurar CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:4200").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL de la API Node.js
NODE_API_URL = os.getenv("NODE_API_URL", "http://localhost:3000/api")

# Configuración del modelo Gemini
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Prompt del sistema para el agente
SYSTEM_PROMPT = """Eres un asistente virtual del restaurante, amable y servicial. Tu función es ayudar a los clientes con:

1. **Información sobre el restaurante**: Horarios (9:00 AM - 11:00 PM), ubicación, ambiente.
2. **Consultar menús**: Puedes usar la herramienta para ver menús disponibles y el más valorado.
3. **Crear reservas**: Puedes crear reservas cuando el cliente te proporcione TODOS los datos.
4. **Modificar reservas**: Puedes cambiar la fecha de una reserva si tienen el token.
5. **Cancelar reservas**: Puedes cancelar reservas con el token.
6. **Consultar reservas**: Puedes verificar el estado de una reserva con el token.

**IMPORTANTE AL CREAR RESERVAS**:
- DEBES obtener TODOS los datos antes de usar la herramienta: nombre completo, teléfono, email, fecha/hora, número de personas
- La fecha debe ser en formato YYYY-MM-DDTHH:mm (ejemplo: 2025-11-25T19:30)
- El horario debe estar entre 9:00 AM y 11:00 PM
- Número de personas: entre 1 y 20
- Pregunta de forma amigable si falta algún dato

**FORMATO DE FECHAS**:
- Cuando el usuario diga "mañana a las 8 de la noche", calcula la fecha correcta y conviértela a formato YYYY-MM-DDTHH:mm
- Ejemplo: Si hoy es 23 de noviembre de 2025 y dicen "mañana a las 8 PM", usa "2025-11-24T20:00"
- Las 8 PM = 20:00 en formato 24 horas

**TOKENS**:
- Cuando crees una reserva, el sistema devuelve un token único
- Explica al cliente que debe guardar ese token para consultar, modificar o cancelar su reserva
- El token también se envía por email

**HERRAMIENTAS DISPONIBLES**:
Tienes acceso a herramientas para ejecutar acciones reales. Úsalas cuando:
- El cliente pregunte por el menú más valorado
- El cliente quiera hacer una reserva (después de recopilar todos los datos)
- El cliente quiera modificar o cancelar su reserva (necesita el token)
- El cliente quiera consultar el estado de su reserva (necesita el token)

Sé cordial, empático y profesional. Confirma siempre los datos antes de ejecutar acciones.
"""

# Modelos Pydantic
class Message(BaseModel):
    role: str  # 'user' o 'assistant'
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: Optional[str] = None

# Almacenamiento temporal de sesiones (en producción usar Redis o base de datos)
chat_sessions = {}

@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servicio está funcionando"""
    return {
        "service": "Agente IA Restaurante",
        "status": "online",
        "model": "gemini-flash",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal para conversación con el agente con tools MCP
    
    Args:
        request: Objeto con el historial de mensajes y session_id opcional
    
    Returns:
        Respuesta del agente con el texto generado
    """
    try:
        # Definir las funciones disponibles para Gemini
        tools_for_gemini = []
        for tool_def in TOOLS_DEFINITIONS:
            func_declaration = {
                "name": tool_def["name"],
                "description": tool_def["description"]
            }
            if tool_def.get("parameters"):
                func_declaration["parameters"] = tool_def["parameters"]
            tools_for_gemini.append(func_declaration)
        
        # Inicializar el modelo con tools
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings,
            tools=[{"function_declarations": tools_for_gemini}]
        )
        
        # Construir el historial de conversación
        history = []
        for msg in request.messages[:-1]:  # Todos menos el último
            history.append({
                "role": "user" if msg.role == "user" else "model",
                "parts": [msg.content]
            })
        
        # Iniciar chat con historial
        chat = model.start_chat(history=history, enable_automatic_function_calling=True)
        
        # Obtener el último mensaje del usuario
        user_message = request.messages[-1].content if request.messages else ""
        
        # Agregar contexto del sistema al primer mensaje
        if len(history) == 0:
            user_message = f"{SYSTEM_PROMPT}\n\nUsuario: {user_message}"
        
        # Enviar mensaje
        response = chat.send_message(user_message)
        
        # Manejar llamadas a funciones si las hay
        while response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = dict(function_call.args)
            
            # Ejecutar la función correspondiente
            if hasattr(restaurante_tools, function_name):
                func = getattr(restaurante_tools, function_name)
                function_response = await func(**function_args)
            else:
                function_response = {"error": f"Función {function_name} no encontrada"}
            
            # Enviar resultado de la función al modelo
            response = chat.send_message(
                genai.protos.Content(
                    parts=[genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response={"result": function_response}
                        )
                    )]
                )
            )
        
        return ChatResponse(
            response=response.text,
            session_id=request.session_id
        )
        
    except Exception as e:
        import traceback
        error_detail = f"Error al procesar el chat: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@app.post("/chat/reset")
async def reset_chat(session_id: Optional[str] = None):
    """
    Reiniciar una sesión de chat
    """
    if session_id and session_id in chat_sessions:
        del chat_sessions[session_id]
    
    return {"message": "Sesión reiniciada correctamente"}

@app.get("/menus")
async def get_menus():
    """
    Obtener menús desde la API de Node.js para contexto del agente
    (Para futuras mejoras con tools)
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NODE_API_URL}/menus")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener menús: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🤖 Iniciando Agente IA en {host}:{port}")
    print(f"📡 Conectado a Node API: {NODE_API_URL}")
    
    uvicorn.run(app, host=host, port=port)
