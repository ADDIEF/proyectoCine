from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # Cambiar 'users' por 'usuarios'
    funcion_id = Column(Integer, ForeignKey("funciones.id"), nullable=False)  # Referencia a la función
    asiento_reservado = Column(String, nullable=False)  # Ej: "A1", "B4"
    estado = Column(String, default="reservado")  # Estado de la reserva (reservado, confirmado)
    fecha_reserva = Column(DateTime, default=datetime.utcnow)  # Fecha de la reserva
    
    # Relación con los detalles de la reserva
    detalles_reserva = relationship("DetalleReserva", back_populates="reserva")
    usuario = relationship("User", back_populates="reservas")  # Relación con el usuario
    funcion = relationship("Funcion", back_populates="reservas")  # Relación con la función
