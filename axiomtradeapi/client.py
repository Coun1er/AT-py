import requests
import json
from typing import Dict, Optional, List
from .auth.auth_manager import AuthManager, create_authenticated_session

class AxiomTradeClient:
    """
    Main client for interacting with Axiom Trade API with automatic token management
    """
    
    def __init__(self, username: str = None, password: str = None, 
                 auth_token: str = None, refresh_token: str = None,
                 storage_dir: str = None, use_saved_tokens: bool = True):
        """
        Initialize AxiomTradeClient with enhanced authentication
        
        Args:
            username: Email for automatic login
            password: Password for automatic login  
            auth_token: Existing auth token (optional)
            refresh_token: Existing refresh token (optional)
            storage_dir: Directory for secure token storage
            use_saved_tokens: Whether to load/save tokens automatically (default: True)
        """
        # Initialize the enhanced auth manager
        self.auth_manager = AuthManager(
            username=username,
            password=password,
            auth_token=auth_token,
            refresh_token=refresh_token,
            storage_dir=storage_dir,
            use_saved_tokens=use_saved_tokens
        )
        
        # Keep backward compatibility
        self.auth = self.auth_manager  # For legacy code
        
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://axiom.trade',
            'Connection': 'keep-alive',
            'Referer': 'https://axiom.trade/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        }
    
    @property
    def access_token(self) -> Optional[str]:
        """Get current access token"""
        return self.auth_manager.tokens.access_token if self.auth_manager.tokens else None
    
    @property
    def refresh_token(self) -> Optional[str]:
        """Get current refresh token"""
        return self.auth_manager.tokens.refresh_token if self.auth_manager.tokens else None
    
    def login(self, email: str = None, password: str = None) -> Dict:
        """
        Login with username and password using the enhanced auth flow
        
        Args:
            email: Email address (optional if provided in constructor)
            password: Password (optional if provided in constructor)
            
        Returns:
            Dict: Login result with token information
        """
        # Use provided credentials or fall back to constructor values
        email = email or self.auth_manager.username
        password = password or self.auth_manager.password
        
        if not email or not password:
            raise ValueError("Email and password are required for login")
        
        # Update auth manager credentials
        self.auth_manager.username = email
        self.auth_manager.password = password
        
        # Perform authentication
        success = self.auth_manager.authenticate()
        
        if success and self.auth_manager.tokens:
            return {
                'success': True,
                'access_token': self.auth_manager.tokens.access_token,
                'refresh_token': self.auth_manager.tokens.refresh_token,
                'expires_at': self.auth_manager.tokens.expires_at,
                'message': 'Login successful'
            }
        else:
            return {
                'success': False,
                'message': 'Login failed'
            }
        
        return login_result
    
    def set_tokens(self, access_token: str, refresh_token: str) -> None:
        """
        Set authentication tokens directly
        
        Args:
            access_token: The access token
            refresh_token: The refresh token
        """
        self.auth_manager._set_tokens(access_token, refresh_token)
    
    def get_tokens(self) -> Dict[str, Optional[str]]:
        """
        Get current tokens
        """
        tokens = self.auth_manager.tokens
        return {
            'access_token': tokens.access_token if tokens else None,
            'refresh_token': tokens.refresh_token if tokens else None,
            'expires_at': tokens.expires_at if tokens else None,
            'is_expired': tokens.is_expired if tokens else True
        }
    
    def is_authenticated(self) -> bool:
        """
        Check if the client has valid authentication tokens
        """
        return self.auth_manager.is_authenticated()
    
    def refresh_access_token(self) -> bool:
        """
        Refresh the access token using stored refresh token
        
        Returns:
            bool: True if refresh was successful, False otherwise
        """
        return self.auth_manager.refresh_tokens()
    
    def ensure_authenticated(self) -> bool:
        """
        Ensure the client has valid authentication tokens
        Automatically refreshes or re-authenticates as needed
        
        Returns:
            bool: True if valid authentication available, False otherwise
        """
        return self.auth_manager.ensure_valid_authentication()
    
    def logout(self) -> None:
        """Clear all authentication data including saved tokens"""
        self.auth_manager.logout()
    
    def clear_saved_tokens(self) -> bool:
        """Clear saved tokens from secure storage"""
        return self.auth_manager.clear_saved_tokens()
    
    def has_saved_tokens(self) -> bool:
        """Check if saved tokens exist in secure storage"""
        return self.auth_manager.has_saved_tokens()
    
    def get_token_info_detailed(self) -> Dict:
        """Get detailed information about current tokens"""
        return self.auth_manager.get_token_info()
    
    def get_trending_tokens(self, time_period: str = '1h') -> Dict:
        """
        Get trending meme tokens
        Available time periods: 1h, 24h, 7d
        """
        # Ensure we have valid authentication
        if not self.ensure_authenticated():
            raise ValueError("Authentication failed. Please login first.")
        
        url = f'https://api6.axiom.trade/meme-trending?timePeriod={time_period}'
        
        try:
            response = self.auth_manager.make_authenticated_request('GET', url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to get trending tokens: {e}")
    
    def get_token_info(self, token_address: str) -> Dict:
        """
        Get information about a specific token
        """
        # Ensure we have valid authentication
        if not self.ensure_authenticated():
            raise ValueError("Authentication failed. Please login first.")
        
        # This endpoint might need to be confirmed with actual API documentation
        url = f'https://api6.axiom.trade/token/{token_address}'
        
        try:
            response = self.auth_manager.make_authenticated_request('GET', url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to get token info: {e}")
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_user_portfolio(self) -> Dict:
        """
        Get user's portfolio information
        """
        if not self.access_token:
            raise ValueError("Access token required. Please login or set tokens first.")
        
        # This endpoint might need to be confirmed with actual API documentation
        url = 'https://api6.axiom.trade/portfolio'
        headers = {
            **self.base_headers,
            'Cookie': f'auth-access-token={self.access_token}'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        return response.json()

# Convenience functions for quick usage
def quick_login_and_get_trending(email: str, b64_password: str, otp_code: str, time_period: str = '1h') -> Dict:
    """
    Quick function to login and get trending tokens in one call
    """
    client = AxiomTradeClient()
    client.login(email, b64_password, otp_code)
    return client.get_trending_tokens(time_period)

def get_trending_with_token(access_token: str, time_period: str = '1h') -> Dict:
    """
    Quick function to get trending tokens with existing access token
    """
    client = AxiomTradeClient()
    client.set_tokens(access_token=access_token)
    return client.get_trending_tokens(time_period)
