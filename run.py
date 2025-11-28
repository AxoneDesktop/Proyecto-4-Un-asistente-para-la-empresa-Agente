#!/usr/bin/env python
"""
Script de arranque del Sistema Multi-Agente
Ejecutar desde la raíz del proyecto: python run.py
"""
import sys
import os

# Obtener directorio raíz del proyecto
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, 'src')

# Cambiar al directorio src para que los imports funcionen
os.chdir(SRC_DIR)
sys.path.insert(0, '.')

if __name__ == "__main__":
    import uvicorn
    from dotenv import load_dotenv
    
    # Cargar .env desde la raíz del proyecto
    load_dotenv(os.path.join(ROOT_DIR, '.env'))
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print("=" * 60)
    print("🚀 SISTEMA MULTI-AGENTE IA - RESTAURANTE")
    print("=" * 60)
    print(f"🤖 Iniciando en {host}:{port}")
    print("=" * 60)
    
    uvicorn.run("main:app", host=host, port=port, reload=True)
