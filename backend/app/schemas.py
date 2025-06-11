from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from enum import Enum
from datetime import date, time
from datetime import datetime
from decimal import Decimal
import re

class RolUsuario(str, Enum):
    visitante = "visitante"
    registrado = "registrado"
    admin = "admin"

class UserCreate(BaseModel):
    nombre: str
    email: EmailStr
    contraseña: str = Field(min_length=6)  # Contraseña con una longitud mínima
    rol: RolUsuario = RolUsuario.registrado  # Rol por defecto es "registrado"

    # Usamos @model_validator en lugar de @root_validator
    @model_validator(mode='before')
    def check_password(cls, values):
        password = values.get('contraseña')
        
        # Verificación de contraseña (al menos una mayúscula, un número y un carácter especial)
        if password:
            if len(password) < 6:
                raise ValueError('La contraseña debe tener al menos 6 caracteres')
            if not re.search(r'[A-Z]', password):  # Verifica mayúsculas
                raise ValueError('La contraseña debe tener al menos una letra mayúscula')
            if not re.search(r'[0-9]', password):  # Verifica números
                raise ValueError('La contraseña debe tener al menos un número')
            if not re.search(r'[\W_]', password):  # Verifica caracteres especiales
                raise ValueError('La contraseña debe tener al menos un carácter especial')
        return values

class UserLogin(BaseModel):
    email: EmailStr
    contraseña: str

class UserResponse(BaseModel):
    id: int
    nombre: str
    email: str
    rol: RolUsuario

    class Config:
        orm_mode = True


# ----------------------- PELICULAS -------------------------

class PeliculaBase(BaseModel):
    titulo: str
    genero: str
    idioma: str
    duracion: int
    clasificacion: str
    sinopsis: str | None = None
    poster_url: str | None = None
    trailer_url: str | None = None

class PeliculaOut(PeliculaBase):
    id: int

    class Config:
        orm_mode = True

class PeliculaBase(BaseModel):
    titulo: str
    genero: str
    idioma: str
    duracion: int  # minutos
    clasificacion: str
    sinopsis: str
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None

class PeliculaCreate(PeliculaBase):
    pass

class PeliculaResponse(PeliculaBase):
    id: int

    class Config:
        from_attributes = True
        
# ----------------------- SALA -------------------------
        
class SalaBase(BaseModel):
    nombre: str
    capacidad: int
    tipo: str
    zona_precio: Optional[dict] = None  # JSON → {“vip”: 50, “normal”: 30}

class SalaCreate(SalaBase):
    pass

class SalaResponse(SalaBase):
    id: int

    class Config:
        from_attributes = True


# ----------------------- FUNCION -------------------------

class FuncionBase(BaseModel):
    pelicula_id: int
    sala_id: int
    fecha: date
    hora: time

class FuncionCreate(FuncionBase):
    pass

class FuncionUpdate(FuncionBase):
    pass

class FuncionOut(FuncionBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------- PROMOCION -------------------------

# Base de la promoción
class PromocionBase(BaseModel):
    codigo: str
    descripcion: str | None = None  # Descripción añadida
    descuento: int  # porcentaje de descuento
    fecha_inicio: date
    fecha_fin: date

# Esquema para crear una nueva promoción
class PromocionCreate(PromocionBase):
    pass

# Esquema de salida para la promoción
class PromocionResponse(PromocionBase):
    id: int

    class Config:
        orm_mode = True
        
# ----------------------- ASIENTO_RESERVADO -------------------------
# Enum para los estados
class EstadoAsiento(str, Enum):
    reservado = "reservado"
    confirmado = "confirmado"
    cancelado = "cancelado"

class AsientoReservadoBase(BaseModel):
    funcion_id: int
    asiento: str
    estado: EstadoAsiento = EstadoAsiento.reservado

class AsientoReservadoCreate(AsientoReservadoBase):
    pass

class AsientoReservadoResponse(AsientoReservadoBase):
    id: int

    class Config:
        orm_mode = True

# ----------------------- RESERVA -------------------------
class ReservaBase(BaseModel):
    usuario_id: int
    funcion_id: int
    asiento_reservado: str
    estado: str = "reservado"
    fecha_reserva: Optional[datetime] = None  # Esta será autogenerada por defecto

class ReservaCreate(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id: int

    class Config:
        orm_mode = True

# ----------------------- DETALLE-RESERVA -------------------------

# Enum para el tipo de detalle de reserva
class TipoDetalleReserva(str, Enum):
    entrada = "entrada"
    producto = "producto"

class DetalleReservaBase(BaseModel):
    reserva_id: int
    tipo: TipoDetalleReserva  # 'entrada' o 'producto'
    descripcion: str
    monto: Decimal  # Usamos Decimal para manejar correctamente los montos

class DetalleReservaCreate(DetalleReservaBase):
    pass

class DetalleReservaResponse(DetalleReservaBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------- PRODUCTO -------------------------
# Enum para tamaño del producto
class TamanoProducto(str, Enum):
    pequeno = "pequeño"
    mediano = "mediano"
    grande = "grande"

class ProductoBase(BaseModel):
    nombre: str
    precio: Decimal
    stock: int  # Número de productos disponibles
    imagen_url: Optional[str] = None  # URL opcional de la imagen
    tamaño: TamanoProducto  # Tamaño del producto (pequeño, mediano, grande)

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------- VENTA -------------------------

class VentaBase(BaseModel):
    usuario_id: int
    producto_id: Optional[int] = None  # Opcional, si se vende un producto
    funcion_id: Optional[int] = None  # Opcional, si se compra una entrada para una función
    monto_total: Decimal  # Monto total de la venta

class VentaCreate(VentaBase):
    pass

class VentaResponse(VentaBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------- FACTURA -------------------------
class FacturaBase(BaseModel):
    venta_id: int
    usuario_id: int
    monto_total: float
    fecha_emision: datetime

class FacturaCreate(FacturaBase):
    pass

class FacturaResponse(FacturaBase):
    id: int

    class Config:
        orm_mode = True



