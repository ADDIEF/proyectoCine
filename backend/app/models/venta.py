from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # Referencia al usuario
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=True)  # Referencia a los productos (opcional)
    funcion_id = Column(Integer, ForeignKey("funciones.id"), nullable=True)  # Referencia a la función (opcional)
    monto_total = Column(Float, nullable=False)  # Monto total de la venta

    # Relación con el modelo de Usuario (usando cadena de texto)
    usuario = relationship("User", back_populates="ventas")

    # Relación con el modelo de Producto (usando cadena de texto)
    producto = relationship("Producto", back_populates="ventas")

    # Relación con el modelo de Funcion (usando cadena de texto)
    funcion = relationship("Funcion", back_populates="ventas")

    # Relación con la factura
    factura = relationship("Factura", back_populates="venta", uselist=False)  # Asegúrate que "Factura" está bien definida aquí