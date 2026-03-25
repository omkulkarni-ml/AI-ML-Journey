"""
Security utilities for tokens and encryption.
"""
import os
import secrets
import string
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def generate_secure_token(length=32):
    """
    Generate a cryptographically secure random token.
    
    Args:
        length: Length of the token (default: 32)
        
    Returns:
        str: Secure random token
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_token(user_id, token_type='access'):
    """
    Generate JWT token payload.
    
    Args:
        user_id: User ID to encode in token
        token_type: Type of token ('access' or 'refresh')
        
    Returns:
        dict: Token payload
    """
    from flask_jwt_extended import create_access_token, create_refresh_token
    
    additional_claims = {
        'type': token_type,
        'iat': datetime.utcnow()
    }
    
    if token_type == 'access':
        expires = timedelta(hours=1)
        token = create_access_token(
            identity=user_id,
            additional_claims=additional_claims,
            expires_delta=expires
        )
    else:
        expires = timedelta(days=30)
        token = create_refresh_token(
            identity=user_id,
            additional_claims=additional_claims,
            expires_delta=expires
        )
    
    return {
        'token': token,
        'expires_at': (datetime.utcnow() + expires).isoformat(),
        'type': token_type
    }


def verify_token(token):
    """
    Verify a JWT token.
    
    Args:
        token: Token string to verify
        
    Returns:
        tuple: (is_valid: bool, payload: dict or None, error: str or None)
    """
    try:
        from flask_jwt_extended import decode_token
        payload = decode_token(token)
        return True, payload, None
    except Exception as e:
        return False, None, str(e)


def jwt_required_custom(fn):
    """
    Custom JWT required decorator with better error handling.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Authentication required',
                'message': str(e)
            }), 401
    return wrapper


def get_current_user():
    """
    Get current authenticated user.
    
    Returns:
        User: Current user or None
    """
    from models import User
    
    try:
        user_id = get_jwt_identity()
        if user_id:
            return User.query.get(user_id)
    except Exception:
        pass
    return None


def require_active_user(fn):
    """
    Decorator to require active (non-locked) user.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
        from models import User
        
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({
                    'success': False,
                    'error': 'User not found'
                }), 404
            
            if not user.is_active:
                return jsonify({
                    'success': False,
                    'error': 'Account is deactivated'
                }), 403
            
            if user.is_locked():
                return jsonify({
                    'success': False,
                    'error': 'Account is temporarily locked'
                }), 403
            
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401
    
    return wrapper


def check_permission(allowed_roles):
    """
    Decorator to check user role permissions.
    
    Args:
        allowed_roles: List of allowed roles
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
            from models import User
            
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user = User.query.get(user_id)
                
                if not user:
                    return jsonify({
                        'success': False,
                        'error': 'User not found'
                    }), 404
                
                if user.role not in allowed_roles:
                    return jsonify({
                        'success': False,
                        'error': 'Insufficient permissions'
                    }), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': 'Authentication required'
                }), 401
        
        return wrapper
    return decorator
