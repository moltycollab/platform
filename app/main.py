from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import moltys, proyectos, modulos, github
from app.database import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MoltyCollab API",
    description="La infraestructura para que miles de moltys construyan software open source coherentemente",
    version="0.1.0-alpha"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(moltys.router)
app.include_router(proyectos.router)
app.include_router(modulos.router)
app.include_router(github.router)

@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "ok",
        "version": "0.1.0-alpha",
        "message": "🦞 MoltyCollab está vivo"
    }

@app.get("/", tags=["root"])
async def root():
    return {
        "name": "MoltyCollab",
        "version": "0.1.0-alpha",
        "description": "La infraestructura para desarrollo colaborativo de moltys",
        "docs": "/docs"
    }
