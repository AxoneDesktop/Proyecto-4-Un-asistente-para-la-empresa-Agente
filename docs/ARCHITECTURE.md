# 🎯 Sistema Multi-Agente - Arquitectura Visual

## Flujo de Ejecución

```
┌─────────────────────────────────────────────────────────────────┐
│                          USUARIO                                 │
│                     (Frontend/Cliente)                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Server                                │
│                   POST /chat endpoint                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            RestauranteMultiAgentSystem                           │
│                  (Sistema Coordinador)                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
            ┌────────────────────────┐
            │  🎯 ORQUESTADOR        │
            │  Analiza consulta      │
            │  Decide routing        │
            └────────┬───────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 📅 RESERVAS  │ │ 🍽️ MENÚS     │ │ ℹ️ INFO      │
│              │ │              │ │              │
│ - Crear      │ │ - Listar     │ │ - Horarios   │
│ - Modificar  │ │ - Recomendar │ │ - Ubicación  │
│ - Cancelar   │ │ - Valorar    │ │ - Políticas  │
│ - Consultar  │ │              │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │    MCP Tools          │
            │  (restaurante_tools)  │
            └───────────┬───────────┘
                        │
                        ▼
            ┌───────────────────────┐
            │   Node.js Backend     │
            │   (API REST)          │
            └───────────────────────┘
```

## Componentes Principales

### 1. Agent Runner System
```
AgentRunner (Base Class)
├── agent_id: str
├── agent_type: AgentType
├── model: GenerativeModel
├── status: AgentStatus
├── execute() → Dict
└── reset()

MultiAgentRunner
├── agents: Dict[str, AgentRunner]
├── register_agent()
├── execute_agent()
├── execute_parallel()
└── get_system_status()
```

### 2. Tipos de Agentes

```python
AgentType (Enum)
├── ORCHESTRATOR  # Coordina y delega
├── RESERVAS      # Gestión de reservas
├── MENUS         # Información de menús
└── INFO          # Info general
```

### 3. Estados del Agente

```python
AgentStatus (Enum)
├── IDLE          # En espera
├── RUNNING       # Ejecutando
├── WAITING       # Esperando respuesta
├── ERROR         # Error ocurrido
└── COMPLETED     # Completado exitosamente
```

## Ejemplo de Flujo Completo

### Consulta Simple (1 Agente)
```
Usuario: "¿Cuál es el horario?"
    ↓
Orquestador analiza → Decide: info_agent
    ↓
Info Agent ejecuta → Responde: "9:00 AM - 11:00 PM"
    ↓
Usuario recibe respuesta
```

### Consulta Múltiple (2+ Agentes)
```
Usuario: "¿Qué menú recomiendas y cuál es el horario?"
    ↓
Orquestador analiza → Decide: [menus_agent, info_agent]
    ↓
    ├→ Menús Agent (paralelo) → "Recomiendo el Menú Premium..."
    └→ Info Agent (paralelo)  → "Horario: 9:00 AM - 11:00 PM"
    ↓
Combina respuestas
    ↓
Usuario recibe respuesta completa
```

### Consulta con Tools (Reserva)
```
Usuario: "Quiero reservar para 4 personas mañana a las 8 PM"
    ↓
Orquestador → reservas_agent
    ↓
Reservas Agent → Solicita datos faltantes
    ↓
Usuario: "Mi nombre es Juan, tel 123456789, email juan@email.com"
    ↓
Reservas Agent → Llama MCP Tool: crear_reserva()
    ↓
MCP Tool → Node.js Backend API
    ↓
Backend → Crea reserva, envía email, devuelve token
    ↓
Reservas Agent → Confirma y explica el token
    ↓
Usuario recibe confirmación con token
```

## Escalabilidad

```
Añadir Nuevo Agente:
    1. Crear prompt especializado
    2. Factory method en AgentFactory
    3. Registrar en RestauranteMultiAgentSystem
    4. Actualizar prompt del orquestador
    5. Agregar tests

Ventajas:
✅ Modular - Agentes independientes
✅ Escalable - Fácil agregar nuevos agentes
✅ Mantenible - Cambios aislados por agente
✅ Observable - Tracking completo de estados
✅ Paralelo - Múltiples agentes simultáneos
```

## Metrics & Monitoring

```
Endpoint: GET /agents/status

Respuesta:
{
  "total_agents": 4,
  "agents": {
    "orchestrator": {
      "status": "idle",
      "execution_count": 15,
      "history_length": 30
    },
    "reservas_agent": {
      "status": "completed",
      "execution_count": 8,
      "history_length": 16
    },
    ...
  }
}
```

## Consideraciones de Diseño

### ✅ Ventajas del Patrón Multi-Agente
- Especialización por dominio
- Prompts optimizados por tarea
- Ejecución paralela eficiente
- Fácil testing individual
- Logging granular

### ⚠️ Trade-offs
- Mayor complejidad inicial
- Más llamadas a API (orquestador + agente)
- Necesita coordinación cuidadosa
- Requiere buen prompt del orquestador

### 🎯 Optimizaciones Implementadas
- Cache de modelos Gemini
- Historial por agente (no global)
- Reinicio selectivo de agentes
- Timeout por ejecución
- Error handling robusto
