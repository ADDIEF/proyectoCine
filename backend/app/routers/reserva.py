from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/reservas",
    tags=["Reservas"]
)

# Crear una nueva reserva
@router.post("/", response_model=schemas.ReservaResponse)
def create_reserva(reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.funcion_id == reserva.funcion_id, models.Reserva.asiento_reservado == reserva.asiento_reservado).first()
    if db_reserva:
        raise HTTPException(status_code=400, detail="Asiento ya reservado para esta función")
    
    new_reserva = models.Reserva(**reserva.dict())
    db.add(new_reserva)
    db.commit()
    db.refresh(new_reserva)
    return new_reserva

# Listar todas las reservas
@router.get("/", response_model=List[schemas.ReservaResponse])
def get_reservas(db: Session = Depends(get_db)):
    reservas = db.query(models.Reserva).all()
    return reservas

# Obtener una reserva por ID
@router.get("/{reserva_id}", response_model=schemas.ReservaResponse)
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

# Actualizar una reserva
@router.put("/{reserva_id}", response_model=schemas.ReservaResponse)
def update_reserva(reserva_id: int, reserva: schemas.ReservaCreate, db: Session = Depends(get_db)):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    for key, value in reserva.dict().items():
        setattr(db_reserva, key, value)
    
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

# Eliminar una reserva
@router.delete("/{reserva_id}", status_code=204)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    db_reserva = db.query(models.Reserva).filter(models.Reserva.id == reserva_id).first()
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    db.delete(db_reserva)
    db.commit()
    return {"detail": "Reserva eliminada"}
