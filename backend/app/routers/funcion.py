from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.dependencies import get_current_user_admin

router = APIRouter(
    prefix="/funciones",
    tags=["Funciones"]
)

@router.post("/", response_model=schemas.FuncionOut, dependencies=[Depends(get_current_user_admin)])
def crear_funcion(funcion: schemas.FuncionCreate, db: Session = Depends(get_db)):
    nueva_funcion = models.Funcion(**funcion.dict())
    db.add(nueva_funcion)
    db.commit()
    db.refresh(nueva_funcion)
    return nueva_funcion

@router.get("/", response_model=List[schemas.FuncionOut])
def listar_funciones(db: Session = Depends(get_db)):
    return db.query(models.Funcion).all()

@router.get("/{funcion_id}", response_model=schemas.FuncionOut)
def obtener_funcion(funcion_id: int, db: Session = Depends(get_db)):
    funcion = db.query(models.Funcion).filter(models.Funcion.id == funcion_id).first()
    if not funcion:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    return funcion

@router.put("/{funcion_id}", response_model=schemas.FuncionOut, dependencies=[Depends(get_current_user_admin)])
def actualizar_funcion(funcion_id: int, datos: schemas.FuncionUpdate, db: Session = Depends(get_db)):
    funcion = db.query(models.Funcion).filter(models.Funcion.id == funcion_id).first()
    if not funcion:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    for key, value in datos.dict().items():
        setattr(funcion, key, value)
    db.commit()
    db.refresh(funcion)
    return funcion

@router.delete("/{funcion_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_user_admin)])
def eliminar_funcion(funcion_id: int, db: Session = Depends(get_db)):
    funcion = db.query(models.Funcion).filter(models.Funcion.id == funcion_id).first()
    if not funcion:
        raise HTTPException(status_code=404, detail="Función no encontrada")
    db.delete(funcion)
    db.commit()
