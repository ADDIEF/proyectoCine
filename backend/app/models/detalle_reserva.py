from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from enum import Enum

class TipoDetalleReserva(str, Enum):
    entrada = "entrada"
    producto = "producto"

class DetalleReserva(Base):
    __tablename__ = "detalles_reserva"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False)  # Relación con Reserva
    tipo = Column(String, nullable=False)  # 'entrada' o 'producto', podemos usar Enum
    descripcion = Column(String, nullable=False)  # Descripción del producto o tipo de entrada
    monto = Column(Float, nullable=False)  # Monto de la entrada o producto

    # Relación con la tabla 'Reserva'
    reserva = relationship("Reserva", back_populates="detalles_reserva")
