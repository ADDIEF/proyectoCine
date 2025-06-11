from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)

# Crear una nueva venta
@router.post("/", response_model=schemas.VentaResponse)
def create_venta(venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    new_venta = models.Venta(**venta.dict())
    db.add(new_venta)
    db.commit()
    db.refresh(new_venta)
    return new_venta

# Listar todas las ventas
@router.get("/", response_model=List[schemas.VentaResponse])
def get_ventas(db: Session = Depends(get_db)):
    ventas = db.query(models.Venta).all()
    return ventas

# Obtener una venta por ID
@router.get("/{venta_id}", response_model=schemas.VentaResponse)
def get_venta(venta_id: int, db: Session = Depends(get_db)):
    venta = db.query(models.Venta).filter(models.Venta.id == venta_id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

# Actualizar una venta
@router.put("/{venta_id}", response_model=schemas.VentaResponse)
def update_venta(venta_id: int, venta: schemas.VentaCreate, db: Session = Depends(get_db)):
    db_venta = db.query(models.Venta).filter(models.Venta.id == venta_id).first()
    if not db_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    for key, value in venta.dict().items():
        setattr(db_venta, key, value)
    
    db.commit()
    db.refresh(db_venta)
    return db_venta

# Eliminar una venta
@router.delete("/{venta_id}", status_code=204)
def delete_venta(venta_id: int, db: Session = Depends(get_db)):
    db_venta = db.query(models.Venta).filter(models.Venta.id == venta_id).first()
    if not db_venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    db.delete(db_venta)
    db.commit()
    return {"detail": "Venta eliminada"}
