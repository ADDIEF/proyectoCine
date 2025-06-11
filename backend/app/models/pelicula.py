from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Pelicula(Base):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    idioma = Column(String, nullable=False)
    duracion = Column(Integer, nullable=False)  # en minutos
    clasificacion = Column(String, nullable=False)
    sinopsis = Column(Text, nullable=True)
    poster_url = Column(String, nullable=True)
    trailer_url = Column(String, nullable=True)

    funciones = relationship("Funcion", back_populates="pelicula", cascade="all, delete")