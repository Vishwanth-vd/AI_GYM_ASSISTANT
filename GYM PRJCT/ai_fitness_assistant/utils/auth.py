"""
Authentication Module
Handles user authentication, password hashing, and session management
"""

import bcrypt
import re
from typing import Optional, Dict, Tuple
from utils.database import db


class AuthManager:
    """Manages user authentication and authorization."""
    
    MIN_PASSWORD_LENGTH = 8
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash."""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception:
            return False
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not email:
            return False, "Email is required"
        
        if not re.match(pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """Validate username."""
        if not username:
            return False, "Username is required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(username) > 20:
            return False, "Username must be less than 20 characters"
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, ""
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """Validate password strength."""
        if not password:
            return False, "Password is required"
        
        if len(password) < AuthManager.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {AuthManager.MIN_PASSWORD_LENGTH} characters"
        
        if not re.search(r'[A-Za-z]', password):
            return False, "Password must contain at least one letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number"
        
        return True, ""
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> Tuple[bool, str, Optional[int]]:
        """
        Register a new user.
        Returns: (success, message, user_id)
        """
        # Validate username
        valid, msg = AuthManager.validate_username(username)
        if not valid:
            return False, msg, None
        
        # Validate email
        valid, msg = AuthManager.validate_email(email)
        if not valid:
            return False, msg, None
        
        # Validate password
        valid, msg = AuthManager.validate_password(password)
        if not valid:
            return False, msg, None
        
        # Check if username exists
        if db.get_user_by_username(username):
            return False, "Username already exists", None
        
        # Check if email exists
        if db.get_user_by_email(email):
            return False, "Email already registered", None
        
        # Hash password
        password_hash = AuthManager.hash_password(password)
        
        # Create user
        user_id = db.create_user(username, email, password_hash)
        
        if user_id:
            return True, "Registration successful", user_id
        else:
            return False, "Registration failed. Please try again.", None
    
    @staticmethod
    def login_user(username_or_email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Authenticate a user.
        Returns: (success, message, user_data)
        """
        if not username_or_email or not password:
            return False, "Username/email and password are required", None
        
        # Try to find user by username or email
        user = db.get_user_by_username(username_or_email)
        if not user:
            user = db.get_user_by_email(username_or_email)
        
        if not user:
            return False, "Invalid credentials", None
        
        # Verify password
        if not AuthManager.verify_password(password, user['password_hash']):
            return False, "Invalid credentials", None
        
        # Check if user is active
        if not user.get('is_active', True):
            return False, "Account is disabled", None
        
        # Update last login
        db.update_last_login(user['id'])
        
        # Remove password hash from returned data
        user_data = {k: v for k, v in user.items() if k != 'password_hash'}
        
        return True, "Login successful", user_data
    
    @staticmethod
    def get_user_profile(user_id: int) -> Optional[Dict]:
        """Get user profile data."""
        return db.get_profile(user_id)
    
    @staticmethod
    def is_profile_complete(user_id: int) -> bool:
        """Check if user has completed their profile."""
        profile = db.get_profile(user_id)
        return profile and profile.get('profile_complete', False)


# Global auth manager instance
auth = AuthManager()
