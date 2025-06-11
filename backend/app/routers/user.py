from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database, schemas
from app.models.user import User
from app.utils import hash_password, verify_password
from app.auth import get_db, crear_token, get_current_user, verificar_admin

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/register")
def register_user(usuario: schemas.UserCreate, db: Session = Depends(get_db)):
    existe = db.query(User).filter(User.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    nuevo_usuario = User(
        nombre=usuario.nombre,
        email=usuario.email,
        contraseña=hash_password(usuario.contraseña),
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"mensaje": "Usuario registrado correctamente", "id": nuevo_usuario.id}

@router.post("/login")
def login_usuario(datos: schemas.UserLogin, db: Session = Depends(get_db)):
    usuario = db.query(User).filter(User.email == datos.email).first()
    if not usuario or not verify_password(datos.contraseña, usuario.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = crear_token({"sub": str(usuario.id), "rol": usuario.rol})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/perfil")
def ver_perfil(usuario=Depends(get_current_user)):
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "email": usuario.email,
        "rol": usuario.rol
    }
