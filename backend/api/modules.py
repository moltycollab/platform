from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from schemas.base import (
    Module, ModuleCreate, ModuleUpdate,
    ModuleList
)
from models import Module as ModuleModel, Project as ProjectModel, User as UserModel


router = APIRouter(prefix="/modules", tags=["modules"])


def create_slug(title: str) -> str:
    """Crear un slug seguro para URLs"""
    # Convertir a minúsculas y reemplazar espacios con guiones
    slug = title.lower().replace(' ', '-').replace('_', '-')
    # Eliminar caracteres especiales excepto guiones
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    # Asegurar que no tenga guiones repetidos
    while '--' in slug:
        slug = slug.replace('--', '-')
    # Eliminar guiones al inicio o final
    slug = slug.strip('-')
    return slug


@router.get("/", response_model=ModuleList)
def get_modules(
    skip: int = 0, 
    limit: int = 100,
    project_id: int = None,
    status: str = None,
    difficulty: str = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de módulos"""
    query = db.query(ModuleModel)
    
    # Filtrar por proyecto si se especifica
    if project_id:
        query = query.filter(ModuleModel.project_id == project_id)
    
    # Filtrar por estado si se especifica
    if status:
        query = query.filter(ModuleModel.status == status)
    
    # Filtrar por dificultad si se especifica
    if difficulty:
        query = query.filter(ModuleModel.difficulty == difficulty)
    
    # Contar total antes de aplicar límites
    total = query.count()
    
    # Aplicar límites
    modules = query.offset(skip).limit(limit).all()
    
    return ModuleList(modules=modules, total=total)


@router.get("/{module_id}", response_model=Module)
def get_module(module_id: int, db: Session = Depends(get_db)):
    """Obtener un módulo por ID"""
    module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.get("/slug/{slug}", response_model=Module)
def get_module_by_slug(slug: str, db: Session = Depends(get_db)):
    """Obtener un módulo por slug"""
    module = db.query(ModuleModel).filter(ModuleModel.slug == slug).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.post("/", response_model=Module)
def create_module(module: ModuleCreate, db: Session = Depends(get_db)):
    """Crear un nuevo módulo"""
    # Verificar que el proyecto exista
    project = db.query(ProjectModel).filter(ProjectModel.id == module.project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project does not exist"
        )
    
    # Crear slug único
    slug = create_slug(module.title)
    
    # Verificar que el slug no exista
    existing_module = db.query(ModuleModel).filter(ModuleModel.slug == slug).first()
    if existing_module:
        # Si existe, añadir un número
        counter = 1
        original_slug = slug
        while existing_module:
            slug = f"{original_slug}-{counter}"
            existing_module = db.query(ModuleModel).filter(ModuleModel.slug == slug).first()
            counter += 1
    
    # Crear el módulo
    db_module = ModuleModel(
        **module.dict(),
        slug=slug,
        created_by=1  # TODO: Obtener del token de autenticación
    )
    
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module


@router.put("/{module_id}", response_model=Module)
def update_module(
    module_id: int, 
    module_update: ModuleUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar un módulo existente"""
    db_module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Actualizar campos permitidos
    for field, value in module_update.dict(exclude_unset=True).items():
        setattr(db_module, field, value)
    
    # Si se actualiza el título, también actualizar el slug
    if module_update.title:
        new_slug = create_slug(module_update.title)
        # Asegurar que el nuevo slug no entre en conflicto con otros módulos
        existing_module = db.query(ModuleModel).filter(
            ModuleModel.slug == new_slug,
            ModuleModel.id != module_id  # Excluir este módulo
        ).first()
        
        if not existing_module:
            db_module.slug = new_slug
    
    db.commit()
    db.refresh(db_module)
    return db_module


@router.delete("/{module_id}")
def delete_module(module_id: int, db: Session = Depends(get_db)):
    """Eliminar un módulo"""
    db_module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # TODO: Considerar validaciones antes de eliminar (tiene contribuciones activas, etc.)
    
    db.delete(db_module)
    db.commit()
    return {"message": "Module deleted successfully"}


@router.post("/{module_id}/assign")
def assign_module(module_id: int, user_id: int, db: Session = Depends(get_db)):
    """Asignar un módulo a un usuario"""
    module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar que el módulo esté disponible
    if module.status != "available":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Module is not available for assignment"
        )
    
    # Asignar el módulo
    module.assigned_to_id = user_id
    module.status = "in_progress"
    module.started_at = db.query("SELECT NOW()").scalar()
    
    db.commit()
    db.refresh(module)
    
    return {"message": "Module assigned successfully", "module": module}


@router.post("/{module_id}/complete")
def complete_module(module_id: int, db: Session = Depends(get_db)):
    """Marcar un módulo como completado"""
    module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    if module.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Module is not currently in progress"
        )
    
    # Marcar como completado
    module.status = "completed"
    module.completed_at = db.query("SELECT NOW()").scalar()
    module.progress_percentage = 100.0
    
    db.commit()
    db.refresh(module)
    
    return {"message": "Module completed successfully", "module": module}