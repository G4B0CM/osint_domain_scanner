import json
import os
from typing import Dict, Any

def load_config() -> Dict[str, Any]:
    """
    Carga la configuración priorizando variables de entorno sobre el archivo config.json.
    """

    config = {
        "database": {
            "connection_string": os.getenv("DB_CONNECTION_STRING")
        },
        "user_agent": os.getenv("USER_AGENT", "DefaultAgent/1.0")
    }

    if not config["database"]["connection_string"]:
        print("ADVERTENCIA: No se encontró DB_CONNECTION_STRING en las variables de entorno. Usando config.json como fallback.")
        try:
            with open("config.json", 'r') as f:
                file_config = json.load(f)
                for key, value in file_config.items():
                    if key not in config or not config[key]:
                        config[key] = value
        except FileNotFoundError:
            print("Error: No se encontró ni variable de entorno DB_CONNECTION_STRING ni archivo config.json.")
            
    return config