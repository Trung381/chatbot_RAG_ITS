import hashlib
import secrets
import string
from typing import Any, Dict, Optional
import json
from datetime import datetime

def generate_random_string(length: int = 32) -> str:
    """Generate a random string of specified length."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def hash_string(text: str) -> str:
    """Create SHA256 hash of a string."""
    return hashlib.sha256(text.encode()).hexdigest()

def serialize_datetime(obj: Any) -> Any:
    """JSON serializer for datetime objects."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string with fallback."""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

class ResponseFormatter:
    """Standardized API response formatter."""
    
    @staticmethod
    def success(data: Any = None, message: str = "Success") -> Dict[str, Any]:
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error(message: str = "Error", code: str = "GENERAL_ERROR") -> Dict[str, Any]:
        return {
            "success": False,
            "message": message,
            "error_code": code
        }
    
    @staticmethod
    def paginated(
        data: list,
        page: int,
        per_page: int,
        total: int,
        message: str = "Success"
    ) -> Dict[str, Any]:
        return {
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "pages": (total + per_page - 1) // per_page
            }
        }
