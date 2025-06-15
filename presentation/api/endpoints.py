from fastapi import APIRouter, Depends
from application.use_cases import GetDomainOsintUseCase
from domain.entities import DomainInfo
from .models import ScanRequest, DomainInfoResponse

def get_use_case_dependency(use_case: GetDomainOsintUseCase):
    def _get_use_case():
        return use_case
    return _get_use_case


def create_api_router(use_case_dependency) -> APIRouter:
    router = APIRouter()
    
    @router.post("/scan", response_model=DomainInfoResponse)
    def scan_domain(
        request: ScanRequest,
        use_case: GetDomainOsintUseCase = Depends(use_case_dependency) # Usa la dependencia directamente
    ):
        domain_info: DomainInfo = use_case.execute(request.domain_name)
        return domain_info

    return router