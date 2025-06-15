import whois
from typing import Optional, Dict, Any
from application.interfaces import IWhoisProvider

class WhoisProvider(IWhoisProvider):
    """Implementación concreta de IWhoisProvider usando la librería python-whois."""
    def get_whois_data(self, domain_name: str) -> Optional[Dict[str, Any]]:
        try:
            w = whois.whois(domain_name)
            # El objeto 'whois' no es directamente serializable a JSON,
            # lo convertimos a un diccionario.
            if w and w.domain_name:
                return {key: val for key, val in w.items()}
            return None
        except Exception as e:
            print(f"Error al obtener WHOIS para {domain_name}: {e}")
            return None