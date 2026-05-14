from fastapi import FastAPI

from routers.estudiantes import router as estudiantes_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Api de gestión de estudiantes",
    description="Backend REST con FastAPI para la gestión de estudiantes",
    version="1.0.0"
)

# configuracion de CORS
origins = [
    "http://localhost:4200", # angular
    "http://localhost:5173", # react vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# endpoint raiz
@app.get("/")
def raiz():
    return {"mensaje": "API Gestión estudiantes funcionando correctamente"}

app.include_router(estudiantes_router)
