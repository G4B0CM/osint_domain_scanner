from typing import Optional
from sqlalchemy.orm import Session
from application.interfaces import IDomainInfoRepository
from domain.entities import DomainInfo
from .models import DomainInfoDB

class SQLDomainInfoRepository(IDomainInfoRepository):
    """Implementación concreta del repositorio para SQL Server usando SQLAlchemy."""
    def __init__(self, session: Session):
        self.session = session

    def save(self, domain_info: DomainInfo) -> DomainInfo:
        # Mapeo de la entidad de dominio al modelo de la DB
        subdomains_str = ",".join(domain_info.subdomains)
        
        db_model = DomainInfoDB(
            domain_name=domain_info.domain_name,
            scanned_at=domain_info.scanned_at,
            whois_data=domain_info.whois_data,
            subdomains=subdomains_str
        )
        
        self.session.add(db_model)
        self.session.commit()
        self.session.refresh(db_model)

        # Mapeo de vuelta a la entidad de dominio, ahora con el ID asignado por la DB
        domain_info.id = getattr(db_model, "id", None)
        return domain_info

    def find_by_domain_name(self, domain_name: str) -> Optional[DomainInfo]:
        db_model = self.session.query(DomainInfoDB).filter(DomainInfoDB.domain_name == domain_name).first()
        
        if not db_model:
            return None
        
        # Mapeo del modelo de la DB a la entidad de dominio
        subdomains_list = db_model.subdomains.split(',') if getattr(db_model, "subdomains", None) else []
        
        return DomainInfo(
            id= getattr(db_model, "id", None),
            domain_name= getattr(db_model, "domain_name"),
            scanned_at= getattr(db_model, "scanned_at"),
            whois_data=getattr(db_model, "whois_data", None),
            subdomains=subdomains_list
        )