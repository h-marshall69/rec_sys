# api/routes/__init__.py
from .recommendations import recommendations_bp
from .users import users_bp
from .health import health_bp

__all__ = ['recommendations_bp', 'users_bp', 'health_bp']