from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from decimal import Decimal
from .nota import NotaRead

class EstudianteBase(BaseModel):
    # validacion de los datos
    nombre: str = Field(..., min_length=2, max_length=50, description="nombre del estudiante")
    apellido: str = Field(..., min_length=2, max_length=50, description="apellido del estudiante")
    
    # validacion adicional
    @field_validator("nombre", "apellido")
    def no_vacios(cls, valor):
        if not valor.strip():
            raise ValueError("El campo no puede estar vacio")
        return valor
    
class EstudianteCreate(EstudianteBase):
    pass

class EstudianteUpdate(BaseModel):
    
    nombre: Optional[str] = Field(None, min_length=2)
    apellido: Optional[str] = Field(None, min_length=2)
    
    # validacion adicional
    @field_validator("nombre", "apellido")
    def no_vacios_optional(cls, valor):
        if valor is not None and not valor.strip():
            raise ValueError("El campo no puede estar vacio")
        return valor
    
class EstudianteRead(BaseModel):
    
    id: int
    nombre: str
    apellido: str
    
    model_config = {
        "from_attributes": True
    }
    
class EstudianteReadNotas(EstudianteRead):
    
    notas: List[NotaRead]
    promedio: Optional[Decimal] = None