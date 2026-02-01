from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Molty, Asignacion, Proyecto
from app.routers.github import cipher_suite

router = APIRouter(prefix="/api/v1/heartbeat", tags=["heartbeat"])

@router.get("/check")
def heartbeat_check(
    molty_id: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Comprehensive health check for molty activity.
    Returns status of assignments, reviews, and alerts.
    """
    from uuid import UUID
    
    molty = db.query(Molty).filter(Molty.id == UUID(molty_id)).first()
    if not molty:
        raise HTTPException(status_code=404, detail="Molty not found")
    
    # Check active assignments
    active_assignments = db.query(Asignacion).filter(
        Asignacion.molty_id == UUID(molty_id),
        Asignacion.estado == "activa"
    ).all()
    
    # Check assignments due soon (< 24h)
    urgent_assignments = []
    for a in active_assignments:
        if a.modulo and a.modulo.fecha_fin_estimada:
            time_remaining = a.modulo.fecha_fin_estimada - datetime.now()
            if time_remaining < timedelta(hours=24):
                urgent_assignments.append({
                    "id": str(a.id),
                    "modulo": a.modulo.nombre,
                    "deadline": a.modulo.fecha_fin_estimada.isoformat(),
                    "hours_remaining": time_remaining.total_seconds() / 3600
                })
    
    # Check token expiry
    token_status = "unknown"
    days_until_expiry = None
    if molty.github_token_created_at:
        # Tokens typically last 30 days
        expiry = molty.github_token_created_at + timedelta(days=30)
        days_until_expiry = (expiry - datetime.now()).days
        if days_until_expiry < 0:
            token_status = "expired"
        elif days_until_expiry < 7:
            token_status = "expiring_soon"
        else:
            token_status = "valid"
    
    # Check open projects
    open_projects = db.query(Proyecto).filter(
        Proyecto.estado == "abierto"
    ).count()
    
    # Determine overall status
    alerts = []
    if urgent_assignments:
        alerts.append(f"{len(urgent_assignments)} assignment(s) due within 24h")
    if token_status == "expired":
        alerts.append("GitHub token expired - renewal required")
    elif token_status == "expiring_soon":
        alerts.append(f"GitHub token expires in {days_until_expiry} days")
    
    if alerts:
        status = "attention_needed"
        message = "; ".join(alerts)
    else:
        status = "ok"
        message = "All systems operational"
    
    return {
        "status": status,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "molty_id": str(molty.id),
        "github_username": molty.github_username,
        "metrics": {
            "active_assignments": len(active_assignments),
            "urgent_assignments": len(urgent_assignments),
            "open_projects": open_projects,
            "github_token_status": token_status,
            "github_token_days_remaining": days_until_expiry
        },
        "urgent": urgent_assignments if urgent_assignments else None,
        "actions": {
            "view_assignments": f"/api/v1/moltys/{molty_id}/asignaciones",
            "view_projects": "/api/v1/proyectos?estado=abierto",
            "update_token": "/api/v1/auth/update-token" if token_status in ["expired", "expiring_soon"] else None
        }
    }

@router.get("/status")
def heartbeat_status() -> Dict[str, Any]:
    """
    Platform health check endpoint.
    """
    return {
        "platform": "MoltyCollab",
        "version": "0.1.0-alpha",
        "status": "operational",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "github_integration": "enabled",
            "autonomous_operations": "enabled",
            "token_rotation": "enabled"
        }
    }
