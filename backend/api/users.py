from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.session import get_db
from schemas.base import (
    User, UserCreate, UserUpdate, 
    Project, ProjectCreate, ProjectUpdateRequest,
    Module, ModuleCreate, ModuleUpdate,
    Vote, VoteCreate,
    ModuleContribution, ModuleContributionCreate,
    ProjectUpdate, ProjectUpdateCreate,
    ProjectMember, ProjectMemberCreate
)
from models import User as UserModel, Project as ProjectModel, Module as ModuleModel
from models import Vote as VoteModel, ModuleContribution as ContributionModel
from models import ProjectUpdate as UpdateModel, ProjectMember as MemberModel
import models


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
def get_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Obtener lista de usuarios"""
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    # Verificar si ya existe un usuario con el mismo github_id o github_username
    existing_user = db.query(UserModel).filter(
        (UserModel.github_id == user.github_id) | 
        (UserModel.github_username == user.github_username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this GitHub ID or username already exists"
        )
    
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Actualizar un usuario existente"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario"""
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}