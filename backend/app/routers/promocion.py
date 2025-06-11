from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/promociones",
    tags=["Promociones"]
)

# Crear una nueva promoción
@router.post("/", response_model=schemas.PromocionResponse)
def create_promocion(promocion: schemas.PromocionCreate, db: Session = Depends(get_db)):
    db_promocion = db.query(models.Promocion).filter(models.Promocion.codigo == promocion.codigo).first()
    if db_promocion:
        raise HTTPException(status_code=400, detail="Código de promoción ya registrado")
    
    new_promocion = models.Promocion(**promocion.dict())
    db.add(new_promocion)
    db.commit()
    db.refresh(new_promocion)
    return new_promocion

# Listar todas las promociones
@router.get("/", response_model=List[schemas.PromocionResponse])
def get_promociones(db: Session = Depends(get_db)):
    promociones = db.query(models.Promocion).all()
    return promociones

# Obtener una promoción por ID
@router.get("/{promocion_id}", response_model=schemas.PromocionResponse)
def get_promocion(promocion_id: int, db: Session = Depends(get_db)):
    promocion = db.query(models.Promocion).filter(models.Promocion.id == promocion_id).first()
    if not promocion:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")
    return promocion

# Actualizar una promoción
@router.put("/{promocion_id}", response_model=schemas.PromocionResponse)
def update_promocion(promocion_id: int, promocion: schemas.PromocionCreate, db: Session = Depends(get_db)):
    db_promocion = db.query(models.Promocion).filter(models.Promocion.id == promocion_id).first()
    if not db_promocion:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")
    
    # Actualizamos todos los campos de la promoción si fueron enviados
    if promocion.codigo:
        db_promocion.codigo = promocion.codigo
    if promocion.descripcion:
        db_promocion.descripcion = promocion.descripcion
    if promocion.descuento:
        db_promocion.descuento = promocion.descuento
    if promocion.fecha_inicio:
        db_promocion.fecha_inicio = promocion.fecha_inicio
    if promocion.fecha_fin:
        db_promocion.fecha_fin = promocion.fecha_fin
    
    db.commit()
    db.refresh(db_promocion)
    return db_promocion


# Eliminar una promoción
@router.delete("/{promocion_id}", status_code=204)
def delete_promocion(promocion_id: int, db: Session = Depends(get_db)):
    db_promocion = db.query(models.Promocion).filter(models.Promocion.id == promocion_id).first()
    if not db_promocion:
        raise HTTPException(status_code=404, detail="Promoción no encontrada")
    
    db.delete(db_promocion)
    db.commit()
    return {"detail": "Promoción eliminada"}
