"""Servicio de configuración del juego."""
import yaml
import os

# Obtener la ruta del directorio raíz del proyecto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargar configuración
with open(os.path.join(ROOT_DIR, 'config.yaml'), 'r', encoding='utf-8') as f:
    CONFIG = yaml.safe_load(f)