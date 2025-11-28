# 💡 Ejemplos de Uso del Sistema Multi-Agente

## Tabla de Contenidos
1. [Ejemplos Básicos](#ejemplos-básicos)
2. [Consultas Múltiples](#consultas-múltiples)
3. [Gestión de Reservas](#gestión-de-reservas)
4. [Consultas de Menús](#consultas-de-menús)
5. [Información General](#información-general)
6. [Casos Especiales](#casos-especiales)

---

## Ejemplos Básicos

### 1. Saludo Inicial
```
👤 Usuario: "Hola, buenos días"

🎯 Orquestador decide: info_agent
📨 Info Agent responde:
"¡Buenos días! Bienvenido a nuestro restaurante. Estoy aquí para ayudarte. 
Puedo ayudarte con información sobre nuestros menús, hacer reservas, 
consultar el horario o cualquier otra información que necesites. ¿En qué 
puedo asistirte hoy?"
```

### 2. Consulta Simple de Horarios
```
👤 Usuario: "¿Cuál es el horario del restaurante?"

🎯 Orquestador decide: info_agent
📨 Info Agent responde:
"Nuestro horario de atención es de 9:00 AM a 11:00 PM, todos los días 
de la semana. ¡Te esperamos!"
```

---

## Consultas Múltiples

### 3. Menú + Horario (2 Agentes en Paralelo)
```
👤 Usuario: "¿Qué menú me recomiendas y cuál es el horario?"

🎯 Orquestador decide: [menus_agent, info_agent]
📨 Respuesta combinada:

**Menús**: 
"Te recomiendo nuestro Menú Premium, que tiene una valoración de 4.8/5 
estrellas. Incluye entrada de ensalada gourmet, plato principal a elegir 
entre salmón a la parrilla o filete de res, y postre de chocolate 
artesanal. Precio: $35.00"

**Info**: 
"Nuestro horario es de 9:00 AM a 11:00 PM todos los días. ¡Te esperamos!"
```

### 4. Reserva + Recomendación
```
👤 Usuario: "Quiero hacer una reserva y saber qué menú recomiendan"

🎯 Orquestador decide: [reservas_agent, menus_agent]
📨 Respuesta combinada:

**Reservas**: 
"¡Con gusto te ayudo a hacer tu reserva! Para continuar, necesito los 
siguientes datos:
- Nombre completo
- Teléfono de contacto
- Email
- Fecha y hora deseada
- Número de personas"

**Menús**: 
"Para acompañar tu visita, te recomiendo nuestro Menú Signature, 
el más valorado por nuestros clientes..."
```

---

## Gestión de Reservas

### 5. Crear Reserva (Proceso Completo)

#### Paso 1: Solicitud Inicial
```
👤 Usuario: "Quiero hacer una reserva para mañana"

🎯 Orquestador decide: reservas_agent
📨 Reservas Agent:
"¡Perfecto! Te ayudaré a crear tu reserva para mañana. 
Necesito los siguientes datos:
1. ¿Cuál es tu nombre completo?
2. ¿Número de teléfono?
3. ¿Email?
4. ¿A qué hora te gustaría la reserva? (Horario: 9:00 AM - 11:00 PM)
5. ¿Para cuántas personas?"
```

#### Paso 2: Usuario Proporciona Datos
```
👤 Usuario: "Juan Pérez, tel 555-1234, juan@email.com, 
             para 4 personas a las 8 de la noche"

🎯 Orquestador decide: reservas_agent
🔧 Reservas Agent llama: crear_reserva()
   - nombre_cliente: "Juan Pérez"
   - telefono_cliente: "555-1234"
   - email_cliente: "juan@email.com"
   - fecha_reserva: "2025-11-25T20:00"
   - num_personas: 4

📨 Reservas Agent responde:
"¡Reserva confirmada exitosamente! 

📋 Detalles:
- Nombre: Juan Pérez
- Fecha: 25 de noviembre de 2025 a las 8:00 PM
- Personas: 4
- Token: RES-ABC123XYZ

🔑 IMPORTANTE: Guarda este token (RES-ABC123XYZ). Lo necesitarás para:
- Consultar tu reserva
- Modificar la fecha
- Cancelar si es necesario

También hemos enviado un email de confirmación a juan@email.com con 
todos los detalles. ¡Te esperamos!"
```

### 6. Consultar Reserva
```
👤 Usuario: "Quiero ver mi reserva con el token RES-ABC123XYZ"

🎯 Orquestador decide: reservas_agent
🔧 Reservas Agent llama: consultar_reserva(token="RES-ABC123XYZ")

📨 Reservas Agent responde:
"Aquí está tu reserva:

📋 Estado: Confirmada
👤 Cliente: Juan Pérez
📅 Fecha: 25 de noviembre de 2025 a las 8:00 PM
👥 Personas: 4
📧 Email: juan@email.com
📱 Teléfono: 555-1234
🔑 Token: RES-ABC123XYZ

¿Necesitas modificar algo?"
```

### 7. Modificar Fecha de Reserva
```
👤 Usuario: "Quiero cambiar mi reserva RES-ABC123XYZ para el sábado 
             a las 7 PM"

🎯 Orquestador decide: reservas_agent
🔧 Reservas Agent llama: modificar_fecha_reserva(
     token="RES-ABC123XYZ",
     nueva_fecha="2025-11-29T19:00"
   )

📨 Reservas Agent responde:
"✅ Fecha modificada exitosamente!

📋 Nueva información:
- Fecha anterior: 25 de noviembre a las 8:00 PM
- Nueva fecha: 29 de noviembre a las 7:00 PM
- Personas: 4
- Token: RES-ABC123XYZ (el mismo)

Hemos enviado un email de confirmación con los nuevos detalles."
```

### 8. Cancelar Reserva
```
👤 Usuario: "Necesito cancelar mi reserva RES-ABC123XYZ"

🎯 Orquestador decide: reservas_agent
🔧 Reservas Agent llama: cancelar_reserva(token="RES-ABC123XYZ")

📨 Reservas Agent responde:
"✅ Reserva cancelada exitosamente

📋 Detalles de la reserva cancelada:
- Cliente: Juan Pérez
- Fecha: 29 de noviembre a las 7:00 PM
- Token: RES-ABC123XYZ

Lamentamos que no puedas acompañarnos. Hemos enviado un email de 
confirmación de la cancelación. ¡Esperamos verte pronto en otra ocasión!"
```

---

## Consultas de Menús

### 9. Menú Más Valorado
```
👤 Usuario: "¿Cuál es el menú más popular?"

🎯 Orquestador decide: menus_agent
🔧 Menús Agent llama: get_menu_mas_valorado()

📨 Menús Agent responde:
"¡Excelente pregunta! Nuestro menú más valorado es:

🌟 MENÚ PREMIUM
⭐ Valoración: 4.8/5 (basado en 156 opiniones)
💰 Precio: $35.00

📋 Incluye:
• Entrada: Ensalada gourmet con vinagreta de frutos rojos
• Plato principal: Salmón a la parrilla con vegetales asados
  O Filete de res con puré de papas trufado
• Postre: Mousse de chocolate artesanal
• Bebida: Incluye una copa de vino de la casa o refresco

✅ Disponible todos los días

Los clientes destacan especialmente la frescura de los ingredientes 
y la excelente presentación. ¿Te gustaría hacer una reserva?"
```

### 10. Listar Todos los Menús
```
👤 Usuario: "Muéstrame todos los menús disponibles"

🎯 Orquestador decide: menus_agent
🔧 Menús Agent llama: listar_menus_disponibles()

📨 Menús Agent responde:
"Tenemos 4 deliciosos menús disponibles:

1️⃣ MENÚ EJECUTIVO
   ⭐ 4.2/5
   💰 $15.00
   📝 Perfecto para el mediodía. Incluye plato del día + ensalada + bebida

2️⃣ MENÚ FAMILIAR
   ⭐ 4.5/5
   💰 $60.00
   📝 Para 4 personas. Variedad de platos principales y acompañamientos

3️⃣ MENÚ PREMIUM ⭐ MÁS VALORADO
   ⭐ 4.8/5
   💰 $35.00
   📝 Experiencia gourmet completa con entrada, plato y postre

4️⃣ MENÚ VEGETARIANO
   ⭐ 4.6/5
   💰 $25.00
   📝 100% plant-based con ingredientes orgánicos

¿Te gustaría más detalles sobre alguno?"
```

---

## Información General

### 11. Ubicación y Cómo Llegar
```
👤 Usuario: "¿Dónde están ubicados?"

🎯 Orquestador decide: info_agent
📨 Info Agent responde:
"Nos encontramos en:

📍 Dirección: Av. Principal 123, Centro de la Ciudad
🅿️ Estacionamiento: Disponible sin costo
🚇 Metro más cercano: Estación Central (5 min a pie)
🚌 Rutas de autobús: Líneas 10, 15, 23

🕒 Horario: 9:00 AM - 11:00 PM todos los días

¿Necesitas indicaciones específicas?"
```

### 12. Políticas del Restaurante
```
👤 Usuario: "¿Cuáles son las políticas de cancelación?"

🎯 Orquestador decide: info_agent
📨 Info Agent responde:
"Nuestras políticas son:

📅 CANCELACIÓN:
- Puedes cancelar hasta 2 horas antes sin penalización
- Usa tu token de reserva para cancelar fácilmente

🕐 CAMBIO DE FECHA:
- Modificaciones sin costo hasta 2 horas antes
- Sujeto a disponibilidad

⏰ PUNTUALIDAD:
- Tolerancia de 15 minutos
- Después de 15 min, la reserva puede liberarse

👶 NIÑOS:
- ¡Bienvenidos! Tenemos menú infantil
- Sillas altas disponibles

🐕 MASCOTAS:
- Permitidas solo en terraza

¿Alguna pregunta específica?"
```

---

## Casos Especiales

### 13. Consulta Ambigua (Orquestador Decide)
```
👤 Usuario: "Ayuda"

🎯 Orquestador decide: info_agent
📨 Info Agent responde:
"¡Por supuesto! Estoy aquí para ayudarte. Puedo asistirte con:

🍽️ MENÚS: Recomendaciones, precios, ingredientes
📅 RESERVAS: Crear, modificar o cancelar reservas
ℹ️ INFORMACIÓN: Horarios, ubicación, políticas

¿Qué te gustaría saber?"
```

### 14. Error - Reserva sin Datos
```
👤 Usuario: "Haz una reserva"

🎯 Orquestador decide: reservas_agent
📨 Reservas Agent responde:
"¡Perfecto! Para crear tu reserva necesito la siguiente información:

1️⃣ ¿Cuál es tu nombre completo?
2️⃣ ¿Teléfono de contacto? (9-15 dígitos)
3️⃣ ¿Email?
4️⃣ ¿Fecha y hora preferida? (Horario: 9:00 AM - 11:00 PM)
5️⃣ ¿Número de personas? (1-20)
6️⃣ ¿Alguna nota especial? (opcional)

Por favor, proporcióname estos datos para continuar."
```

### 15. Token Inválido
```
👤 Usuario: "Consulta mi reserva con token INVALID123"

🎯 Orquestador decide: reservas_agent
🔧 Reservas Agent llama: consultar_reserva(token="INVALID123")

📨 Reservas Agent responde:
"❌ No pude encontrar una reserva con ese token.

Verifica que:
✓ El token esté escrito correctamente (distingue mayúsculas)
✓ El formato sea: RES-XXXXXXXXX
✓ La reserva no haya sido cancelada previamente

El token se envió a tu email al confirmar la reserva. 
¿Puedes revisarlo y volver a intentar?"
```

### 16. Fuera de Horario
```
👤 Usuario: "Quiero reservar para las 2 AM"

🎯 Orquestador decide: reservas_agent
📨 Reservas Agent responde:
"Lo siento, pero nuestro horario de atención es de 9:00 AM a 11:00 PM.

⏰ Horarios disponibles:
- Desayuno/Brunch: 9:00 AM - 12:00 PM
- Almuerzo: 12:00 PM - 4:00 PM
- Cena: 6:00 PM - 11:00 PM

¿Te gustaría hacer una reserva en uno de estos horarios?"
```

---

## Tips de Uso

### Para Obtener Mejor Respuesta:

✅ **Sé específico**
- ❌ "Quiero comer"
- ✅ "¿Qué menú me recomiendas para 2 personas con presupuesto de $50?"

✅ **Proporciona contexto**
- ❌ "Cambiar reserva"
- ✅ "Quiero cambiar mi reserva RES-ABC123 para el sábado a las 7 PM"

✅ **Usa lenguaje natural**
- ✅ "Quiero reservar para mañana a las 8 de la noche para 4 personas"
- ✅ "Necesito el menú más económico"
- ✅ "¿Aceptan mascotas?"

### El Sistema Entiende:

- 🕐 Formato de tiempo natural ("8 de la noche" = 20:00)
- 📅 Fechas relativas ("mañana", "este sábado")
- 💬 Sinónimos ("cancelar" = "anular", "menú" = "carta")
- 🔄 Contexto de conversación (recuerda lo que dijiste antes)

---

**Nota**: Todos estos ejemplos son funcionales con el sistema implementado. 
El orquestador decide inteligentemente qué agente(s) debe(n) responder 
basándose en el contenido de la consulta.
