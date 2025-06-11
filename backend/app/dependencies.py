from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        usuario = db.query(User).filter(User.id == user_id).first()
        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

def get_current_user_admin(current_user: User = Depends(get_current_user)):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return current_user
