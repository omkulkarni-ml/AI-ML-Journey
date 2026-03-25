"""
Security middleware configuration.
"""
from flask_talisman import Talisman
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def setup_security(app):
    """
    Setup security headers and CORS.
    
    Args:
        app: Flask application instance
    """
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('ALLOWED_ORIGINS', ['http://localhost:5173', 'http://localhost:3000']),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "supports_credentials": True
        }
    })
    
    # Configure security headers with Talisman (in production)
    if not app.config.get('DEBUG', False):
        Talisman(
            app,
            force_https=True,
            strict_transport_security=True,
            strict_transport_security_max_age=31536000,
            content_security_policy={
                'default-src': "'self'",
                'script-src': ["'self'", "'unsafe-inline'"],
                'style-src': ["'self'", "'unsafe-inline'"],
                'img-src': ["'self'", "data:", "https:"],
                'font-src': ["'self'"],
                'connect-src': ["'self'"],
            },
            referrer_policy='strict-origin-when-cross-origin',
            feature_policy={
                'geolocation': "'none'",
                'microphone': "'none'",
                'camera': "'none'",
            }
        )
    
    # Add security headers middleware
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Remove server header
        response.headers.pop('Server', None)
        
        return response


def check_token_blacklist(jwt_header, jwt_payload):
    """
    Check if token is blacklisted.
    
    Args:
        jwt_header: JWT header
        jwt_payload: JWT payload
        
    Returns:
        bool: True if token is blacklisted
    """
    from routes.auth import blacklist
    jti = jwt_payload['jti']
    return jti in blacklist
