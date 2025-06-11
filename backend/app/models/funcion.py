from sqlalchemy import Column, Integer, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from app.database import Base

class Funcion(Base):
    __tablename__ = "funciones"

    id = Column(Integer, primary_key=True, index=True)
    pelicula_id = Column(Integer, ForeignKey("peliculas.id"), nullable=False)
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)

    pelicula = relationship("Pelicula", back_populates="funciones")
    sala = relationship("Sala", back_populates="funciones")
    # Relación con los asientos reservados
    asientos_reservados = relationship("AsientoReservado", back_populates="funcion")
    
    # Relación con las reservas
    reservas = relationship("Reserva", back_populates="funcion")
    # Relación con las ventas
    ventas = relationship("Venta", back_populates="funcion")
    
    
    
    