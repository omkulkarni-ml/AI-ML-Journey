"""
Global error handlers.
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from utils.logger import get_logger

logger = get_logger('error_handler')


def setup_error_handlers(app):
    """
    Setup global error handlers.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle bad request errors."""
        return jsonify({
            'success': False,
            'error': 'Bad request',
            'message': str(error.description) if hasattr(error, 'description') else 'Invalid request'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle unauthorized errors."""
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle forbidden errors."""
        return jsonify({
            'success': False,
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle not found errors."""
        return jsonify({
            'success': False,
            'error': 'Not found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle method not allowed errors."""
        return jsonify({
            'success': False,
            'error': 'Method not allowed',
            'message': 'The requested method is not allowed for this resource'
        }), 405
    
    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        """Handle rate limit exceeded errors."""
        return jsonify({
            'success': False,
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.',
            'retry_after': error.description if hasattr(error, 'description') else None
        }), 429
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle marshmallow validation errors."""
        return jsonify({
            'success': False,
            'error': 'Validation error',
            'messages': error.messages
        }), 400
    
    @app.errorhandler(SQLAlchemyError)
    def handle_database_error(error):
        """Handle database errors."""
        logger.error(f"Database error: {str(error)}")
        return jsonify({
            'success': False,
            'error': 'Database error',
            'message': 'An error occurred while accessing the database'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_generic_error(error):
        """Handle all other errors."""
        # Log the error
        logger.error(f"Unhandled error: {str(error)}", exc_info=True)
        
        # If it's an HTTP exception, use its code
        if isinstance(error, HTTPException):
            return jsonify({
                'success': False,
                'error': error.name,
                'message': error.description
            }), error.code
        
        # Generic 500 error
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500
