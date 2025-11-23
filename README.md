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

## 📡 Endpoints

### `GET /`
Información del servicio

### `GET /health`
Health check del servicio

### `POST /chat`
Conversación con el agente

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

Una vez iniciado, puedes probar en:
- **Documentación interactiva**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Ejemplo con curl:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hola, ¿cuál es el horario del restaurante?\"}]}"
```

## 🔄 Integración con el Sistema

El agente puede:
- ✅ Responder preguntas sobre el restaurante
- ✅ Guiar en el proceso de reservas
- ✅ Explicar cómo consultar reservas
- ✅ Informar sobre valoraciones
- 🔜 Acceder a información de menús (próximamente con tools)
- 🔜 Consultar disponibilidad de reservas (próximamente con tools)

## 📦 Estructura del Proyecto

```
Proyecto-4-Un-asistente-para-la-empresa-Agente/
├── main.py              # Aplicación principal FastAPI
├── requirements.txt     # Dependencias Python
├── .env                 # Variables de entorno (no en git)
├── .env.example         # Plantilla de variables de entorno
├── .gitignore          # Archivos ignorados por git
├── test_chat.py        # Script de pruebas
└── README.md           # Esta documentación
```

## 🛠️ Próximas Mejoras

1. **Tools/Functions** para que el agente pueda:
   - Consultar menús disponibles
   - Verificar disponibilidad de reservas
   - Consultar estado de reserva por token

2. **Persistencia de sesiones** con Redis

3. **Logging avanzado** para monitoreo

4. **Rate limiting** para protección del servicio

## 🔐 Seguridad

- Las API Keys se gestionan mediante variables de entorno
- CORS configurado para dominios específicos
- Safety settings de Gemini activados

## 📝 Notas

- El modelo usado es `gemini-1.5-flash` (rápido y eficiente)
- Configuración de temperatura: 0.7 (balance entre creatividad y coherencia)
- Max tokens de salida: 2048
