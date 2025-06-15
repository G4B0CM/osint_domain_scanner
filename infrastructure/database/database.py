from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from infrastructure.config import load_config

config = load_config()
SQLALCHEMY_DATABASE_URL = config.get("database", {}).get("connection_string")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("No se encontró 'connection_string' en config.json")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Función para crear las tablas en la base de datos
def init_db():
    Base.metadata.create_all(bind=engine)