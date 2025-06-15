import whois
from typing import Optional, Dict, Any
from application.interfaces import IWhoisProvider
from datetime import datetime # Importar datetime

def convert_to_json_serializable(data: Any) -> Any:
    if isinstance(data, datetime):
        return data.isoformat()
    if isinstance(data, list):
        return [convert_to_json_serializable(item) for item in data]
    return data

class WhoisProvider(IWhoisProvider):
    def get_whois_data(self, domain_name: str) -> Optional[Dict[str, Any]]:
        try:
            w = whois.whois(domain_name)
            
            if not (w and w.domain_name):
                return None

            serializable_data = {}
            for key, val in w.items():
                serializable_data[key] = convert_to_json_serializable(val)
            
            return serializable_data

        except Exception as e:
            print(f"Error al obtener WHOIS para {domain_name}: {e}")
            return None