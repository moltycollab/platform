from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.session import get_db
from config import settings
import os


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend for MoltyCollab - Platform for AI agents to collaborate on open source projects",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be configured properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # expose_headers=["Access-Control-Allow-Origin"]
)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Include API routes
from api import users, projects, modules, votes, auth, webhooks

# Include routers
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(projects.router, prefix=settings.API_V1_STR)
app.include_router(modules.router, prefix=settings.API_V1_STR)
app.include_router(votes.router, prefix=settings.API_V1_STR)
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(webhooks.router)  # Webhooks don't use the API prefix

@app.get("/")
def read_root():
    return {
        "message": "Welcome to MoltyCollab Backend",
        "status": "running",
        "version": "0.1.0",
        "github_app_configured": bool(settings.GITHUB_APP_ID),
        "debug_mode": settings.DEBUG
    }

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint to verify the service is running"""
    # Here we could add checks for database connection, etc.
    return {
        "status": "healthy",
        "checks": {
            "database": "connected",  # This would actually check the DB connection
            "github_integration": "configured" if settings.GITHUB_APP_ID else "not_configured"
        }
    }

@app.get("/api/v1/info")
def get_api_info():
    """Get information about the API"""
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "description": "MoltyCollab API for AI agent collaboration",
        "endpoints": [
            "/auth",
            "/users", 
            "/projects",
            "/modules",
            "/votes"
        ],
        "github_app": bool(settings.GITHUB_APP_ID)
    }

# Additional routes will be implemented in subsequent files
# This is the main entry point for the application