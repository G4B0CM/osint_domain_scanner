from sqlalchemy import Column, Integer, String, DateTime, JSON
from .database import Base

class DomainInfoDB(Base):
    __tablename__ = "domain_scans"

    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String, index=True, nullable=False)
    scanned_at = Column(DateTime, nullable=False)
    whois_data = Column(JSON) # JSON es soportado por muchos dialectos de SQL
    subdomains = Column(String) # Guardaremos la lista como un string separado por comas