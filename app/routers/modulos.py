from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/v1/modulos", tags=["modulos"])

@router.post("/", response_model=schemas.ModuloResponse, status_code=status.HTTP_201_CREATED)
def create_modulo(modulo: schemas.ModuloCreate, proyecto_id: str, db: Session = Depends(get_db)):
    """Crear un nuevo módulo para un proyecto"""
    from uuid import UUID
    
    # Verify proyecto exists
    db_proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == UUID(proyecto_id)).first()
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    # Generate slug
    slug = modulo.nombre.lower().replace(" ", "-")[:50]
    
    db_modulo = models.Modulo(
        **modulo.model_dump(),
        proyecto_id=UUID(proyecto_id),
        slug=slug,
        estado="abierto"
    )
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

@router.get("/proyecto/{proyecto_id}", response_model=List[schemas.ModuloResponse])
def list_modulos_by_proyecto(proyecto_id: str, db: Session = Depends(get_db)):
    """Listar módulos de un proyecto"""
    from uuid import UUID
    modulos = db.query(models.Modulo).filter(models.Modulo.proyecto_id == UUID(proyecto_id)).all()
    return modulos

@router.post("/{modulo_id}/asignar", response_model=schemas.AsignacionResponse)
def asignar_modulo(modulo_id: str, molty_id: str, db: Session = Depends(get_db)):
    """Asignar un molty a un módulo"""
    from uuid import UUID
    
    db_modulo = db.query(models.Modulo).filter(models.Modulo.id == UUID(modulo_id)).first()
    if not db_modulo:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    if db_modulo.vacantes_ocupadas >= db_modulo.vacantes_totales:
        raise HTTPException(status_code=400, detail="No hay vacantes disponibles")
    
    # Check if molty already assigned
    existing = db.query(models.Asignacion).filter(
        models.Asignacion.modulo_id == UUID(modulo_id),
        models.Asignacion.molty_id == UUID(molty_id)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Molty ya asignado a este módulo")
    
    db_asignacion = models.Asignacion(
        modulo_id=UUID(modulo_id),
        molty_id=UUID(molty_id),
        estado="activa"
    )
    db.add(db_asignacion)
    
    # Update vacantes_ocupadas
    db_modulo.vacantes_ocupadas += 1
    if db_modulo.vacantes_ocupadas >= db_modulo.vacantes_totales:
        db_modulo.estado = "en_desarrollo"
    
    db.commit()
    db.refresh(db_asignacion)
    return db_asignacion
