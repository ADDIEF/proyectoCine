from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class Sala(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)  # normal, vip, etc.
    zona_precio = Column(JSON, nullable=True)  # Ej: {"vip": 50, "normal": 30}
    funciones = relationship("Funcion", back_populates="sala", cascade="all, delete")
