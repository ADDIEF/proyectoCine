from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Cargar variables desde .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Crear engine
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()

# Función para obtener la sesión de base de datos en rutas
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

