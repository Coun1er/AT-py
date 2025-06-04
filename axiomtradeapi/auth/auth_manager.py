"""
Authentication and Cookie Manager for Axiom Trade API
Handles automatic login, token refresh, and cookie management
"""

import requests
import json
import time
import logging
import os
from typing import Dict, Optional, Union
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class AuthTokens:
    """Container for authentication tokens"""
    access_token: str
    refresh_token: str
    expires_at: float
    issued_at: float
    
    @property
    def is_expired(self) -> bool:
        """Check if token is expired (with 5 minute buffer)"""
        return time.time() >= (self.expires_at - 300)  # 5 minute buffer
    
    @property
    def needs_refresh(self) -> bool:
        """Check if token needs refresh (15 minute buffer)"""
        return time.time() >= (self.expires_at - 900)  # 15 minute buffer


class CookieManager:
    """Manages cookies for HTTP requests"""
    
    def __init__(self):
        self.cookies = {}
        self.logger = logging.getLogger(__name__)
    
    def set_auth_cookies(self, auth_token: str, refresh_token: str) -> None:
        """Set authentication cookies"""
        self.cookies['auth-access-token'] = auth_token
        self.cookies['auth-refresh-token'] = refresh_token
        self.logger.debug("Authentication cookies updated")
    
    def get_cookie_header(self) -> str:
        """Get formatted cookie header string"""
        if not self.cookies:
            return ""
        
        cookie_pairs = [f"{key}={value}" for key, value in self.cookies.items()]
        return "; ".join(cookie_pairs)
    
    def clear_auth_cookies(self) -> None:
        """Clear authentication cookies"""
        self.cookies.pop('auth-access-token', None)
        self.cookies.pop('auth-refresh-token', None)
        self.logger.debug("Authentication cookies cleared")
    
    def has_auth_cookies(self) -> bool:
        """Check if auth cookies are present"""
        return 'auth-access-token' in self.cookies and 'auth-refresh-token' in self.cookies


class AuthManager:
    """
    Manages authentication for Axiom Trade API
    Handles automatic login, token refresh, and session management
    """
    
    def __init__(self, username: str = None, password: str = None, 
                 auth_token: str = None, refresh_token: str = None):
        """
        Initialize AuthManager
        
        Args:
            username: Email for automatic login
            password: Password for automatic login  
            auth_token: Existing auth token (optional)
            refresh_token: Existing refresh token (optional)
        """
        self.username = username
        self.password = password
        self.base_url = "https://axiom.trade"
        self.login_url = f"{self.base_url}/api/auth/login"
        self.refresh_url = f"{self.base_url}/api/auth/refresh"
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize cookie manager
        self.cookie_manager = CookieManager()
        
        # Token storage
        self.tokens: Optional[AuthTokens] = None
        
        # Initialize with existing tokens if provided
        if auth_token and refresh_token:
            self._set_tokens(auth_token, refresh_token)
        
        # Auto-login if credentials provided
        elif username and password:
            self.authenticate()
    
    def _set_tokens(self, auth_token: str, refresh_token: str, 
                   expires_in: int = 3600) -> None:
        """Set authentication tokens"""
        current_time = time.time()
        
        self.tokens = AuthTokens(
            access_token=auth_token,
            refresh_token=refresh_token,
            expires_at=current_time + expires_in,
            issued_at=current_time
        )
        
        # Update cookies
        self.cookie_manager.set_auth_cookies(auth_token, refresh_token)
        
        self.logger.info("Authentication tokens updated successfully")
    
    def authenticate(self) -> bool:
        """
        Authenticate with username/password
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not self.username or not self.password:
            self.logger.error("Username and password required for authentication")
            return False
        
        payload = {
            "email": self.username,
            "password": self.password
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/discover",
            "User-Agent": "AxiomTradeAPI-py/1.0"
        }
        
        try:
            self.logger.info("Attempting authentication...")
            
            response = requests.post(
                self.login_url, 
                json=payload, 
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                # Extract tokens from response cookies
                auth_token = response.cookies.get('auth-access-token')
                refresh_token = response.cookies.get('auth-refresh-token')
                
                if auth_token and refresh_token:
                    self._set_tokens(auth_token, refresh_token)
                    self.logger.info("✅ Authentication successful!")
                    return True
                else:
                    self.logger.error("❌ No authentication tokens in response")
                    return False
            else:
                self.logger.error(f"❌ Authentication failed: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Authentication request failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected authentication error: {e}")
            return False
    
    def refresh_tokens(self) -> bool:
        """
        Refresh authentication tokens
        
        Returns:
            bool: True if refresh successful, False otherwise
        """
        if not self.tokens or not self.tokens.refresh_token:
            self.logger.error("No refresh token available")
            return False
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"auth-refresh-token={self.tokens.refresh_token}",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/discover",
            "User-Agent": "AxiomTradeAPI-py/1.0"
        }
        
        try:
            self.logger.info("Refreshing authentication tokens...")
            
            response = requests.post(
                self.refresh_url,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                # Extract new tokens from response cookies
                new_auth_token = response.cookies.get('auth-access-token')
                new_refresh_token = response.cookies.get('auth-refresh-token')
                
                if new_auth_token:
                    # Use existing refresh token if new one not provided
                    refresh_token = new_refresh_token or self.tokens.refresh_token
                    self._set_tokens(new_auth_token, refresh_token)
                    self.logger.info("✅ Tokens refreshed successfully!")
                    return True
                else:
                    self.logger.error("❌ No new access token in refresh response")
                    return False
            else:
                self.logger.error(f"❌ Token refresh failed: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"❌ Token refresh request failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"❌ Unexpected token refresh error: {e}")
            return False
    
    def ensure_valid_authentication(self) -> bool:
        """
        Ensure we have valid authentication tokens
        Automatically refreshes or re-authenticates as needed
        
        Returns:
            bool: True if valid authentication available, False otherwise
        """
        # No tokens at all - try to authenticate
        if not self.tokens:
            if self.username and self.password:
                return self.authenticate()
            else:
                self.logger.error("No authentication tokens and no credentials provided")
                return False
        
        # Tokens are still valid
        if not self.tokens.is_expired:
            return True
        
        # Try to refresh tokens
        if self.refresh_tokens():
            return True
        
        # Refresh failed - try to re-authenticate
        if self.username and self.password:
            self.logger.info("Token refresh failed, attempting re-authentication...")
            return self.authenticate()
        
        self.logger.error("Cannot refresh tokens and no credentials for re-authentication")
        return False
    
    def get_authenticated_headers(self, additional_headers: Dict[str, str] = None) -> Dict[str, str]:
        """
        Get headers with authentication cookies
        
        Args:
            additional_headers: Additional headers to include
            
        Returns:
            dict: Headers with authentication cookies
        """
        # Ensure we have valid authentication
        if not self.ensure_valid_authentication():
            self.logger.warning("No valid authentication available")
        
        # Base headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/discover",
            "User-Agent": "AxiomTradeAPI-py/1.0"
        }
        
        # Add authentication cookies if available
        cookie_header = self.cookie_manager.get_cookie_header()
        if cookie_header:
            headers["Cookie"] = cookie_header
        
        # Add any additional headers
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def is_authenticated(self) -> bool:
        """Check if currently authenticated with valid tokens"""
        return (self.tokens is not None and 
                not self.tokens.is_expired and 
                self.cookie_manager.has_auth_cookies())
    
    def logout(self) -> None:
        """Clear all authentication data"""
        self.tokens = None
        self.cookie_manager.clear_auth_cookies()
        self.logger.info("Logged out successfully")
    
    def get_token_info(self) -> Dict[str, Union[str, bool, float]]:
        """Get information about current tokens"""
        if not self.tokens:
            return {"authenticated": False}
        
        return {
            "authenticated": True,
            "access_token_preview": self.tokens.access_token[:20] + "..." if self.tokens.access_token else None,
            "expires_at": self.tokens.expires_at,
            "issued_at": self.tokens.issued_at,
            "is_expired": self.tokens.is_expired,
            "needs_refresh": self.tokens.needs_refresh,
            "time_until_expiry": self.tokens.expires_at - time.time() if not self.tokens.is_expired else 0
        }


# Convenience function for quick authentication
def create_authenticated_session(username: str = None, password: str = None,
                                auth_token: str = None, refresh_token: str = None) -> AuthManager:
    """
    Create an authenticated session
    
    Args:
        username: Email for automatic login
        password: Password for automatic login
        auth_token: Existing auth token (optional)
        refresh_token: Existing refresh token (optional)
        
    Returns:
        AuthManager: Configured authentication manager
    """
    return AuthManager(
        username=username,
        password=password,
        auth_token=auth_token,
        refresh_token=refresh_token
    )
