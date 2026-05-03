from sqlalchemy import Column, String, Integer
from database import Base
from sqlalchemy.orm import relationship

class Estudiante(Base):
    # nombre de la tabla de la base de datos
    __tablename__ = "estudiantes"
    
    # Id autoincremental y llave primaria
    id = Column(Integer, primary_key=True)
    
    # nombre estudiante
    nombre = Column(String, nullable=False)
    
    # apellido estudiante
    apellido = Column(String, nullable=False)
    
    # relacion
    notas = relationship("Nota", back_populates="estudiante", cascade="all, delete-orphan")
    
    