import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

# 1. Importaciones de las capas
from application.use_cases import GetDomainOsintUseCase
from infrastructure.external.whois_provider import WhoisProvider
from infrastructure.external.subdomain_finder import MockSubdomainFinder
from infrastructure.config import load_config
from infrastructure.database.database import SessionLocal, init_db
from infrastructure.database.sql_repository import SQLDomainInfoRepository
from presentation.api.endpoints import create_api_router

# 2. Cargar configuración
config = load_config()

# 3. Inicializar la aplicación FastAPI
app = FastAPI(
    title="OSINT Domain Scanner API",
    description="Un microservicio para obtener información pública de dominios web.",
    version="1.0.0"
)

# Evento de startup para crear las tablas de la DB si no existen
@app.on_event("startup")
def on_startup():
    print("Inicializando base de datos...")
    init_db()
    print("Base de datos inicializada.")

# Función para obtener una sesión de base de datos por petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 4. Inyección de Dependencias
whois_provider_instance = WhoisProvider()
subdomain_finder_instance = MockSubdomainFinder()

# Ahora, el caso de uso se construye dentro de la petición
# para que pueda recibir una sesión de DB fresca.
def get_domain_osint_use_case(db: Session = Depends(get_db)):
    sql_repository = SQLDomainInfoRepository(session=db)
    return GetDomainOsintUseCase(
        whois_provider=whois_provider_instance,
        subdomain_finder=subdomain_finder_instance,
        domain_repository=sql_repository # Inyectamos el repo SQL
    )

# 5. Crear y registrar el router de la API
# Modificamos la creación del router para que maneje la nueva dependencia
# Esta es una forma común en FastAPI de inyectar dependencias por petición
api_router = create_api_router(get_domain_osint_use_case)
app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)