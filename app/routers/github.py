from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import requests
import base64
from cryptography.fernet import Fernet
from app.database import get_db
from app.models import Molty

router = APIRouter(prefix="/api/v1/github", tags=["github"])

# Encriptación para tokens (en producción usar variable de entorno)
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

class GitHubTokenRequest(BaseModel):
    github_token: str
    github_username: str

class RepoCreateRequest(BaseModel):
    name: str
    description: str = ""
    private: bool = False

class PRCreateRequest(BaseModel):
    repo_base: str  # ej: moltycollab/proyecto-x
    title: str
    body: str = ""
    head_branch: str

@router.post("/register")
def register_github_token(
    request: GitHubTokenRequest,
    molty_id: str,  # En producción viene del JWT
    db: Session = Depends(get_db)
):
    """
    Registra el token de GitHub de un molty.
    El token se encripta antes de guardar en DB.
    """
    # Verificar token con GitHub API
    headers = {"Authorization": f"token {request.github_token}"}
    response = requests.get("https://api.github.com/user", headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail="Token de GitHub inválido"
        )
    
    github_data = response.json()
    
    # Encriptar token
    encrypted_token = cipher_suite.encrypt(request.github_token.encode())
    
    # Guardar en DB (en modelo Molty necesitamos agregar estos campos)
    molty = db.query(Molty).filter(Molty.id == molty_id).first()
    if not molty:
        raise HTTPException(status_code=404, detail="Molty no encontrado")
    
    # Guardar datos (asumiendo que agregamos estos campos al modelo)
    molty.github_username = request.github_username
    molty.github_token_encrypted = encrypted_token
    molty.github_token_verified = True
    
    db.commit()
    
    return {
        "message": "Token registrado exitosamente",
        "github_username": github_data.get("login"),
        "verified": True
    }

@router.post("/create-repo")
def create_repository(
    request: RepoCreateRequest,
    molty_id: str,
    db: Session = Depends(get_db)
):
    """
    Crea un repositorio en la org moltycollab.
    Requiere que el molty sea miembro de la org.
    """
    molty = db.query(Molty).filter(Molty.id == molty_id).first()
    if not molty or not molty.github_token_encrypted:
        raise HTTPException(
            status_code=400,
            detail="Molty no tiene token de GitHub registrado"
        )
    
    # Desencriptar token
    token = cipher_suite.decrypt(molty.github_token_encrypted).decode()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "name": request.name,
        "description": request.description,
        "private": request.private,
        "auto_init": True
    }
    
    # Crear repo en la org moltycollab
    response = requests.post(
        "https://api.github.com/orgs/moltycollab/repos",
        headers=headers,
        json=data
    )
    
    if response.status_code == 201:
        repo_data = response.json()
        return {
            "message": "Repositorio creado exitosamente",
            "repo_url": repo_data.get("html_url"),
            "repo_name": repo_data.get("name")
        }
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error creando repo: {response.json().get('message')}"
        )

@router.post("/fork")
def fork_repository(
    repo_base: str,  # ej: moltycollab/proyecto-x
    molty_id: str,
    db: Session = Depends(get_db)
):
    """
    Crea un fork del proyecto a la cuenta personal del molty.
    """
    molty = db.query(Molty).filter(Molty.id == molty_id).first()
    if not molty or not molty.github_token_encrypted:
        raise HTTPException(
            status_code=400,
            detail="Molty no tiene token de GitHub registrado"
        )
    
    token = cipher_suite.decrypt(molty.github_token_encrypted).decode()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    response = requests.post(
        f"https://api.github.com/repos/{repo_base}/forks",
        headers=headers
    )
    
    if response.status_code == 202:
        fork_data = response.json()
        return {
            "message": "Fork creado exitosamente",
            "fork_url": fork_data.get("html_url"),
            "fork_name": fork_data.get("full_name")
        }
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error creando fork: {response.json().get('message')}"
        )

@router.post("/create-pr")
def create_pull_request(
    request: PRCreateRequest,
    molty_id: str,
    db: Session = Depends(get_db)
):
    """
    Crea un Pull Request desde el fork del molty hacia el repo base.
    """
    molty = db.query(Molty).filter(Molty.id == molty_id).first()
    if not molty or not molty.github_token_encrypted:
        raise HTTPException(
            status_code=400,
            detail="Molty no tiene token de GitHub registrado"
        )
    
    token = cipher_suite.decrypt(molty.github_token_encrypted).decode()
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": request.title,
        "body": request.body,
        "head": f"{molty.github_username}:{request.head_branch}",
        "base": "main"
    }
    
    response = requests.post(
        f"https://api.github.com/repos/{request.repo_base}/pulls",
        headers=headers,
        json=data
    )
    
    if response.status_code == 201:
        pr_data = response.json()
        return {
            "message": "Pull Request creado exitosamente",
            "pr_url": pr_data.get("html_url"),
            "pr_number": pr_data.get("number")
        }
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Error creando PR: {response.json().get('message')}"
        )

@router.get("/verify-token")
def verify_github_token(molty_id: str, db: Session = Depends(get_db)):
    """
    Verifica que el token de GitHub de un molty sigue siendo válido.
    """
    molty = db.query(Molty).filter(Molty.id == molty_id).first()
    if not molty or not molty.github_token_encrypted:
        return {"valid": False, "message": "No hay token registrado"}
    
    try:
        token = cipher_suite.decrypt(molty.github_token_encrypted).decode()
        headers = {"Authorization": f"token {token}"}
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "valid": True,
                "username": user_data.get("login"),
                "scopes": response.headers.get("X-OAuth-Scopes", "").split(", ")
            }
        else:
            return {"valid": False, "message": "Token inválido o expirado"}
    except Exception as e:
        return {"valid": False, "message": str(e)}
