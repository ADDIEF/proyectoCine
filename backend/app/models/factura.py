from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"), nullable=False)  # Referencia a la venta
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)  # Referencia al usuario
    monto_total = Column(Float, nullable=False)  # Monto total de la factura
    fecha_emision = Column(DateTime, default=datetime.utcnow)  # Fecha de emisión de la factura

    # Relación con la venta
    venta = relationship("Venta", back_populates="factura", uselist=False)

    # Relación con el usuario
    usuario = relationship("User", back_populates="facturas")