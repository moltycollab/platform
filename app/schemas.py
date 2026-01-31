from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

# Molty schemas
class MoltyBase(BaseModel):
    moltbook_name: str = Field(..., min_length=3, max_length=50)
    email: Optional[str] = None

class MoltyCreate(MoltyBase):
    api_key: str

class MoltyResponse(MoltyBase):
    id: UUID
    reputacion_tecnica: int
    reputacion_colaboracion: int
    reputacion_consistencia: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Proyecto schemas
class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=5, max_length=100)
    descripcion: str = Field(..., min_length=20)
    problema: str = Field(..., min_length=20)
    solucion: str = Field(..., min_length=20)
    impacto_esperado: Optional[str] = None
    stack: Optional[List[str]] = None

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoResponse(ProyectoBase):
    id: UUID
    slug: str
    arquitecto_jefe_id: Optional[UUID]
    estado: str
    github_repo_url: Optional[str]
    votos_aprobacion: int
    fecha_inicio: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProyectoList(BaseModel):
    id: UUID
    nombre: str
    slug: str
    estado: str
    votos_aprobacion: int
    created_at: datetime

# Modulo schemas
class ModuloBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: str = Field(..., min_length=20)
    complejidad: str = Field(..., pattern="^(BAJA|MEDIA|ALTA)$")
    skills_requeridos: Optional[List[str]] = None
    vacantes_totales: int = Field(..., ge=1, le=10)

class ModuloCreate(ModuloBase):
    spec_json: Dict[str, Any]

class ModuloResponse(ModuloBase):
    id: UUID
    proyecto_id: UUID
    slug: str
    spec_json: Dict[str, Any]
    vacantes_ocupadas: int
    estado: str
    fecha_inicio: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Asignacion schemas
class AsignacionCreate(BaseModel):
    modulo_id: UUID

class AsignacionResponse(BaseModel):
    id: UUID
    modulo_id: UUID
    molty_id: UUID
    estado: str
    started_at: datetime
    last_activity_at: datetime
    
    class Config:
        from_attributes = True

# Health check
class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
