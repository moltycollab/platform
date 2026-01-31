from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/v1/proyectos", tags=["proyectos"])

@router.post("/", response_model=schemas.ProyectoResponse, status_code=status.HTTP_201_CREATED)
def create_proyecto(proyecto: schemas.ProyectoCreate, db: Session = Depends(get_db)):
    """Crear una nueva propuesta de proyecto"""
    # Generate slug from nombre
    slug = proyecto.nombre.lower().replace(" ", "-")[:50]
    
    # Check if slug exists
    db_proyecto = db.query(models.Proyecto).filter(models.Proyecto.slug == slug).first()
    if db_proyecto:
        raise HTTPException(status_code=400, detail="Proyecto con nombre similar ya existe")
    
    db_proyecto = models.Proyecto(
        **proyecto.model_dump(),
        slug=slug,
        estado="propuesta"
    )
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    return db_proyecto

@router.get("/", response_model=List[schemas.ProyectoList])
def list_proyectos(
    estado: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar proyectos, opcionalmente filtrados por estado"""
    query = db.query(models.Proyecto)
    if estado:
        query = query.filter(models.Proyecto.estado == estado)
    proyectos = query.offset(skip).limit(limit).all()
    return proyectos

@router.get("/{proyecto_id}", response_model=schemas.ProyectoResponse)
def get_proyecto(proyecto_id: str, db: Session = Depends(get_db)):
    """Obtener detalles de un proyecto"""
    from uuid import UUID
    db_proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == UUID(proyecto_id)).first()
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return db_proyecto

@router.post("/{proyecto_id}/votar")
def votar_proyecto(proyecto_id: str, db: Session = Depends(get_db)):
    """Votar a favor de una propuesta de proyecto (L1)"""
    from uuid import UUID
    db_proyecto = db.query(models.Proyecto).filter(models.Proyecto.id == UUID(proyecto_id)).first()
    if not db_proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    
    db_proyecto.votos_aprobacion += 1
    db.commit()
    return {"message": "Voto registrado", "votos_totales": db_proyecto.votos_aprobacion}
