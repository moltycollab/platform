import jwt
import time
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from config import settings
import os


class GitHubAppService:
    """Service to handle GitHub App authentication and operations"""
    
    def __init__(self):
        self.app_id = settings.GITHUB_APP_ID
        self.private_key_path = settings.GITHUB_APP_PRIVATE_KEY_PATH
        self.webhook_secret = settings.GITHUB_WEBHOOK_SECRET
        self.api_base_url = "https://api.github.com"
        
    def _load_private_key(self) -> str:
        """Load the private key from file"""
        if not os.path.exists(self.private_key_path):
            raise FileNotFoundError(f"Private key not found at {self.private_key_path}")
        
        with open(self.private_key_path, 'r') as key_file:
            return key_file.read()
    
    def generate_jwt_token(self) -> str:
        """Generate a JWT token for GitHub App authentication"""
        private_key = self._load_private_key()
        
        # Create JWT payload
        payload = {
            'iat': int(time.time()),  # issued at time
            'exp': int(time.time()) + (10 * 60),  # expiration time (10 minutes)
            'iss': self.app_id  # GitHub App's identifier
        }
        
        # Generate JWT
        encoded_jwt = jwt.encode(payload, private_key, algorithm='RS256')
        return encoded_jwt
    
    def get_app_info(self) -> Dict:
        """Get information about the GitHub App"""
        jwt_token = self.generate_jwt_token()
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(f'{self.api_base_url}/app', headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_installations(self) -> List[Dict]:
        """Get all installations of the GitHub App"""
        jwt_token = self.generate_jwt_token()
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(f'{self.api_base_url}/app/installations', headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_installation_access_token(self, installation_id: int) -> Dict:
        """Get an access token for a specific installation"""
        jwt_token = self.generate_jwt_token()
        
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.post(
            f'{self.api_base_url}/app/installations/{installation_id}/access_tokens',
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    def get_installation_repositories(self, installation_id: int) -> Dict:
        """Get repositories for a specific installation"""
        # First get an access token for the installation
        token_data = self.get_installation_access_token(installation_id)
        access_token = token_data['token']
        
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        response = requests.get(
            f'{self.api_base_url}/installation/repositories',
            headers=headers
        )
        response.raise_for_status()
        
        return response.json()
    
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify the signature of a webhook payload"""
        expected_signature = 'sha256=' + self._calculate_signature(payload)
        return signature == expected_signature
    
    def _calculate_signature(self, payload: bytes) -> str:
        """Calculate the SHA256 signature for webhook verification"""
        private_key = self._load_private_key()
        
        # Calculate HMAC-SHA256 signature
        import hashlib
        import hmac
        
        # Use the webhook secret to calculate the signature
        secret = self.webhook_secret.encode('utf-8')
        signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
        return signature


# Global instance
github_app_service = GitHubAppService()