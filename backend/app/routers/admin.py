from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/zona-secreta")
def admin_area(usuario: User = Depends(get_current_user)):
    if usuario.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso solo para administradores")
    return {"mensaje": f"Bienvenido, administrador {usuario.nombre}"}
