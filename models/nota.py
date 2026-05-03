from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Nota(Base):
    # nombre de la tabla de la base de datos
    __tablename__ = "notas"
    
    # Id autoincremental y llave primaria
    id = Column(Integer, primary_key=True)
    
    valor = Column(Numeric(3,2), nullable=False)
    
    # clave foranea
    estudiante_id = Column(Integer, ForeignKey("estudiantes.id"), nullable=False)
    
    # Relacion
    estudiante = relationship("Estudiante", back_populates="notas")
    
    