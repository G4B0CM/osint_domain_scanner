from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

@dataclass
class DomainInfo:
    """
    Entidad del dominio. Ahora incluye un ID y una fecha de escaneo
    para facilitar su seguimiento en la base de datos.
    """
    domain_name: str
    whois_data: Optional[Dict[str, Any]] = None
    subdomains: List[str] = field(default_factory=list)
    
    # Campos para persistencia
    id: Optional[int] = None
    scanned_at: datetime = field(default_factory=datetime.utcnow)