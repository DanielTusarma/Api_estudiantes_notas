# configuracion de la base de datos e importaciones
import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# cargar las variables de entorno
load_dotenv()

# construccion de la URL de conexion a la base de datos
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# creacion del motor de conexion
engine = create_engine(DATABASE_URL, echo=True)

# creacion de un Sessionlocal por peticion
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# clase base para los modelos
Base = declarative_base()

# dependencia para fastapi: obtiene una sesion de la base de datos por peticion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# prueba rapida de conexion
if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Conexion exitosa a PostreSQL")
    except Exception as e:
        print("Error al conectar a la base de datos", e)