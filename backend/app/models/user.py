from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class RolUsuario(str, enum.Enum):
    visitante = "visitante"
    registrado = "registrado"
    admin = "admin"

class User(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    contraseña = Column(String, nullable=False)
    rol = Column(Enum(RolUsuario), default="registrado")

    # Usamos cadenas de texto para evitar problemas con el orden de definición de clases
    reservas = relationship("Reserva", back_populates="usuario")
    ventas = relationship("Venta", back_populates="usuario")  # Aquí usamos la cadena "Venta"
    facturas = relationship("Factura", back_populates="usuario")




    
    
    
    