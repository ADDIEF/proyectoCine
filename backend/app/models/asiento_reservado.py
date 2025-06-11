from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum

class EstadoAsiento(str, Enum):
    reservado = "reservado"
    confirmado = "confirmado"
    cancelado = "cancelado"

class AsientoReservado(Base):
    __tablename__ = "asientos_reservados"

    id = Column(Integer, primary_key=True, index=True)
    funcion_id = Column(Integer, ForeignKey("funciones.id"), nullable=False)
    asiento = Column(String, nullable=False)  # Ej: "B4"
    estado = Column(String, default=EstadoAsiento.reservado, nullable=False)  # Usar el Enum

    # Relación bidireccional con la función
    funcion = relationship("Funcion", back_populates="asientos_reservados")

