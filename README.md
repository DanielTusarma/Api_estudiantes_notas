# API Estudiantes y Notas

Proyecto backend desarrollado con FastAPI para gestionar estudiantes y sus notas académicas.

La aplicación permite:

* Crear estudiantes.
* Agregar notas a estudiantes.
* Listar estudiantes con sus notas y promedio.
* Reemplazar notas.
* Eliminar estudiantes.

---

# Tecnologías utilizadas

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* Uvicorn

---

# Arquitectura del proyecto

El proyecto está organizado siguiendo una estructura por capas:

```plaintext
routes/         # Rutas y endpoints
models/         # Modelos SQLAlchemy
schemas/        # Validaciones y serialización con Pydantic
services/       # Lógica de negocio
database.py     # Configuración de base de datos
main.py         # Punto de entrada de FastAPI
```

---

# Funcionalidades implementadas

## Estudiantes

* Crear estudiante.
* Listar estudiantes.
* Eliminar estudiante.

## Notas

* Agregar una nota a un estudiante.
* Reemplazar todas las notas de un estudiante.
* Calcular promedio automáticamente.

---

# Regla de negocio

El promedio de un estudiante solo se muestra cuando tiene mínimo 3 notas registradas.

Si el estudiante tiene menos de 3 notas:

```json
{
  "promedio": null
}
```

---

# Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/DanielTusarma/Api_estudiantes_notas.git
cd Api_estudiantes_notas
```

---

## 2. Crear entorno virtual

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 4. Configurar variables de entorno

Crear un archivo `.env`

```env
DATABASE_URL=postgresql+psycopg2://usuario:password@localhost:5432/estudiantes_db
```

---

## 5. Ejecutar migraciones

```bash
alembic upgrade head
```

---

## 6. Ejecutar servidor

```bash
uvicorn main:app --reload
```

---

# Documentación automática

FastAPI genera documentación automática en:

```plaintext
http://127.0.0.1:8000/docs
```

---

# Estado del proyecto

En desarrollo.

Próximas mejoras:

* Agregar asignaturas.
* Validaciones adicionales.
* Testing automatizado.
* Autenticación.
* Dockerización.
