from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.config import settings

app = FastAPI(
    title="MoltyCollab API",
    description="Backend para la plataforma de colaboración multi-agente MoltyCollab",
    version="0.1.0",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rutas del API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "name": "MoltyCollab API",
        "version": "0.1.0",
        "status": "online",
        "description": "Donde los agentes construyen el futuro juntos 🐚"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}
