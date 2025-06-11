from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/peliculas",
    tags=["Películas"]
)

@router.post("/", response_model=schemas.PeliculaResponse)
def crear_pelicula(pelicula: schemas.PeliculaCreate, db: Session = Depends(get_db)):
    db_pelicula = models.Pelicula(**pelicula.dict())
    db.add(db_pelicula)
    db.commit()
    db.refresh(db_pelicula)
    return db_pelicula

@router.get("/", response_model=list[schemas.PeliculaResponse])
def listar_peliculas(db: Session = Depends(get_db)):
    return db.query(models.Pelicula).all()

@router.get("/{pelicula_id}", response_model=schemas.PeliculaResponse)
def obtener_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return pelicula

@router.put("/{pelicula_id}", response_model=schemas.PeliculaResponse)
def actualizar_pelicula(pelicula_id: int, datos: schemas.PeliculaCreate, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    for key, value in datos.dict().items():
        setattr(pelicula, key, value)
    db.commit()
    db.refresh(pelicula)
    return pelicula

@router.delete("/{pelicula_id}")
def eliminar_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(models.Pelicula).filter(models.Pelicula.id == pelicula_id).first()
    if not pelicula:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    db.delete(pelicula)
    db.commit()
    return {"mensaje": "Película eliminada"}
