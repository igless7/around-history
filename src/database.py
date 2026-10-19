from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def get_engine():
    """
    Crea el motor de conexión. 
    Por defecto usa SQLite local, pero basta con cambiar la URL a 'postgresql://...' para usar PostgreSQL.
    """
    return create_engine(DATABASE_URL, echo=False)

def init_db(engine):
    """Crea las tablas físicamente en la Base de Datos si no existen."""
    Base.metadata.create_all(engine)

def get_session_factory(engine):
    """Retorna una fábrica de sesiones ORM."""
    return sessionmaker(bind=engine)