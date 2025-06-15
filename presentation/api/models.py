from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ScanRequest(BaseModel):
    domain_name: str = Field(...)

class DomainInfoResponse(BaseModel):
    domain_name: str
    whois_data: Optional[Dict[str, Any]] = None
    subdomains: List[str] = []

    class Config:
        orm_mode = True 