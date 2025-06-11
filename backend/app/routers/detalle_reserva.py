from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/detalles_reserva",
    tags=["Detalles de Reserva"]
)

# Crear un detalle de reserva
@router.post("/", response_model=schemas.DetalleReservaResponse)
def create_detalle_reserva(detalle: schemas.DetalleReservaCreate, db: Session = Depends(get_db)):
    db_detalle = db.query(models.DetalleReserva).filter(models.DetalleReserva.reserva_id == detalle.reserva_id, models.DetalleReserva.tipo == detalle.tipo, models.DetalleReserva.descripcion == detalle.descripcion).first()
    if db_detalle:
        raise HTTPException(status_code=400, detail="Detalle de reserva ya existe")
    
    new_detalle = models.DetalleReserva(**detalle.dict())
    db.add(new_detalle)
    db.commit()
    db.refresh(new_detalle)
    return new_detalle

# Listar todos los detalles de reserva
@router.get("/", response_model=List[schemas.DetalleReservaResponse])
def get_detalles_reserva(db: Session = Depends(get_db)):
    detalles = db.query(models.DetalleReserva).all()
    return detalles

# Obtener un detalle de reserva por ID
@router.get("/{detalle_id}", response_model=schemas.DetalleReservaResponse)
def get_detalle_reserva(detalle_id: int, db: Session = Depends(get_db)):
    detalle = db.query(models.DetalleReserva).filter(models.DetalleReserva.id == detalle_id).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    return detalle

# Actualizar un detalle de reserva
@router.put("/{detalle_id}", response_model=schemas.DetalleReservaResponse)
def update_detalle_reserva(detalle_id: int, detalle: schemas.DetalleReservaCreate, db: Session = Depends(get_db)):
    db_detalle = db.query(models.DetalleReserva).filter(models.DetalleReserva.id == detalle_id).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    
    for key, value in detalle.dict().items():
        setattr(db_detalle, key, value)
    
    db.commit()
    db.refresh(db_detalle)
    return db_detalle

# Eliminar un detalle de reserva
@router.delete("/{detalle_id}", status_code=204)
def delete_detalle_reserva(detalle_id: int, db: Session = Depends(get_db)):
    db_detalle = db.query(models.DetalleReserva).filter(models.DetalleReserva.id == detalle_id).first()
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de reserva no encontrado")
    
    db.delete(db_detalle)
    db.commit()
    return {"detail": "Detalle de reserva eliminado"}
