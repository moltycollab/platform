from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from schemas.base import (
    Project, ProjectCreate, ProjectUpdateRequest,
    ProjectList
)
from models import Project as ProjectModel, User as UserModel
from urllib.parse import quote_plus


router = APIRouter(prefix="/projects", tags=["projects"])


def create_slug(name: str) -> str:
    """Crear un slug seguro para URLs"""
    # Convertir a minúsculas y reemplazar espacios con guiones
    slug = name.lower().replace(' ', '-').replace('_', '-')
    # Eliminar caracteres especiales excepto guiones
    slug = ''.join(c for c in slug if c.isalnum() or c == '-')
    # Asegurar que no tenga guiones repetidos
    while '--' in slug:
        slug = slug.replace('--', '-')
    # Eliminar guiones al inicio o final
    slug = slug.strip('-')
    return slug


@router.get("/", response_model=ProjectList)
def get_projects(
    skip: int = 0, 
    limit: int = 100,
    is_public: bool = True,
    category: str = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de proyectos"""
    query = db.query(ProjectModel)
    
    # Filtrar por visibilidad
    query = query.filter(ProjectModel.is_public == is_public)
    
    # Filtrar por categoría si se especifica
    if category:
        query = query.filter(ProjectModel.category.ilike(f"%{category}%"))
    
    # Contar total antes de aplicar límites
    total = query.count()
    
    # Aplicar límites
    projects = query.offset(skip).limit(limit).all()
    
    return ProjectList(projects=projects, total=total)


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Obtener un proyecto por ID"""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/slug/{slug}", response_model=Project)
def get_project_by_slug(slug: str, db: Session = Depends(get_db)):
    """Obtener un proyecto por slug"""
    project = db.query(ProjectModel).filter(ProjectModel.slug == slug).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=Project)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Crear un nuevo proyecto"""
    # Verificar que el owner exista
    owner = db.query(UserModel).filter(UserModel.id == project.owner_id).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner user does not exist"
        )
    
    # Crear slug único
    slug = create_slug(project.name)
    
    # Verificar que el slug no exista
    existing_project = db.query(ProjectModel).filter(ProjectModel.slug == slug).first()
    if existing_project:
        # Si existe, añadir un número
        counter = 1
        original_slug = slug
        while existing_project:
            slug = f"{original_slug}-{counter}"
            existing_project = db.query(ProjectModel).filter(ProjectModel.slug == slug).first()
            counter += 1
    
    # Crear URL del repositorio GitHub
    github_repo_url = f"https://github.com/{project.github_repo_owner}/{project.github_repo_name}"
    
    # Crear el proyecto
    db_project = ProjectModel(
        **project.dict(),
        slug=slug,
        github_repo_url=github_repo_url
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int, 
    project_update: ProjectUpdateRequest, 
    db: Session = Depends(get_db)
):
    """Actualizar un proyecto existente"""
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Actualizar campos permitidos
    for field, value in project_update.dict(exclude_unset=True).items():
        setattr(db_project, field, value)
    
    # Si se actualiza el nombre, también actualizar el slug
    if project_update.name:
        new_slug = create_slug(project_update.name)
        # Asegurar que el nuevo slug no entre en conflicto con otros proyectos
        existing_project = db.query(ProjectModel).filter(
            ProjectModel.slug == new_slug,
            ProjectModel.id != project_id  # Excluir este proyecto
        ).first()
        
        if not existing_project:
            db_project.slug = new_slug
    
    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Eliminar un proyecto"""
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # TODO: Considerar validaciones antes de eliminar (tiene módulos activos, etc.)
    
    db.delete(db_project)
    db.commit()
    return {"message": "Project deleted successfully"}