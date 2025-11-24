"""
Microservicio Multi-Agente IA para el restaurante
Sistema de agentes especializados con Gemini Flash
- Agente de Reservas
- Agente de Menús  
- Agente de Información General
- Orquestador para coordinar agentes
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
from multi_agents import RestauranteMultiAgentSystem

# Cargar variables de entorno
load_dotenv()

# Configurar Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY no está configurada en el archivo .env")

genai.configure(api_key=GEMINI_API_KEY)

# Crear la aplicación FastAPI
app = FastAPI(
    title="Sistema Multi-Agente IA Restaurante",
    description="Microservicio multi-agente con Gemini Flash: Reservas, Menús e Info General",
    version="2.0.0"
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

# Inicializar el sistema multi-agente
multi_agent_system = None

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

@app.on_event("startup")
async def startup_event():
    """Inicializa el sistema multi-agente al arrancar"""
    global multi_agent_system
    multi_agent_system = RestauranteMultiAgentSystem()
    print("✅ Sistema Multi-Agente inicializado")

@app.get("/")
async def root():
    """Endpoint raíz para verificar que el servicio está funcionando"""
    return {
        "service": "Sistema Multi-Agente IA Restaurante",
        "status": "online",
        "architecture": "multi-agent",
        "agents": ["reservas", "menus", "info", "orchestrator"],
        "version": "2.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal para conversación con el sistema multi-agente
    
    El orquestador analiza la consulta y delega a los agentes especializados:
    - reservas_agent: Maneja reservas (crear, modificar, cancelar, consultar)
    - menus_agent: Información de menús y recomendaciones
    - info_agent: Información general del restaurante
    
    Args:
        request: Objeto con el historial de mensajes y session_id opcional
    
    Returns:
        Respuesta coordinada del sistema multi-agente
    """
    try:
        if not multi_agent_system:
            raise HTTPException(status_code=503, detail="Sistema multi-agente no inicializado")
        
        # Obtener el último mensaje del usuario
        user_message = request.messages[-1].content if request.messages else ""
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Mensaje vacío")
        
        # Procesar con el sistema multi-agente
        result = await multi_agent_system.process_message(
            user_message=user_message,
            session_id=request.session_id
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Error al procesar mensaje")
            )
        
        return ChatResponse(
            response=result.get("response", ""),
            session_id=result.get("session_id")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error al procesar el chat: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@app.post("/chat/reset")
async def reset_chat(session_id: Optional[str] = None):
    """
    Reiniciar una sesión de chat (reinicia todos los agentes)
    """
    if not multi_agent_system:
        raise HTTPException(status_code=503, detail="Sistema multi-agente no inicializado")
    
    multi_agent_system.reset_session(session_id)
    
    return {"message": "Sesión reiniciada correctamente", "session_id": session_id}

@app.get("/agents/status")
async def agents_status():
    """
    Obtiene el estado de todos los agentes del sistema
    """
    if not multi_agent_system:
        raise HTTPException(status_code=503, detail="Sistema multi-agente no inicializado")
    
    return multi_agent_system.get_system_status()

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
    
    print("=" * 60)
    print("🚀 SISTEMA MULTI-AGENTE IA - RESTAURANTE")
    print("=" * 60)
    print(f"🤖 Iniciando en {host}:{port}")
    print(f"📡 Node API: {NODE_API_URL}")
    print("\n🎯 Agentes disponibles:")
    print("   - Orquestador: Coordina y delega tareas")
    print("   - Reservas Agent: Gestión de reservas")
    print("   - Menús Agent: Información de menús")
    print("   - Info Agent: Información general")
    print("=" * 60)
    
    uvicorn.run(app, host=host, port=port)
