from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/asientos_reservados",
    tags=["Asientos Reservados"]
)

# Crear un asiento reservado
@router.post("/", response_model=schemas.AsientoReservadoResponse)
def create_asiento_reservado(asiento: schemas.AsientoReservadoCreate, db: Session = Depends(get_db)):
    db_asiento = db.query(models.AsientoReservado).filter(models.AsientoReservado.funcion_id == asiento.funcion_id, models.AsientoReservado.asiento == asiento.asiento).first()
    if db_asiento:
        raise HTTPException(status_code=400, detail="Asiento ya reservado")
    
    new_asiento = models.AsientoReservado(**asiento.dict())
    db.add(new_asiento)
    db.commit()
    db.refresh(new_asiento)
    return new_asiento

# Listar todos los asientos reservados
@router.get("/", response_model=List[schemas.AsientoReservadoResponse])
def get_asientos_reservados(db: Session = Depends(get_db)):
    asientos = db.query(models.AsientoReservado).all()
    return asientos

# Obtener un asiento reservado por ID
@router.get("/{asiento_id}", response_model=schemas.AsientoReservadoResponse)
def get_asiento_reservado(asiento_id: int, db: Session = Depends(get_db)):
    asiento = db.query(models.AsientoReservado).filter(models.AsientoReservado.id == asiento_id).first()
    if not asiento:
        raise HTTPException(status_code=404, detail="Asiento reservado no encontrado")
    return asiento

# Actualizar un asiento reservado
@router.put("/{asiento_id}", response_model=schemas.AsientoReservadoResponse)
def update_asiento_reservado(asiento_id: int, asiento: schemas.AsientoReservadoCreate, db: Session = Depends(get_db)):
    db_asiento = db.query(models.AsientoReservado).filter(models.AsientoReservado.id == asiento_id).first()
    if not db_asiento:
        raise HTTPException(status_code=404, detail="Asiento reservado no encontrado")
    
    for key, value in asiento.dict().items():
        setattr(db_asiento, key, value)
    
    db.commit()
    db.refresh(db_asiento)
    return db_asiento

# Eliminar un asiento reservado
@router.delete("/{asiento_id}", status_code=204)
def delete_asiento_reservado(asiento_id: int, db: Session = Depends(get_db)):
    db_asiento = db.query(models.AsientoReservado).filter(models.AsientoReservado.id == asiento_id).first()
    if not db_asiento:
        raise HTTPException(status_code=404, detail="Asiento reservado no encontrado")
    
    db.delete(db_asiento)
    db.commit()
    return {"detail": "Asiento reservado eliminado"}
