from fastapi import APIRouter
from app.api import endpoints

api_router = APIRouter()

# En un sistema real, aquí incluimos cada módulo
# api_router.include_router(endpoints.auth_router, prefix="/auth", tags=["auth"])
# api_router.include_router(endpoints.agents_router, prefix="/agents", tags=["agents"])
# api_router.include_router(endpoints.projects_router, prefix="/projects", tags=["projects"])
# api_router.include_router(endpoints.modules_router, prefix="/modules", tags=["modules"])
