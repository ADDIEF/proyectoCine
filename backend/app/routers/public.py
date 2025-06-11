from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.pelicula import Pelicula
from app import schemas

router = APIRouter(
    prefix="/publico",
    tags=["Público"]
)

@router.get("/cartelera", response_model=list[schemas.PeliculaOut])
def listar_cartelera(db: Session = Depends(get_db)):
    peliculas = db.query(Pelicula).all()
    return peliculas
