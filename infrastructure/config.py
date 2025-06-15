import json
from typing import Dict, Any

def load_config(path: str = "config.json") -> Dict[str, Any]:
    """Carga la configuración desde un archivo JSON."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo de configuración '{path}' no fue encontrado.")
        return {} 