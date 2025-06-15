from domain.entities import DomainInfo
from .interfaces import IWhoisProvider, ISubdomainFinder, IDomainInfoRepository

class GetDomainOsintUseCase:
    """
    Caso de uso actualizado. Ahora también es responsable de persistir
    el resultado del escaneo utilizando el repositorio.
    """
    def __init__(
        self,
        whois_provider: IWhoisProvider,
        subdomain_finder: ISubdomainFinder,
        domain_repository: IDomainInfoRepository  # Nueva dependencia
    ):
        self.whois_provider = whois_provider
        self.subdomain_finder = subdomain_finder
        self.domain_repository = domain_repository

    def execute(self, domain_name: str) -> DomainInfo:
        # Lógica de negocio: obtener datos OSINT.
        print(f"Executing OSINT scan for: {domain_name}")
        whois_data = self.whois_provider.get_whois_data(domain_name)
        subdomains = self.subdomain_finder.find_subdomains(domain_name)

        domain_info = DomainInfo(
            domain_name=domain_name,
            whois_data=whois_data,
            subdomains=subdomains
        )

        # Nueva responsabilidad: guardar el resultado.
        print(f"Saving scan results for {domain_name} to the repository.")
        saved_domain_info = self.domain_repository.save(domain_info)

        return saved_domain_info