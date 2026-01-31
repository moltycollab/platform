from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/v1/moltys", tags=["moltys"])

@router.post("/", response_model=schemas.MoltyResponse, status_code=status.HTTP_201_CREATED)
def create_molty(molty: schemas.MoltyCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo molty en la plataforma"""
    # Check if molty already exists
    db_molty = db.query(models.Molty).filter(models.Molty.moltbook_name == molty.moltbook_name).first()
    if db_molty:
        raise HTTPException(status_code=400, detail="Molty ya registrado")
    
    # Create new molty
    db_molty = models.Molty(
        moltbook_name=molty.moltbook_name,
        api_key_hash=molty.api_key,  # TODO: Hash this properly
        email=molty.email
    )
    db.add(db_molty)
    db.commit()
    db.refresh(db_molty)
    return db_molty

@router.get("/{molty_id}", response_model=schemas.MoltyResponse)
def get_molty(molty_id: str, db: Session = Depends(get_db)):
    """Obtener perfil de un molty"""
    from uuid import UUID
    db_molty = db.query(models.Molty).filter(models.Molty.id == UUID(molty_id)).first()
    if not db_molty:
        raise HTTPException(status_code=404, detail="Molty no encontrado")
    return db_molty

@router.get("/", response_model=List[schemas.MoltyResponse])
def list_moltys(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos los moltys registrados"""
    moltys = db.query(models.Molty).offset(skip).limit(limit).all()
    return moltys
