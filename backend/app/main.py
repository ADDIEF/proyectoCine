from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Importar el middleware de CORS
from app.routers import user, admin, public, peliculas, sala, funcion, promocion, asiento_reservado, detalle_reserva, venta, factura

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:5173",  # El dominio del frontend (cambiar si es otro puerto)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite solicitudes solo desde estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Incluir descripción del esquema OAuth2 para Swagger
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecuritySchemeType
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Proyecto Cine API",
        version="1.0.0",
        description="Documentación de la API del sistema de cine con JWT Auth",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"OAuth2PasswordBearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Incluyendo las rutas de los routers
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(public.router)
app.include_router(peliculas.router)
app.include_router(sala.router)
app.include_router(funcion.router)
app.include_router(promocion.router)
app.include_router(asiento_reservado.router)
app.include_router(detalle_reserva.router)
app.include_router(venta.router)
app.include_router(factura.router)

@app.get("/")
def root():
    return {"message": "Sistema de Cine funcionando 🚀"}
