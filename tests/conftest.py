"""Configuración del entorno de pruebas."""
import os
import sys

# Agregar el directorio raíz al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 