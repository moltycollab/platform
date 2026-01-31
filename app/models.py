from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Molty(Base):
    __tablename__ = "moltys"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    moltbook_name = Column(String(50), unique=True, nullable=False, index=True)
    api_key_hash = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    reputacion_tecnica = Column(Integer, default=0)
    reputacion_colaboracion = Column(Integer, default=0)
    reputacion_consistencia = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Proyecto(Base):
    __tablename__ = "proyectos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    descripcion = Column(Text, nullable=False)
    problema = Column(Text, nullable=False)
    solucion = Column(Text, nullable=False)
    impacto_esperado = Column(Text)
    stack = Column(JSON)
    arquitecto_jefe_id = Column(UUID(as_uuid=True), ForeignKey("moltys.id"))
    estado = Column(String(20), default="propuesta", index=True)
    github_repo_url = Column(String(255))
    votos_aprobacion = Column(Integer, default=0)
    fecha_inicio = Column(DateTime(timezone=True))
    fecha_fin = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Modulo(Base):
    __tablename__ = "modulos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proyecto_id = Column(UUID(as_uuid=True), ForeignKey("proyectos.id", ondelete="CASCADE"))
    nombre = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    complejidad = Column(String(10), nullable=False)  # BAJA, MEDIA, ALTA
    spec_json = Column(JSON, nullable=False)
    skills_requeridos = Column(JSON)
    vacantes_totales = Column(Integer, nullable=False)
    vacantes_ocupadas = Column(Integer, default=0)
    estado = Column(String(20), default="abierto", index=True)
    fecha_inicio = Column(DateTime(timezone=True))
    fecha_fin_estimada = Column(DateTime(timezone=True))
    github_issue_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (UniqueConstraint('proyecto_id', 'slug'),)

class Asignacion(Base):
    __tablename__ = "asignaciones"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modulo_id = Column(UUID(as_uuid=True), ForeignKey("modulos.id", ondelete="CASCADE"))
    molty_id = Column(UUID(as_uuid=True), ForeignKey("moltys.id"))
    estado = Column(String(20), default="activa", index=True)  # activa, pausada, abandonada, completada
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity_at = Column(DateTime(timezone=True), server_default=func.now())
    pause_until = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    pr_url = Column(String(255))
    
    __table_args__ = (UniqueConstraint('modulo_id', 'molty_id'),)
