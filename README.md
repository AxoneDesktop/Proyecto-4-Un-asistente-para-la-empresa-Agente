# 🤖 Agente IA - Microservicio Conversacional

Microservicio Python con FastAPI y Google Gemini Flash para el sistema de reservas del restaurante.

## 🚀 Características

- **Agente conversacional** con Google Gemini Flash
- **API RESTful** con FastAPI
- **Integración** con la API Node.js del backend
- **Historial de conversación** mantenido por sesión
- **CORS configurado** para el frontend

## 📋 Requisitos Previos

- Python 3.9 o superior
- Cuenta de Google Cloud con API de Gemini habilitada
- API Key de Google Gemini

## 🔧 Instalación

1. **Crear entorno virtual**:
```bash
python -m venv venv
```

2. **Activar entorno virtual**:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**:
- Copiar `.env.example` a `.env`
- Agregar tu API Key de Google Gemini en `GEMINI_API_KEY`

```bash
copy .env.example .env
```

Editar `.env` y agregar:
```
GEMINI_API_KEY=tu_api_key_aqui
```

## 🎯 Obtener API Key de Google Gemini

1. Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Iniciar sesión con tu cuenta de Google
3. Hacer clic en "Create API Key"
4. Copiar la clave y agregarla al archivo `.env`

## ▶️ Ejecutar el Servicio

```bash
python main.py
```

El servicio estará disponible en: `http://localhost:8000`

## 🏗️ Arquitectura Multi-Agente

### Flujo de Procesamiento

```
Usuario → Orquestador → [Analiza consulta] → Selecciona Agente(s)
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              Agente(s)            Ejecutan en paralelo
              Especializado(s)     si es necesario
                    ↓
              Respuesta(s) → Combinadas → Usuario
```

### Agentes Especializados

#### 🎯 Orquestador
- Analiza la intención del usuario
- Decide qué agente(s) debe(n) responder
- Puede invocar múltiples agentes en paralelo

#### 📅 Agente de Reservas
- Crear nuevas reservas (requiere todos los datos)
- Modificar fecha de reservas existentes
- Cancelar reservas
- Consultar estado de reservas
- Validar datos y horarios

#### 🍽️ Agente de Menús
- Recomendar menús (más valorado)
- Listar menús disponibles
- Describir platos y precios
- Información nutricional (próximamente)

#### ℹ️ Agente de Información
- Horarios del restaurante
- Ubicación y direcciones
- Políticas generales
- Ambiente y servicios

## 📡 Endpoints

### `GET /`
Información del servicio y agentes disponibles

### `GET /health`
Health check del servicio

### `GET /agents/status`
Estado de todos los agentes (ejecuciones, historial, etc.)

### `POST /chat`
Conversación con el sistema multi-agente

**Request Body**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Hola, quisiera información sobre el restaurante"
    }
  ],
  "session_id": "opcional-id-de-sesion"
}
```

**Response**:
```json
{
  "response": "¡Hola! Bienvenido a nuestro restaurante...",
  "session_id": "opcional-id-de-sesion"
}
```

### `POST /chat/reset`
Reiniciar sesión de chat

### `GET /menus`
Obtener menús desde la API Node.js (para futuras mejoras)

## 🧪 Probar el Servicio

### 1. Script de Prueba Multi-Agente

```bash
python test_multiagent.py
```

Este script prueba:
- Routing del orquestador
- Respuestas de cada agente especializado
- Ejecución paralela de múltiples agentes
- Estado del sistema

### 2. Documentación Interactiva

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Ejemplos con curl

**Consulta simple (un agente)**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"messages\": [{\"role\": \"user\", \"content\": \"¿Cuál es el horario?\"}]}"
```

**Consulta múltiple (varios agentes)**:
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"messages\": [{\"role\": \"user\", \"content\": \"¿Qué menú recomiendas y cuál es el horario?\"}]}"
```

**Estado de los agentes**:
```bash
curl http://localhost:8000/agents/status
```

## 🔄 Integración con el Sistema

El sistema multi-agente puede:

### ✅ Implementado
- **Reservas completas**: Crear, modificar, cancelar, consultar
- **Gestión de menús**: Recomendar y listar menús disponibles
- **Información general**: Horarios, ubicación, políticas
- **Routing inteligente**: Delega automáticamente a agente correcto
- **Ejecución paralela**: Múltiples agentes responden simultáneamente
- **MCP Tools**: Integración completa con backend Node.js

### 🔜 Próximamente
- Persistencia de sesiones con Redis
- Agent memory para contexto entre sesiones
- Métricas y analytics de agentes
- A/B testing de prompts de agentes

## 📦 Estructura del Proyecto

```
Proyecto-4-Un-asistente-para-la-empresa-Agente/
├── main.py                 # API FastAPI con endpoints
├── agent_runner.py         # Sistema de Agent Runners
├── multi_agents.py         # Definición de agentes especializados
├── mcp_tools.py           # Herramientas MCP para agentes
├── requirements.txt       # Dependencias Python
├── .env                   # Variables de entorno (no en git)
├── .env.example          # Plantilla de variables de entorno
├── test_multiagent.py    # Pruebas del sistema multi-agente
├── test_chat.py          # Pruebas de chat básicas
└── README.md             # Esta documentación
```

### Componentes Clave

- **`agent_runner.py`**: 
  - `AgentRunner`: Clase base para ejecutar agentes
  - `MultiAgentRunner`: Gestor de múltiples agentes
  - Sistema de estados y logging

- **`multi_agents.py`**:
  - `AgentFactory`: Crea agentes especializados
  - `RestauranteMultiAgentSystem`: Sistema completo
  - Prompts especializados para cada agente

- **`mcp_tools.py`**:
  - Herramientas para interactuar con backend
  - Definiciones de tools para Gemini
  - Cliente HTTP para Node.js API

## 🛠️ Ventajas del Sistema Multi-Agente

### ✨ Especialización
Cada agente es experto en su dominio, con prompts optimizados

### ⚡ Paralelismo
Múltiples consultas procesadas simultáneamente

### 🎯 Precisión
El orquestador asegura que el agente correcto responda

### 🔧 Mantenibilidad
Fácil agregar nuevos agentes sin modificar existentes

### 📊 Observabilidad
Tracking detallado de ejecuciones y estados

## 🆕 Agregar un Nuevo Agente

```python
# 1. Definir prompt del agente
NUEVO_AGENT_PROMPT = """..."""

# 2. Crear factory method
@staticmethod
def create_nuevo_agent(agent_id: str = "nuevo_agent"):
    model = genai.GenerativeModel(...)
    return AgentRunner(agent_id, AgentType.NUEVO, model)

# 3. Registrar en el sistema
nuevo_agent = AgentFactory.create_nuevo_agent()
self.runner.register_agent(nuevo_agent)

# 4. Actualizar prompt del orquestador
```

## 🔐 Seguridad

- Las API Keys se gestionan mediante variables de entorno
- CORS configurado para dominios específicos
- Safety settings de Gemini activados

## 📝 Notas Técnicas

- **Modelo**: `gemini-2.0-flash-exp` (última versión, más rápido)
- **Temperatura**: 
  - Orquestador: 0.3 (más determinístico para routing)
  - Agentes especializados: 0.7 (balance creatividad/coherencia)
- **Max tokens**: 2048 para respuestas, 512 para orquestador
- **Safety settings**: Habilitados para todos los agentes

## 🤝 Contribuir

Para contribuir al sistema multi-agente:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nuevo-agente`)
3. Implementa tu agente siguiendo el patrón existente
4. Agrega tests en `test_multiagent.py`
5. Commit y push (`git commit -m 'Add: nuevo agente'`)
6. Crea un Pull Request
