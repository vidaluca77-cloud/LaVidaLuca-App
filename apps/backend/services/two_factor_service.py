"""
Two-Factor Authentication (2FA) service using TOTP.
"""

from typing import Optional, List
import secrets
import hashlib
import base64
from sqlalchemy.orm import Session

from ..models.user import User
from ..core.security import PasswordPolicyError


class TwoFactorService:
    """Service for managing 2FA functionality."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def setup_2fa(self, user: User) -> dict:
        """Setup 2FA for a user and return setup data."""
        if user.two_factor_enabled:
            raise ValueError("2FA is already enabled for this user")
        
        # Generate TOTP secret
        secret = self._generate_2fa_secret()
        
        # Generate backup codes
        backup_codes = self._generate_backup_codes()
        
        # Store secret (will be enabled after verification)
        user.two_factor_secret = secret
        user.backup_codes = backup_codes
        
        self.db.commit()
        
        # Generate QR code for easy setup
        qr_code = self._generate_qr_code(secret, user.email)
        
        return {
            "secret": secret,
            "qr_code": qr_code,
            "backup_codes": backup_codes
        }
    
    def enable_2fa(self, user: User, token: str) -> bool:
        """Enable 2FA after verifying the setup token."""
        if not user.two_factor_secret:
            raise ValueError("2FA must be set up before enabling")
        
        if user.two_factor_enabled:
            raise ValueError("2FA is already enabled")
        
        # Verify the token
        if not self._verify_2fa_token(user.two_factor_secret, token):
            return False
        
        # Enable 2FA
        user.two_factor_enabled = True
        self.db.commit()
        
        return True
    
    def disable_2fa(self, user: User) -> bool:
        """Disable 2FA for a user."""
        if not user.two_factor_enabled:
            return False
        
        user.two_factor_enabled = False
        user.two_factor_secret = None
        user.backup_codes = []
        
        self.db.commit()
        return True
    
    def verify_2fa_token(self, user: User, token: str) -> bool:
        """Verify a 2FA token (TOTP or backup code)."""
        if not user.two_factor_enabled or not user.two_factor_secret:
            return False
        
        # First try TOTP token (6 digits)
        if len(token) == 6 and token.isdigit():
            return self._verify_2fa_token(user.two_factor_secret, token)
        
        # Then try backup code (8 characters)
        elif len(token) == 8:
            return self._verify_backup_code(user, token)
        
        return False
    
    def regenerate_backup_codes(self, user: User) -> List[str]:
        """Regenerate backup codes for a user."""
        if not user.two_factor_enabled:
            raise ValueError("2FA must be enabled to regenerate backup codes")
        
        backup_codes = self._generate_backup_codes()
        user.backup_codes = backup_codes
        
        self.db.commit()
        return backup_codes
    
    def _generate_2fa_secret(self) -> str:
        """Generate a TOTP secret."""
        # Generate 20 random bytes and encode as base32
        secret_bytes = secrets.token_bytes(20)
        secret = base64.b32encode(secret_bytes).decode('utf-8')
        return secret
    
    def _generate_backup_codes(self, count: int = 8) -> List[str]:
        """Generate backup codes for 2FA."""
        codes = []
        for _ in range(count):
            # Generate 4-byte random code and format as hex
            code = secrets.token_hex(4).upper()
            # Format as XXXX-XXXX for readability
            formatted_code = f"{code[:4]}-{code[4:]}"
            codes.append(formatted_code)
        return codes
    
    def _generate_qr_code(self, secret: str, user_email: str) -> str:
        """Generate QR code data for 2FA setup (simplified version)."""
        # In a real implementation, you would use a QR code library
        # For now, return the otpauth URL that can be used to generate QR codes
        from ..core.config import settings
        
        issuer = settings.PROJECT_NAME
        otpauth_url = f"otpauth://totp/{issuer}:{user_email}?secret={secret}&issuer={issuer}"
        
        # Return base64 encoded URL (placeholder for actual QR code)
        return base64.b64encode(otpauth_url.encode()).decode()
    
    def _verify_2fa_token(self, secret: str, token: str) -> bool:
        """Verify TOTP token (simplified implementation)."""
        # This is a simplified implementation
        # In production, use a proper TOTP library like pyotp
        import time
        import hmac
        
        try:
            # Get current time step (30-second intervals)
            time_step = int(time.time()) // 30
            
            # Check current and previous time step for clock drift
            for step in [time_step, time_step - 1]:
                if self._generate_totp(secret, step) == token:
                    return True
            
            return False
        except Exception:
            return False
    
    def _generate_totp(self, secret: str, time_step: int) -> str:
        """Generate TOTP token for given time step (simplified)."""
        # Simplified TOTP implementation
        # In production, use a proper library
        
        # Convert secret from base32
        try:
            secret_bytes = base64.b32decode(secret)
        except Exception:
            return "000000"
        
        # Convert time step to bytes
        time_bytes = time_step.to_bytes(8, 'big')
        
        # Generate HMAC
        hmac_digest = hmac.new(secret_bytes, time_bytes, hashlib.sha1).digest()
        
        # Dynamic truncation
        offset = hmac_digest[-1] & 0x0f
        truncated = hmac_digest[offset:offset + 4]
        
        # Convert to integer and get 6-digit code
        code = int.from_bytes(truncated, 'big') & 0x7fffffff
        return f"{code % 1000000:06d}"
    
    def _verify_backup_code(self, user: User, code: str) -> bool:
        """Verify and consume a backup code."""
        if not user.backup_codes:
            return False
        
        # Normalize the code (remove spaces and dashes)
        normalized_code = code.upper().replace('-', '').replace(' ', '')
        
        # Check against backup codes
        for i, backup_code in enumerate(user.backup_codes):
            normalized_backup = backup_code.replace('-', '').replace(' ', '')
            
            if secrets.compare_digest(normalized_backup, normalized_code):
                # Remove used backup code
                user.backup_codes.pop(i)
                self.db.commit()
                return True
        
        return False