from sqlalchemy import Column, Integer, String, Date
from app.database import Base

class Promocion(Base):
    __tablename__ = "promociones"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)  # Descripción añadida
    descuento = Column(Integer, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
