from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)

# Crear una nueva factura
@router.post("/", response_model=schemas.FacturaResponse)
def create_factura(factura: schemas.FacturaCreate, db: Session = Depends(get_db)):
    db_factura = db.query(models.Factura).filter(models.Factura.venta_id == factura.venta_id).first()
    if db_factura:
        raise HTTPException(status_code=400, detail="Factura ya registrada para esta venta")
    
    new_factura = models.Factura(**factura.dict())
    db.add(new_factura)
    db.commit()
    db.refresh(new_factura)
    return new_factura

# Listar todas las facturas
@router.get("/", response_model=List[schemas.FacturaResponse])
def get_facturas(db: Session = Depends(get_db)):
    facturas = db.query(models.Factura).all()
    return facturas

# Obtener una factura por ID
@router.get("/{factura_id}", response_model=schemas.FacturaResponse)
def get_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

# Actualizar una factura
@router.put("/{factura_id}", response_model=schemas.FacturaResponse)
def update_factura(factura_id: int, factura: schemas.FacturaCreate, db: Session = Depends(get_db)):
    db_factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not db_factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    for key, value in factura.dict().items():
        setattr(db_factura, key, value)
    
    db.commit()
    db.refresh(db_factura)
    return db_factura

# Eliminar una factura
@router.delete("/{factura_id}", status_code=204)
def delete_factura(factura_id: int, db: Session = Depends(get_db)):
    db_factura = db.query(models.Factura).filter(models.Factura.id == factura_id).first()
    if not db_factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    
    db.delete(db_factura)
    db.commit()
    return {"detail": "Factura eliminada"}
