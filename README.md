# 🤖 Sistema Multi-Agente IA - Restaurante

Sistema de agentes IA especializados con FastAPI y Google Gemini Flash para gestión de reservas de restaurante.

**📚 Capstone Project - 5-Day Gen AI Intensive Course (Google & Kaggle)**

## 🚀 Características

- **Sistema Multi-Agente** con orquestador inteligente
- **4 Agentes Especializados**: Reservas, Menús, Info, Orquestador
- **Function Calling** con herramientas MCP personalizadas
- **Ejecución Paralela** para consultas multi-dominio
- **Memoria Conversacional** por sesión
- **API RESTful** con FastAPI

## 📁 Estructura del Proyecto

```
├── src/                    # Código fuente principal
│   ├── main.py            # API FastAPI
│   ├── agent_runner.py    # Sistema de ejecución de agentes
│   ├── multi_agents.py    # Definición de agentes especializados
│   └── mcp_tools.py       # Herramientas MCP (function calling)
├── tests/                  # Tests del sistema
│   ├── test_chat.py
│   ├── test_multiagent.py
│   └── ...
├── docs/                   # Documentación técnica
│   ├── ARCHITECTURE.md    # Arquitectura detallada
│   ├── MCP_TOOLS.md       # Documentación de herramientas
│   ├── EXAMPLES.md        # Ejemplos de uso
│   └── diagrams/          # Diagramas de arquitectura
├── run.py                  # Script de arranque
├── requirements.txt
├── .env.example
├── CAPSTONE_PROJECT.md     # Documento del Capstone
└── README.md
```

## 📋 Requisitos Previos

- Python 3.9+
- API Key de Google Gemini
- Backend Node.js corriendo (puerto 3000)
- Base de datos MySQL configurada

## 🔧 Instalación Rápida

```bash
# 1. Clonar repositorio
git clone https://github.com/AxoneDesktop/Proyecto-4-Un-asistente-para-la-empresa-Agente.git
cd Proyecto-4-Un-asistente-para-la-empresa-Agente

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
copy .env.example .env
# Editar .env y agregar tu GEMINI_API_KEY
```

## 🎯 Obtener API Key de Google Gemini

1. Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crear API Key
3. Agregarla al archivo `.env`

## ▶️ Ejecutar el Servicio

```bash
python run.py
```

El servicio estará disponible en: `http://localhost:8000`

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Arquitectura Multi-Agente

```
Usuario → Orquestador → [Analiza consulta] → Selecciona Agente(s)
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
              📅 Reservas         🍽️ Menús         ℹ️ Info
                    ↓
              Respuesta(s) → Combinadas → Usuario
```

### Agentes Especializados

| Agente | Responsabilidad |
|--------|-----------------|
| 🎯 Orquestador | Analiza intención y delega a agentes |
| 📅 Reservas | Crear, modificar, cancelar, consultar reservas |
| 🍽️ Menús | Listar y recomendar menús |
| ℹ️ Info | Horarios, ubicación, navegación |

## 📡 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Info del servicio |
| GET | `/health` | Health check |
| GET | `/agents/status` | Estado de agentes |
| POST | `/chat` | Conversación con agente |
| POST | `/chat/reset` | Reiniciar sesión |

### Ejemplo de uso

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Quiero reservar para 4 personas mañana"}]}'
```

## 🧪 Tests

```bash
cd tests
python test_multiagent.py
```

## 📖 Documentación Adicional

- [Arquitectura del Sistema](docs/ARCHITECTURE.md)
- [Herramientas MCP](docs/MCP_TOOLS.md)
- [Ejemplos de Uso](docs/EXAMPLES.md)
- [Capstone Project](CAPSTONE_PROJECT.md)

## 🔗 Repositorios Relacionados

- **Backend**: [Proyecto-4-Un-asistente-para-la-empresa-backend](https://github.com/AxoneDesktop/Proyecto-4-Un-asistente-para-la-empresa-backend)
- **Frontend**: [Proyecto-4-Un-asistente-para-la-empresa-frontend](https://github.com/AxoneDesktop/Proyecto-4-Un-asistente-para-la-empresa-frontend)

## 📝 Notas Técnicas

- **Modelo**: Gemini 2.5 Flash
- **Framework**: FastAPI + Python 3.11
- **Temperatura**: 0.3 (orquestador) / 0.7 (agentes)

## 📄 Licencia

MIT License
