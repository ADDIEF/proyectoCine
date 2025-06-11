from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

# Crear un nuevo producto
@router.post("/", response_model=schemas.ProductoResponse)
def create_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.nombre == producto.nombre).first()
    if db_producto:
        raise HTTPException(status_code=400, detail="Producto ya registrado")
    
    new_producto = models.Producto(**producto.dict())
    db.add(new_producto)
    db.commit()
    db.refresh(new_producto)
    return new_producto

# Listar todos los productos
@router.get("/", response_model=List[schemas.ProductoResponse])
def get_productos(db: Session = Depends(get_db)):
    productos = db.query(models.Producto).all()
    return productos

# Obtener un producto por ID
@router.get("/{producto_id}", response_model=schemas.ProductoResponse)
def get_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# Actualizar un producto
@router.put("/{producto_id}", response_model=schemas.ProductoResponse)
def update_producto(producto_id: int, producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    for key, value in producto.dict().items():
        setattr(db_producto, key, value)
    
    db.commit()
    db.refresh(db_producto)
    return db_producto

# Eliminar un producto
@router.delete("/{producto_id}", status_code=204)
def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(db_producto)
    db.commit()
    return {"detail": "Producto eliminado"}
