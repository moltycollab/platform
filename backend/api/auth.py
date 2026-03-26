from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from urllib.parse import urlencode
import requests
import jwt
from datetime import datetime, timedelta
from database.session import get_db
from config import settings
from models import User as UserModel
from schemas.base import Token, User
import os


router = APIRouter(prefix="/auth", tags=["auth"])

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_USER_EMAILS_URL = "https://api.github.com/user/emails"


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.get("/github")
def github_auth_redirect():
    """Redirect to GitHub OAuth authorization"""
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
        "scope": "user:email repo"
    }
    auth_url = f"{GITHUB_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@router.get("/github/callback")
def github_callback(code: str, db: Session = Depends(get_db)):
    """Handle GitHub OAuth callback and create/get user"""
    # Exchange code for access token
    token_data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GITHUB_REDIRECT_URI
    }
    
    headers = {"Accept": "application/json"}
    response = requests.post(GITHUB_TOKEN_URL, data=token_data, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to exchange code for access token"
        )
    
    token_json = response.json()
    access_token = token_json.get("access_token")
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No access token received from GitHub"
        )
    
    # Get user info from GitHub
    user_headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    user_response = requests.get(GITHUB_USER_URL, headers=user_headers)
    if user_response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get user info from GitHub"
        )
    
    github_user = user_response.json()
    
    # Get user emails
    emails_response = requests.get(GITHUB_USER_EMAILS_URL, headers=user_headers)
    user_emails = []
    if emails_response.status_code == 200:
        user_emails = emails_response.json()
    
    # Find primary/public email
    primary_email = None
    for email_obj in user_emails:
        if email_obj.get("primary") or email_obj.get("visibility") == "public":
            primary_email = email_obj.get("email")
            break
    
    if not primary_email and user_emails:
        primary_email = user_emails[0].get("email")
    
    # Check if user already exists
    existing_user = db.query(UserModel).filter(
        (UserModel.github_id == str(github_user["id"])) |
        (UserModel.github_username == github_user["login"])
    ).first()
    
    if existing_user:
        # Update existing user with new info
        existing_user.avatar_url = github_user.get("avatar_url")
        existing_user.bio = github_user.get("bio")
        existing_user.location = github_user.get("location")
        existing_user.company = github_user.get("company")
        existing_user.email = primary_email or existing_user.email
        existing_user.name = github_user.get("name") or github_user.get("login")
        existing_user.github_id = str(github_user["id"])
        
        db.commit()
        db.refresh(existing_user)
        user = existing_user
    else:
        # Create new user
        user_data = {
            "github_id": str(github_user["id"]),
            "github_username": github_user["login"],
            "name": github_user.get("name") or github_user["login"],
            "email": primary_email,
            "avatar_url": github_user.get("avatar_url"),
            "bio": github_user.get("bio"),
            "location": github_user.get("location"),
            "company": github_user.get("company"),
            "is_active": True
        }
        
        user = UserModel(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.github_username},
        expires_delta=access_token_expires
    )
    
    # Return redirect with token (in a real app, you'd handle this differently)
    # For now, return token in response
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "github_username": user.github_username,
            "name": user.name,
            "email": user.email,
            "avatar_url": user.avatar_url
        }
    }


@router.post("/token")  # For compatibility with standard OAuth patterns
def login_for_access_token(request: Request, db: Session = Depends(get_db)):
    """Login route that would normally process form data"""
    # This would normally handle username/password or code exchange
    # For GitHub OAuth, the actual login happens at the callback
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Use /auth/github for GitHub OAuth"
    )