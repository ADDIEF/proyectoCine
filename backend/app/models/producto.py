from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum

class TamanoProducto(str, Enum):
    pequeno = "pequeño"
    mediano = "mediano"
    grande = "grande"

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)  # Validación implícita para stock no negativo
    imagen_url = Column(String, nullable=True)  # URL de la imagen del producto
    tamaño = Column(String, nullable=False)  # Usamos el Enum de tamaños

    # Relación con la tabla Venta (esto dependerá de cómo quieras asociar productos a ventas)
    ventas = relationship("Venta", back_populates="producto")

