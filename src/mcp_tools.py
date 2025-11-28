"""
MCP Server para el sistema de restaurante
Proporciona tools para que el agente IA pueda interactuar con el backend
"""
import os
import json
import httpx
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

NODE_API_URL = os.getenv("NODE_API_URL", "http://localhost:3000/api")

class RestauranteTools:
    """Herramientas para el agente del restaurante"""
    
    def __init__(self):
        self.api_url = NODE_API_URL
        
    async def get_menu_mas_valorado(self) -> Dict[str, Any]:
        """
        Obtiene el menú con mejor valoración promedio
        
        Returns:
            Información del menú más valorado
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Obtener todos los menús
                response = await client.get(f"{self.api_url}/menus")
                response.raise_for_status()
                menus = response.json()
                
                if not menus:
                    return {"error": "No hay menús disponibles"}
                
                # Encontrar el menú con mejor valoración
                mejor_menu = max(menus, key=lambda x: x.get('valoracion_promedio', 0))
                
                return {
                    "success": True,
                    "menu": {
                        "id": mejor_menu.get('id'),
                        "nombre": mejor_menu.get('nombre'),
                        "descripcion": mejor_menu.get('descripcion'),
                        "precio": mejor_menu.get('precio'),
                        "valoracion_promedio": mejor_menu.get('valoracion_promedio', 0),
                        "disponible": mejor_menu.get('disponible', False)
                    }
                }
        except Exception as e:
            return {"error": f"Error al obtener menús: {str(e)}"}
    
    async def crear_reserva(
        self,
        nombre_cliente: str,
        telefono_cliente: str,
        email_cliente: str,
        fecha_reserva: str,
        num_personas: int,
        notas: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crea una nueva reserva en el sistema
        
        Args:
            nombre_cliente: Nombre completo del cliente
            telefono_cliente: Teléfono (9-15 dígitos)
            email_cliente: Email válido
            fecha_reserva: Fecha y hora en formato YYYY-MM-DDTHH:mm
            num_personas: Número de personas (1-20)
            notas: Notas adicionales opcionales
            
        Returns:
            Información de la reserva creada con el token
        """
        try:
            data = {
                "nombre_cliente": nombre_cliente,
                "telefono_cliente": telefono_cliente,
                "email_cliente": email_cliente,
                "fecha_reserva": fecha_reserva,
                "num_personas": num_personas
            }
            
            if notas:
                data["notas"] = notas
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{self.api_url}/reservas",
                    json=data
                )
                
                if response.status_code == 201:
                    result = response.json()
                    return {
                        "success": True,
                        "reserva": result.get('reserva'),
                        "token": result.get('token'),
                        "mensaje": "Reserva creada exitosamente. Se ha enviado un email con el token de confirmación."
                    }
                else:
                    error_data = response.json()
                    return {
                        "success": False,
                        "error": error_data.get('error', 'Error al crear la reserva')
                    }
                    
        except Exception as e:
            return {"success": False, "error": f"Error al crear reserva: {str(e)}"}
    
    async def modificar_fecha_reserva(
        self,
        token: str,
        nueva_fecha: str
    ) -> Dict[str, Any]:
        """
        Modifica la fecha de una reserva existente
        
        Args:
            token: Token de la reserva
            nueva_fecha: Nueva fecha y hora en formato YYYY-MM-DDTHH:mm
            
        Returns:
            Confirmación de la modificación
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Modificar fecha usando el token directamente
                response = await client.patch(
                    f"{self.api_url}/reservas/token/{token}/fecha",
                    json={"fecha_reserva": nueva_fecha}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "reserva": result,
                        "mensaje": "Fecha de reserva modificada exitosamente"
                    }
                else:
                    error_data = response.json()
                    return {
                        "success": False,
                        "error": error_data.get('error', 'Error al modificar fecha')
                    }
                    
        except Exception as e:
            return {"success": False, "error": f"Error al modificar fecha: {str(e)}"}
    
    async def cancelar_reserva(self, token: str) -> Dict[str, Any]:
        """
        Cancela una reserva existente
        
        Args:
            token: Token de la reserva a cancelar
            
        Returns:
            Confirmación de la cancelación
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Cancelar reserva usando el token directamente
                response = await client.post(
                    f"{self.api_url}/reservas/token/{token}/cancelar"
                )
                
                if response.status_code == 200:
                    return {
                        "success": True,
                        "mensaje": "Reserva cancelada exitosamente"
                    }
                elif response.status_code == 404:
                    return {
                        "success": False,
                        "error": "Token de reserva no encontrado o inválido"
                    }
                else:
                    error_data = response.json()
                    return {
                        "success": False,
                        "error": error_data.get('error', 'Error al cancelar reserva')
                    }
                    
        except Exception as e:
            return {"success": False, "error": f"Error al cancelar reserva: {str(e)}"}
    
    async def consultar_reserva(self, token: str) -> Dict[str, Any]:
        """
        Consulta el estado de una reserva
        
        Args:
            token: Token de la reserva
            
        Returns:
            Información completa de la reserva
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_url}/reservas/token/{token}")
                
                if response.status_code == 200:
                    reserva = response.json()
                    return {
                        "success": True,
                        "reserva": reserva
                    }
                else:
                    return {
                        "success": False,
                        "error": "Reserva no encontrada con ese token"
                    }
                    
        except Exception as e:
            return {"success": False, "error": f"Error al consultar reserva: {str(e)}"}
    
    async def listar_menus_disponibles(self) -> Dict[str, Any]:
        """
        Lista todos los menús disponibles
        
        Returns:
            Lista de menús disponibles
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_url}/menus")
                response.raise_for_status()
                menus = response.json()
                
                # Filtrar solo disponibles
                menus_disponibles = [m for m in menus if m.get('disponible', False)]
                
                return {
                    "success": True,
                    "menus": menus_disponibles,
                    "total": len(menus_disponibles)
                }
                
        except Exception as e:
            return {"error": f"Error al listar menús: {str(e)}"}

# Definición de tools para el agente
TOOLS_DEFINITIONS = [
    {
        "name": "get_menu_mas_valorado",
        "description": "Obtiene el menú con la mejor valoración promedio del restaurante. Úsalo cuando el cliente pregunte por el menú más popular, mejor valorado o recomendado.",
        "parameters": {}
    },
    {
        "name": "crear_reserva",
        "description": "Crea una nueva reserva en el sistema. IMPORTANTE: Solo usar cuando el cliente proporcione TODOS los datos requeridos (nombre, teléfono, email, fecha/hora, número de personas). La fecha debe estar en formato YYYY-MM-DDTHH:mm (ej: 2025-11-25T19:30). El horario debe ser entre 9:00 y 23:00.",
        "parameters": {
            "type": "object",
            "properties": {
                "nombre_cliente": {
                    "type": "string",
                    "description": "Nombre completo del cliente"
                },
                "telefono_cliente": {
                    "type": "string",
                    "description": "Teléfono del cliente (9-15 dígitos, puede incluir +)"
                },
                "email_cliente": {
                    "type": "string",
                    "description": "Email válido del cliente"
                },
                "fecha_reserva": {
                    "type": "string",
                    "description": "Fecha y hora de la reserva en formato YYYY-MM-DDTHH:mm"
                },
                "num_personas": {
                    "type": "integer",
                    "description": "Número de personas (entre 1 y 20)"
                },
                "notas": {
                    "type": "string",
                    "description": "Notas o comentarios adicionales (opcional)"
                }
            },
            "required": ["nombre_cliente", "telefono_cliente", "email_cliente", "fecha_reserva", "num_personas"]
        }
    },
    {
        "name": "modificar_fecha_reserva",
        "description": "Modifica la fecha y hora de una reserva existente. Requiere el token de la reserva y la nueva fecha. La reserva debe estar en estado 'confirmada'.",
        "parameters": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "Token único de la reserva"
                },
                "nueva_fecha": {
                    "type": "string",
                    "description": "Nueva fecha y hora en formato YYYY-MM-DDTHH:mm"
                }
            },
            "required": ["token", "nueva_fecha"]
        }
    },
    {
        "name": "cancelar_reserva",
        "description": "Cancela una reserva existente. Requiere el token de la reserva. Esta acción no se puede deshacer.",
        "parameters": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "Token único de la reserva a cancelar"
                }
            },
            "required": ["token"]
        }
    },
    {
        "name": "consultar_reserva",
        "description": "Consulta el estado actual de una reserva usando su token. Devuelve toda la información de la reserva incluyendo estado, fecha, cliente, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "Token único de la reserva"
                }
            },
            "required": ["token"]
        }
    },
    {
        "name": "listar_menus_disponibles",
        "description": "Lista todos los menús disponibles en el restaurante con sus precios, descripciones y valoraciones.",
        "parameters": {}
    }
]

# Instancia global de las herramientas
restaurante_tools = RestauranteTools()
