from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from domain.entities import DomainInfo

class IWhoisProvider(ABC):
    @abstractmethod
    def get_whois_data(self, domain_name: str) -> Optional[Dict[str, Any]]:
        pass

class ISubdomainFinder(ABC):
    @abstractmethod
    def find_subdomains(self, domain_name: str) -> List[str]:
        pass

# NUEVA INTERFAZ
class IDomainInfoRepository(ABC):
    """
    Interfaz para la persistencia de la entidad DomainInfo.
    La capa de aplicación no sabe si esto guarda en SQL, un archivo o en memoria.
    """
    @abstractmethod
    def save(self, domain_info: DomainInfo) -> DomainInfo:
        pass

    @abstractmethod
    def find_by_domain_name(self, domain_name: str) -> Optional[DomainInfo]:
        # Útil para, por ejemplo, no volver a escanear un dominio reciente.
        pass