"""
Password manager for Pocket Hedge Fund.

This module provides password hashing, verification, and validation
for the authentication system.
"""

import logging
import re
import secrets
import string
from typing import Optional, Dict, Any
import bcrypt
from passlib.context import CryptContext

logger = logging.getLogger(__name__)


class PasswordManager:
    """
    Password manager for Pocket Hedge Fund.
    
    Provides password hashing, verification, validation, and security features.
    """
    
    def __init__(self):
        """Initialize password manager."""
        # Setup password hashing context
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=12
        )
        
        # Password requirements
        self.min_length = 8
        self.max_length = 128
        self.require_uppercase = True
        self.require_lowercase = True
        self.require_digits = True
        self.require_special_chars = True
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        try:
            if not password:
                raise ValueError("Password cannot be empty")
            
            # Hash password
            hashed = self.pwd_context.hash(password)
            
            logger.debug("Password hashed successfully")
            return hashed
            
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            raise
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            if not plain_password or not hashed_password:
                return False
            
            # Verify password
            is_valid = self.pwd_context.verify(plain_password, hashed_password)
            
            logger.debug(f"Password verification result: {is_valid}")
            return is_valid
            
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    def validate_password(self, password: str) -> Dict[str, Any]:
        """
        Validate password against requirements.
        
        Args:
            password: Password to validate
            
        Returns:
            Dict containing validation results
        """
        try:
            errors = []
            warnings = []
            
            # Check length
            if len(password) < self.min_length:
                errors.append(f"Password must be at least {self.min_length} characters long")
            elif len(password) > self.max_length:
                errors.append(f"Password must be no more than {self.max_length} characters long")
            
            # Check for uppercase letters
            if self.require_uppercase and not re.search(r'[A-Z]', password):
                errors.append("Password must contain at least one uppercase letter")
            
            # Check for lowercase letters
            if self.require_lowercase and not re.search(r'[a-z]', password):
                errors.append("Password must contain at least one lowercase letter")
            
            # Check for digits
            if self.require_digits and not re.search(r'\d', password):
                errors.append("Password must contain at least one digit")
            
            # Check for special characters
            if self.require_special_chars and not re.search(f'[{re.escape(self.special_chars)}]', password):
                errors.append(f"Password must contain at least one special character: {self.special_chars}")
            
            # Check for common patterns
            if self._is_common_password(password):
                warnings.append("Password is commonly used and may be insecure")
            
            # Check for repeated characters
            if self._has_repeated_characters(password):
                warnings.append("Password contains repeated characters")
            
            # Check for sequential characters
            if self._has_sequential_characters(password):
                warnings.append("Password contains sequential characters")
            
            # Calculate strength score
            strength_score = self._calculate_strength_score(password)
            strength_level = self._get_strength_level(strength_score)
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings,
                'strength_score': strength_score,
                'strength_level': strength_level,
                'length': len(password)
            }
            
        except Exception as e:
            logger.error(f"Error validating password: {e}")
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"],
                'warnings': [],
                'strength_score': 0,
                'strength_level': 'very_weak',
                'length': 0
            }
    
    def generate_secure_password(self, length: int = 16, include_special: bool = True) -> str:
        """
        Generate a secure random password.
        
        Args:
            length: Password length
            include_special: Whether to include special characters
            
        Returns:
            Generated password string
        """
        try:
            if length < self.min_length:
                length = self.min_length
            elif length > self.max_length:
                length = self.max_length
            
            # Define character sets
            lowercase = string.ascii_lowercase
            uppercase = string.ascii_uppercase
            digits = string.digits
            special = self.special_chars if include_special else ""
            
            # Ensure at least one character from each required set
            password = [
                secrets.choice(lowercase),
                secrets.choice(uppercase),
                secrets.choice(digits)
            ]
            
            if include_special and special:
                password.append(secrets.choice(special))
            
            # Fill remaining length
            all_chars = lowercase + uppercase + digits + special
            for _ in range(length - len(password)):
                password.append(secrets.choice(all_chars))
            
            # Shuffle password
            secrets.SystemRandom().shuffle(password)
            
            generated_password = ''.join(password)
            
            logger.debug(f"Generated secure password of length {length}")
            return generated_password
            
        except Exception as e:
            logger.error(f"Error generating password: {e}")
            raise
    
    def check_password_breach(self, password: str) -> bool:
        """
        Check if password has been breached (simplified check).
        
        Args:
            password: Password to check
            
        Returns:
            True if password appears to be breached, False otherwise
        """
        try:
            # This is a simplified check - in production, you would integrate
            # with services like HaveIBeenPwned API
            
            # Check for very common passwords
            common_passwords = [
                'password', '123456', '123456789', 'qwerty', 'abc123',
                'password123', 'admin', 'letmein', 'welcome', 'monkey',
                '1234567890', 'password1', 'qwerty123', 'dragon', 'master'
            ]
            
            return password.lower() in common_passwords
            
        except Exception as e:
            logger.error(f"Error checking password breach: {e}")
            return False
    
    def get_password_requirements(self) -> Dict[str, Any]:
        """
        Get password requirements.
        
        Returns:
            Dict containing password requirements
        """
        return {
            'min_length': self.min_length,
            'max_length': self.max_length,
            'require_uppercase': self.require_uppercase,
            'require_lowercase': self.require_lowercase,
            'require_digits': self.require_digits,
            'require_special_chars': self.require_special_chars,
            'special_chars': self.special_chars
        }
    
    def update_password_requirements(self, requirements: Dict[str, Any]):
        """
        Update password requirements.
        
        Args:
            requirements: New password requirements
        """
        try:
            if 'min_length' in requirements:
                self.min_length = max(4, requirements['min_length'])
            
            if 'max_length' in requirements:
                self.max_length = min(256, requirements['max_length'])
            
            if 'require_uppercase' in requirements:
                self.require_uppercase = requirements['require_uppercase']
            
            if 'require_lowercase' in requirements:
                self.require_lowercase = requirements['require_lowercase']
            
            if 'require_digits' in requirements:
                self.require_digits = requirements['require_digits']
            
            if 'require_special_chars' in requirements:
                self.require_special_chars = requirements['require_special_chars']
            
            if 'special_chars' in requirements:
                self.special_chars = requirements['special_chars']
            
            logger.info("Password requirements updated")
            
        except Exception as e:
            logger.error(f"Error updating password requirements: {e}")
            raise
    
    # Private helper methods
    
    def _is_common_password(self, password: str) -> bool:
        """Check if password is commonly used."""
        common_patterns = [
            r'^password\d*$',
            r'^123456\d*$',
            r'^qwerty\d*$',
            r'^admin\d*$',
            r'^user\d*$',
            r'^test\d*$',
            r'^guest\d*$',
            r'^demo\d*$'
        ]
        
        for pattern in common_patterns:
            if re.match(pattern, password.lower()):
                return True
        
        return False
    
    def _has_repeated_characters(self, password: str) -> bool:
        """Check for repeated characters."""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def _has_sequential_characters(self, password: str) -> bool:
        """Check for sequential characters."""
        for i in range(len(password) - 2):
            if (ord(password[i+1]) == ord(password[i]) + 1 and 
                ord(password[i+2]) == ord(password[i]) + 2):
                return True
        return False
    
    def _calculate_strength_score(self, password: str) -> int:
        """Calculate password strength score (0-100)."""
        score = 0
        
        # Length score (0-30 points)
        if len(password) >= 8:
            score += 10
        if len(password) >= 12:
            score += 10
        if len(password) >= 16:
            score += 10
        
        # Character variety score (0-40 points)
        if re.search(r'[a-z]', password):
            score += 10
        if re.search(r'[A-Z]', password):
            score += 10
        if re.search(r'\d', password):
            score += 10
        if re.search(f'[{re.escape(self.special_chars)}]', password):
            score += 10
        
        # Complexity score (0-30 points)
        if not self._is_common_password(password):
            score += 10
        if not self._has_repeated_characters(password):
            score += 10
        if not self._has_sequential_characters(password):
            score += 10
        
        return min(score, 100)
    
    def _get_strength_level(self, score: int) -> str:
        """Get strength level from score."""
        if score >= 80:
            return 'very_strong'
        elif score >= 60:
            return 'strong'
        elif score >= 40:
            return 'moderate'
        elif score >= 20:
            return 'weak'
        else:
            return 'very_weak'
