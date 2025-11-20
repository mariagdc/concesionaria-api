from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "DATABASE_URL=postgresql://usuario:/compraventa")

# Motor síncrono para SQLModel
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Crea todas las tablas en la base de datos"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependencia para obtener sesión de base de datos"""
    with Session(engine) as session:
        yield session