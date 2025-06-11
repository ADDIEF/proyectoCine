from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.database import SessionLocal
from app.models.user import User
from typing import Dict

# Configuración JWT
SECRET_KEY = "proyecto_cine_super_seguro_123"
ALGORITHM = "HS256"
EXPIRACION_MINUTOS = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")
def crear_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)  # El token expira en 1 hora
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def verificar_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verificar_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    user_id = int(payload.get("sub"))
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return usuario

def verificar_admin(usuario: User = Depends(get_current_user)):
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado (solo administradores)")
    return usuario
