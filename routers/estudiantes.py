from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from sqlalchemy.orm import Session

from database import get_db
from services.estudiante_service import (
    crear_estudiante, 
    listar_estudiantes_con_promedio, 
    agregar_nota_estudiante,
    reemplazar_notas,
    eliminar_estudiante
)
from schemas.estudiante import EstudianteRead, EstudianteCreate, EstudianteReadNotas, EstudianteUpdate
from schemas.nota import NotaRead, NotaUpdateList, NotaBase


router = APIRouter(
    prefix="/api/estudiantes",
    tags=["Estudiantes"]
)

# ruta para crear un estudiante
@router.post("/", response_model=EstudianteRead, status_code=201)
def crear_estudiante_endpoint(datos: EstudianteCreate, db: Session = Depends(get_db)):
    # crear un estudiante
    nuevo_estudiante = crear_estudiante(db, datos)
    return nuevo_estudiante

# ruta para listar estudiantes
@router.get("/", response_model=List[EstudianteReadNotas])
def obtener_estudiantes_endpoint(db: Session = Depends(get_db)):
    estudiantes = listar_estudiantes_con_promedio(db)
    return estudiantes

# ruta para agregar una nota a un estudiante
@router.patch("/{id}/notas", response_model=NotaRead, status_code=200)
def agregar_nota_a_estudiante(
    datos: NotaBase,
    id: int = Path(..., gt=0, description="Id del estudiante a actualizar"),
    db: Session = Depends(get_db)
):
    nueva_nota = agregar_nota_estudiante(db, id, datos)
    
    if not nueva_nota:
        raise HTTPException(
            status_code=404,
            detail=f"Estudiante con id {id} no encontrado"
        )
    
    return nueva_nota
    

# ruta para reemplazar todas las notas de un estudiante
@router.put("/{id}/notas", response_model=EstudianteReadNotas, status_code=200)
def reemplazar_nota_estudiante_endpoint(
    datos: NotaUpdateList,
    id: int = Path(..., gt=0, description="Id del estudiante a actualizar notas"),
    db: Session = Depends(get_db)
):
    reemplazar_notas_all = reemplazar_notas(db, id, datos.notas)
    
    if not reemplazar_notas_all:
        raise HTTPException(
            status_code=404,
            detail=f"Estudiante con id {id} no encontrado"
        )
    
    return reemplazar_notas_all

# ruta para eliminar un estudiante
@router.delete("/{id}", status_code=204)
def eliminar_estudiante_endpoint(
    id: int = Path(..., gt=0, description="Id del estudiante a eliminar"),
    db: Session = Depends(get_db)
):
    resultado = eliminar_estudiante(db, id)
    if not resultado:
        raise HTTPException(
            status_code=404,
            detail=f"Estudiante con id {id} no encontrado"
        )
    
    return None