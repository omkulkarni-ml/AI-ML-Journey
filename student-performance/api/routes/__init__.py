"""
Routes package initialization.
"""
from .features import features_bp
from .predict import predict_bp
from .auth import auth_bp
from .history import history_bp

__all__ = ['features_bp', 'predict_bp', 'auth_bp', 'history_bp']
