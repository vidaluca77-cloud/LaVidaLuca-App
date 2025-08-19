"""
Validation service for input validation and sanitization.
"""

import re
from typing import Dict, Any, List
import html


class ValidationService:
    """Service for validating and sanitizing user input."""
    
    def validate_email(self, email: str) -> bool:
        """Validate email format."""
        if not email:
            return False
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_pattern, email) is not None
    
    def validate_password_strength(self, password: str) -> bool:
        """Validate password strength."""
        if not password or len(password) < 8:
            return False
        
        # Check for at least one uppercase, one lowercase, one digit
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        return has_upper and has_lower and has_digit
    
    def validate_activity_data(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate activity data."""
        errors = []
        
        # Required fields
        if not activity_data.get("title", "").strip():
            errors.append("Title is required")
        
        if not activity_data.get("category", "").strip():
            errors.append("Category is required")
        
        # Valid categories
        valid_categories = ["technology", "sports", "arts", "nature", "science"]
        if activity_data.get("category") not in valid_categories:
            errors.append(f"Category must be one of: {', '.join(valid_categories)}")
        
        # Valid difficulty levels
        valid_difficulties = ["beginner", "intermediate", "advanced"]
        if activity_data.get("difficulty_level") not in valid_difficulties:
            errors.append(f"Difficulty level must be one of: {', '.join(valid_difficulties)}")
        
        # Duration validation
        duration = activity_data.get("duration_minutes")
        if duration is not None and (not isinstance(duration, int) or duration <= 0):
            errors.append("Duration must be a positive integer")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors
        }
    
    def sanitize_input(self, input_text: str) -> str:
        """Sanitize user input to prevent XSS and other attacks."""
        if not input_text:
            return ""
        
        # HTML escape to prevent XSS
        sanitized = html.escape(input_text)
        
        # Remove potentially dangerous patterns
        dangerous_patterns = [
            r'<script.*?>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'DROP\s+TABLE',
            r'INSERT\s+INTO',
            r'DELETE\s+FROM',
            r'UPDATE\s+SET'
        ]
        
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()