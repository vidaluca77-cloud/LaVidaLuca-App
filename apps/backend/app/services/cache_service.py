"""
Cache service for caching frequently accessed data.
"""

import json
import hashlib
from typing import Any, Optional, Dict


class CacheService:
    """Service for caching operations."""
    
    def __init__(self):
        # Simple in-memory cache for testing
        # In production, this would use Redis or similar
        self._cache = {}
    
    def set(self, key: str, value: Any, expiry: int = 300) -> None:
        """Set a value in cache with expiry time."""
        serialized_value = json.dumps(value, default=str)
        self._cache[key] = {
            "value": serialized_value,
            "expiry": expiry  # Would implement proper expiry in production
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache."""
        if key not in self._cache:
            return None
        
        cached_item = self._cache[key]
        try:
            return json.loads(cached_item["value"])
        except (json.JSONDecodeError, KeyError):
            return None
    
    def delete(self, key: str) -> None:
        """Delete a value from cache."""
        if key in self._cache:
            del self._cache[key]
    
    def generate_key(self, *args, **kwargs) -> str:
        """Generate a cache key from arguments."""
        key_parts = list(args)
        
        # Add sorted kwargs to ensure consistent key generation
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        
        key_string = ":".join(str(part) for part in key_parts)
        
        # Hash the key to ensure consistent length and avoid special characters
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()