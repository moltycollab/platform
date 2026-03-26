import jwt
import requests
from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from config import settings
from models import User as UserModel
from database.session import get_db


class GitHubAuthService:
    GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_USER_URL = "https://api.github.com/user"
    GITHUB_USER_EMAILS_URL = "https://api.github.com/user/emails"
    GITHUB_INSTALLATIONS_URL = "https://api.github.com/user/installations"
    
    def __init__(self):
        self.client_id = settings.GITHUB_CLIENT_ID
        self.client_secret = settings.GITHUB_CLIENT_SECRET
        self.redirect_uri = settings.GITHUB_REDIRECT_URI
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        
    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
        
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )
    
    def get_github_access_token(self, code: str) -> str:
        """Exchange authorization code for access token"""
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        headers = {"Accept": "application/json"}
        response = requests.post(self.GITHUB_TOKEN_URL, data=token_data, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to exchange code for access token: {response.text}"
            )
        
        token_json = response.json()
        access_token = token_json.get("access_token")
        
        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No access token received from GitHub"
            )
        
        return access_token
    
    def get_github_user_info(self, access_token: str) -> dict:
        """Get user info from GitHub API"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        user_response = requests.get(self.GITHUB_USER_URL, headers=headers)
        if user_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from GitHub"
            )
        
        github_user = user_response.json()
        
        # Get user emails
        emails_response = requests.get(self.GITHUB_USER_EMAILS_URL, headers=headers)
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
        
        github_user["email"] = primary_email
        
        return github_user
    
    def get_or_create_user(self, db: Session, github_user: dict) -> UserModel:
        """Get existing user or create new one based on GitHub info"""
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
            existing_user.email = github_user.get("email", existing_user.email)
            existing_user.name = github_user.get("name") or github_user.get("login")
            existing_user.github_id = str(github_user["id"])
            
            db.commit()
            db.refresh(existing_user)
            return existing_user
        else:
            # Create new user
            user_data = {
                "github_id": str(github_user["id"]),
                "github_username": github_user["login"],
                "name": github_user.get("name") or github_user["login"],
                "email": github_user.get("email"),
                "avatar_url": github_user.get("avatar_url"),
                "bio": github_user.get("bio"),
                "location": github_user.get("location"),
                "company": github_user.get("company"),
                "is_active": True,
                "is_verified": True  # GitHub-authenticated users are considered verified
            }
            
            user = UserModel(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
    
    def get_user_installations(self, access_token: str) -> list:
        """Get GitHub installations for the authenticated user"""
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get(self.GITHUB_INSTALLATIONS_URL, headers=headers)
        if response.status_code != 200:
            return []  # Return empty list if no installations
        
        return response.json().get("installations", [])
    
    def get_authorization_url(self, state: str = None) -> str:
        """Generate GitHub OAuth authorization URL"""
        from urllib.parse import urlencode
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "user:email repo read:org"
        }
        
        if state:
            params["state"] = state
            
        return f"{self.GITHUB_AUTH_URL}?{urlencode(params)}"


# Global instance
github_auth_service = GitHubAuthService()