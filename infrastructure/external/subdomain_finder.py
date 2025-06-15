from typing import List
from application.interfaces import ISubdomainFinder

class MockSubdomainFinder(ISubdomainFinder):
    """Implementación de ejemplo que devuelve una lista fija de subdominios."""
    def find_subdomains(self, domain_name: str) -> List[str]:
        print("ADVERTENCIA: Usando buscador de subdominios de ejemplo (Mock).")
        if "google.com" in domain_name:
            return ["mail.google.com", "drive.google.com", "calendar.google.com"]
        return [f"www.{domain_name}", f"api.{domain_name}", f"dev.{domain_name}"]