
# Sistema de Gestión de Cine

Este proyecto es un sistema de gestión para un cine que permite a los usuarios consultar películas en cartelera, seleccionar asientos, realizar compras de entradas y productos de confitería, y gestionar promociones y descuentos. Está desarrollado con **FastAPI** para el backend, **PostgreSQL** como base de datos, y **React** para el frontend.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- **Python 3.8+**
- **PostgreSQL**
- **Node.js y npm** (para el frontend con React)

## Instrucciones para Ejecutar el Proyecto

Sigue estos pasos para ejecutar el proyecto desde cero.

### Backend (API Rest con FastAPI)

1. **Accede al directorio del backend**:

   ```bash
   cd backend
   ```

2. **Crear un entorno virtual** (si aún no lo tienes):

   - En **Windows**:

     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

3. **Instalar las dependencias**:

   Dentro del entorno virtual, instala las dependencias necesarias usando `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Crear la base de datos**:

   Crea una base de datos en PostgreSQL llamada `proyecto_cine`. Puedes hacerlo usando `psql` o cualquier cliente de PostgreSQL que prefieras.

   ```sql
   CREATE DATABASE proyecto_cine;
   ```

5. **Configurar las variables de entorno**:

   Crea un archivo `.env` en la carpeta raíz de `backend` y configura las siguientes variables (cambia las credenciales según sea necesario):

   ```env
   DATABASE_URL=postgresql://postgres:fernandez23@localhost:5432/proyecto_cine
   SECRET_KEY=tu_clave_secreta
   ```

   - **`DATABASE_URL`**: Asegúrate de que `postgres:fernandez23` esté configurado con las credenciales correctas de tu base de datos de PostgreSQL.
   - **`SECRET_KEY`**: Define una clave secreta que se usará para JWT.

6. **Ejecutar migraciones de Alembic**:

   Ahora, ejecuta las migraciones de Alembic para crear las tablas en la base de datos:

   ```bash
   alembic upgrade head
   ```

7. **Iniciar el servidor de FastAPI**:

   Finalmente, ejecuta el servidor con Uvicorn:

   ```bash
   uvicorn app.main:app --reload
   ```

   El servidor debería estar corriendo en `http://localhost:8000`. Puedes acceder a la documentación de la API en `http://localhost:8000/docs`.

---

### Frontend (React + Vite)

1. **Accede al directorio del frontend**:

   ```bash
   cd ../frontend
   ```

2. **Instalar las dependencias**:

   Primero, asegúrate de tener las dependencias del frontend instaladas:

   ```bash
   npm install
   ```

3. **Ejecutar el servidor de desarrollo**:

   Luego, ejecuta el servidor de desarrollo de Vite para el frontend:

   ```bash
   npm run dev
   ```

   El frontend debería estar corriendo en `http://localhost:5173`.

---

## Consideraciones Adicionales

- **Cambiar la contraseña de la base de datos**: Si necesitas cambiar la contraseña de tu base de datos, asegúrate de actualizarla en el archivo `.env` del backend, bajo la variable `DATABASE_URL`. La estructura sería:

  ```env
  DATABASE_URL=postgresql://usuario:nueva_contraseña@localhost/proyecto_cine
  ```

- **Acceso a la base de datos**: Asegúrate de que el servicio de PostgreSQL esté corriendo en tu máquina local y que puedas acceder a la base de datos usando el cliente que prefieras (como `psql` o PgAdmin).

---

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```
proyectoCine/
├── backend/          # Backend con FastAPI y configuración de base de datos
│   ├── app/
│   ├── alembic/
│   ├── .env          # Archivo de configuración de entorno
│   └── requirements.txt  # Dependencias del backend
└── frontend/         # Frontend con React y Vite
    ├── src/
    ├── package.json  # Dependencias del frontend
    └── public/
```

---

## Contribuciones

Si deseas contribuir al proyecto, sigue estos pasos:

1. Forkea el repositorio.
2. Crea una nueva rama para tu característica (`git checkout -b feature/nueva-funcionalidad`).
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Crea un pull request.

---

