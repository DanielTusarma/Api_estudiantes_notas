from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.estudiante import Estudiante
from models.nota import Nota
from schemas.estudiante import EstudianteCreate, EstudianteRead, EstudianteReadNotas
from decimal import Decimal
from schemas.nota import NotaRead

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
            promedio=promedio
        )
        
        resultado.append(estudiante_dato)
            
    
    return resultado

# agregar una sola nota a un estudiante
def agregar_nota_estudiante(db: Session, estudiante_id: int, valor_nota: Decimal):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        raise ValueError("Estudiante no encontrado")
    
    if valor_nota < 0 or valor_nota > 5:
        raise ValueError("La nota debe estar entre 0 y 5")
    
    try:
        
        nueva_nota = Nota(valor=valor_nota)
        
        estudiante.notas.append(nueva_nota)
        
        db.commit()
        db.refresh(nueva_nota)
        
        return NotaRead.model_validate(nueva_nota)
    
    except SQLAlchemyError as e:
        db.rollback()
        raise e
        
def reemplazar_notas(db: Session, estudiante_id: int, nuevas_notas):
    estudiante = db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()
    
    if not estudiante:
        raise ValueError("Estudiante no encontrado")
    
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