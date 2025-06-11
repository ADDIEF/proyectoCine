from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/salas",
    tags=["Salas"]
)

@router.post("/", response_model=schemas.SalaResponse)
def crear_sala(sala: schemas.SalaCreate, db: Session = Depends(get_db)):
    db_sala = models.Sala(**sala.dict())
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala

@router.get("/", response_model=list[schemas.SalaResponse])
def listar_salas(db: Session = Depends(get_db)):
    return db.query(models.Sala).all()

@router.get("/{sala_id}", response_model=schemas.SalaResponse)
def obtener_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).filter(models.Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    return sala

@router.put("/{sala_id}", response_model=schemas.SalaResponse)
def actualizar_sala(sala_id: int, datos: schemas.SalaCreate, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).filter(models.Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    for key, value in datos.dict().items():
        setattr(sala, key, value)
    db.commit()
    db.refresh(sala)
    return sala

@router.delete("/{sala_id}")
def eliminar_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.query(models.Sala).filter(models.Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    db.delete(sala)
    db.commit()
    return {"mensaje": "Sala eliminada"}
