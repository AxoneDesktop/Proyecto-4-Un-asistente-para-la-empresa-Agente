# 🤖 MCP Tools - Capacidades del Agente IA

El agente conversacional ahora tiene capacidades para ejecutar acciones reales en el sistema mediante **MCP (Model Context Protocol) Tools**.

## 🎯 Funcionalidades Disponibles

### 1. **Consultar Menú Más Valorado** ✨
```python
get_menu_mas_valorado()
```
- Obtiene el menú con mejor valoración promedio
- Devuelve nombre, descripción, precio y valoración
- **Ejemplo de uso**: "¿Cuál es vuestro menú más popular?"

### 2. **Listar Menús Disponibles** 📋
```python
listar_menus_disponibles()
```
- Lista todos los menús actualmente disponibles
- Incluye precios, descripciones y valoraciones
- **Ejemplo de uso**: "¿Qué menús tenéis?"

### 3. **Crear Reserva** 📅
```python
crear_reserva(
    nombre_cliente: str,
    telefono_cliente: str,
    email_cliente: str,
    fecha_reserva: str,  # Formato: YYYY-MM-DDTHH:mm
    num_personas: int,    # Entre 1 y 20
    notas: str = None
)
```
- Crea una nueva reserva en el sistema
- Envía email con token de confirmación
- Valida todos los datos automáticamente
- **Ejemplo de conversación**:
  ```
  Usuario: "Quiero hacer una reserva"
  Agente: "¡Perfecto! ¿Para cuántas personas?"
  Usuario: "4 personas"
  Agente: "¿Para qué día y hora?"
  Usuario: "Mañana a las 8 de la noche"
  Agente: "¿Cuál es tu nombre completo?"
  Usuario: "Juan Pérez"
  Agente: "¿Tu teléfono?"
  Usuario: "666777888"
  Agente: "¿Y tu email?"
  Usuario: "juan@example.com"
  Agente: [EJECUTA crear_reserva y devuelve el token]
  ```

### 4. **Consultar Reserva** 🔍
```python
consultar_reserva(token: str)
```
- Verifica el estado de una reserva
- Muestra toda la información: fecha, estado, personas, etc.
- **Ejemplo de uso**: "Quiero consultar mi reserva TOKEN-ABC-123"

### 5. **Modificar Fecha de Reserva** ✏️
```python
modificar_fecha_reserva(
    token: str,
    nueva_fecha: str  # Formato: YYYY-MM-DDTHH:mm
)
```
- Cambia la fecha y hora de una reserva existente
- Solo funciona con reservas confirmadas
- Valida que la nueva fecha esté en horario permitido
- **Ejemplo de uso**: "Mi token es ABC123, quiero cambiar mi reserva al viernes a las 7 PM"

### 6. **Cancelar Reserva** ❌
```python
cancelar_reserva(token: str)
```
- Cancela una reserva existente
- Acción irreversible
- **Ejemplo de uso**: "Quiero cancelar mi reserva, mi token es ABC123"

## 🔧 Cómo Funciona

### Arquitectura MCP

```
Usuario → Frontend (Chat) → FastAPI → Gemini con Tools → MCP Tools → Backend Node.js → MySQL
                                           ↓
                                    Respuesta Natural
```

### Flujo de Ejecución

1. **Usuario envía mensaje** al chat
2. **Gemini analiza** si necesita usar una herramienta
3. **Si necesita datos adicionales**, pregunta al usuario
4. **Cuando tiene todos los datos**, ejecuta la función correspondiente
5. **La función MCP** hace la llamada al backend Node.js
6. **Backend procesa** y devuelve resultado
7. **Gemini formula** una respuesta natural con el resultado
8. **Usuario recibe** respuesta conversacional

## 📝 Formato de Fechas

El agente entiende lenguaje natural y lo convierte automáticamente:

| Usuario Dice | Agente Convierte |
|-------------|------------------|
| "Mañana a las 8 PM" | `2025-11-24T20:00` |
| "Pasado mañana a las 7 de la tarde" | `2025-11-25T19:00` |
| "El viernes a las 9 de la noche" | `2025-11-29T21:00` |

**Horario permitido**: 9:00 AM - 11:00 PM (09:00 - 23:00)

## 🎨 Características del Agente

### Inteligente
- ✅ Recopila datos de forma conversacional
- ✅ Valida formato de emails y teléfonos
- ✅ Convierte fechas de lenguaje natural a formato ISO
- ✅ Confirma datos antes de ejecutar acciones

### Seguro
- ✅ Requiere token para modificaciones
- ✅ Valida permisos antes de cancelar
- ✅ Solo modifica reservas confirmadas
- ✅ Maneja errores con mensajes claros

### Amigable
- ✅ Respuestas en lenguaje natural
- ✅ Emojis para mejorar experiencia
- ✅ Confirmaciones claras
- ✅ Guía paso a paso

## 🧪 Probar el MCP

### Prueba Básica
```bash
cd C:\Users\axone\Documents\GitHub\Proyecto-4-Un-asistente-para-la-empresa-Agente
python test_mcp.py
```

### Pruebas Manuales desde el Chat

1. **Menú más valorado**:
   - "¿Cuál es vuestro mejor menú?"
   - "¿Qué menú recomendáis?"

2. **Crear reserva**:
   - "Quiero reservar mesa para 4 personas mañana"
   - El agente te guiará para recopilar todos los datos

3. **Consultar reserva**:
   - "Mi token es ABC123, ¿cuál es el estado de mi reserva?"

4. **Modificar fecha**:
   - "Tengo la reserva ABC123, quiero cambiarla al sábado a las 8 PM"

5. **Cancelar**:
   - "Cancelar mi reserva ABC123"

## ⚙️ Configuración

Las tools están en `mcp_tools.py` y se integran automáticamente con Gemini mediante:

```python
from mcp_tools import restaurante_tools, TOOLS_DEFINITIONS

# En main.py, Gemini recibe las definiciones
tools=[{"function_declarations": tools_for_gemini}]

# Y puede llamar a las funciones
await restaurante_tools.crear_reserva(...)
```

## 🔄 Extensiones Futuras

Fácilmente se pueden agregar más tools:

- ✨ Consultar disponibilidad de mesas
- ✨ Registrar llegada de cliente
- ✨ Ver pedidos de una reserva
- ✨ Solicitar la cuenta
- ✨ Dejar valoración de menú
- ✨ Ver promociones activas

Solo necesitas:
1. Agregar la función en `mcp_tools.py`
2. Agregar la definición en `TOOLS_DEFINITIONS`
3. El agente automáticamente podrá usarla

## 📊 Ventajas del MCP

- 🚀 **Acciones Reales**: No solo informa, ejecuta
- 🤝 **Conversacional**: Recopila datos naturalmente
- 🔒 **Seguro**: Valida permisos y datos
- 📱 **Integrado**: Conecta frontend, IA y backend
- 🎯 **Preciso**: Gemini decide cuándo usar cada tool
