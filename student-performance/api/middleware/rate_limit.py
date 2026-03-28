"""
Rate limiting configuration.
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per day", "200 per hour", "30 per minute"]
)


def setup_rate_limiting(app):
    """
    Setup rate limiting for the application.
    
    Args:
        app: Flask application instance
    """
    limiter.init_app(app)
    
    # Note: Specific endpoint rate limits are applied via decorators in routes
    # Global limits are applied via default_limits above


def get_limiter():
    """Get the limiter instance."""
    return limiter
