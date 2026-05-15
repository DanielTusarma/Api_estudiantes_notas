from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.estudiante import Estudiante
from models.nota import Nota
from schemas.estudiante import EstudianteCreate, EstudianteRead, EstudianteReadNotas
from decimal import Decimal
from schemas.nota import NotaRead, NotaBase

# servicio para crear un nuevo estudiante
def crear_estudiante(db: Session, datos: EstudianteCreate):
    try: 
        nuevo_estudiante = Estudiante(
            nombre=datos.nombre,
            apellido=datos.apellido
        )
        
        db.add(nuevo_estudiante)
        db.commit()
        db.refresh(nuevo_estudiante)
        
        return nuevo_estudiante

    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
# servicio para obtener estudiantes con promedio
def listar_estudiantes_con_promedio(db: Session):
    estudiantes = db.query(Estudiante).all()
    
    resultado = []

    for est in estudiantes:
        
        if len(est.notas) >= 3:
            promedio = sum(n.valor for n in est.notas) / Decimal(len(est.notas))
        else:
            promedio = None
        
        estudiante_dato = EstudianteReadNotas(
            id=est.id,
            nombre=est.nombre,
            apellido=est.apellido,
            notas=est.notas,
            promedio=round(promedio, 2) if promedio is not None else None
        )
        
        resultado.append(estudiante_dato)
            
    
    return resultado

# agregar una sola nota a un estudiante
def agregar_nota_estudiante(db: Session, estudiante_id: int, datos: NotaBase):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        return None
    
    if datos.valor < 0 or datos.valor > 5:
        raise ValueError("La nota debe estar entre 0 y 5")
    
    try:
        
        nueva_nota = Nota(valor=datos.valor)
        
        estudiante.notas.append(nueva_nota)
        
        db.commit()
        db.refresh(nueva_nota)
        
        return NotaRead.model_validate(nueva_nota)
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
    
# servicio para reemplazar todas las notas del estudiante
def reemplazar_notas(db: Session, estudiante_id: int, nuevas_notas):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        return None
    
    try:
        
        estudiante.notas.clear()
        
        for nota in nuevas_notas:
            nueva_nota = Nota(valor=nota.valor)
            estudiante.notas.append(nueva_nota)

        db.commit()
        db.refresh(estudiante)
    
        return EstudianteReadNotas.model_validate(estudiante)
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    
# servicio para eliminar un estudiante
def eliminar_estudiante(db: Session, estudiante_id: int):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        return None
    
    try:
        db.delete(estudiante)
        db.commit()
        
        return {"message": "Estudiante eliminado exitosamente"}
        
    except SQLAlchemyError as e:
        db.rollback()
        raise e