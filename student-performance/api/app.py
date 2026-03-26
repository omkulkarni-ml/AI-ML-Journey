"""
Flask API application for Student Performance Predictor.
"""
import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routes
from routes import features_bp, predict_bp, auth_bp, history_bp
from ml.model import get_model

# Import models and utilities
from models import init_db
from middleware import setup_security, setup_rate_limiting, setup_error_handlers, check_token_blacklist
from utils.logger import setup_logging, get_logger

# Initialize logger
logger = get_logger('app')


def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load configuration
    env = config_name or os.environ.get('FLASK_ENV', 'development')
    
    # Base configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_SORT_KEYS'] = False
    
    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', app.config['SECRET_KEY'])
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'error'
    
    # Database Configuration - use absolute path for SQLite
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Use absolute path for SQLite to avoid path issues
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'instance', 'student_performance.db')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # CORS Configuration - allow origins from environment or use defaults
    allowed_origins = os.environ.get('ALLOWED_ORIGINS', '')
    if allowed_origins:
        app.config['ALLOWED_ORIGINS'] = [origin.strip() for origin in allowed_origins.split(',')]
    else:
        app.config['ALLOWED_ORIGINS'] = [
            'http://localhost:5173',
            'http://localhost:3000',
            'http://127.0.0.1:5173'
        ]
    
    # Environment specific config
    if env == 'production':
        app.config['DEBUG'] = False
        app.config['TESTING'] = False
    elif env == 'testing':
        app.config['DEBUG'] = True
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    else:
        app.config['DEBUG'] = True
        app.config['TESTING'] = False
    
    # Initialize extensions
    jwt = JWTManager(app)
    
    # JWT token blacklist check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return check_token_blacklist(jwt_header, jwt_payload)
    
    # Initialize database
    init_db(app)
    
    # Setup security middleware
    setup_security(app)
    
    # Setup rate limiting
    setup_rate_limiting(app)
    
    # Setup error handlers
    setup_error_handlers(app)
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(features_bp, url_prefix='/api')
    app.register_blueprint(predict_bp, url_prefix='/api')
    app.register_blueprint(history_bp, url_prefix='/api')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        try:
            model = get_model()
            model_info = model.get_model_info()
            
            return jsonify({
                'success': True,
                'data': {
                    'status': 'healthy',
                    'model_loaded': model_info['loaded'],
                    'model_type': model_info['model_type'],
                    'timestamp': __import__('datetime').datetime.utcnow().isoformat()
                }
            })
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Service unhealthy',
                'message': str(e)
            }), 503
    
    # Model info endpoint
    @app.route('/api/model/info', methods=['GET'])
    def model_info():
        """Get model metadata."""
        try:
            model = get_model()
            info = model.get_model_info()
            
            return jsonify({
                'success': True,
                'data': info
            })
        except Exception as e:
            logger.error(f"Model info error: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Failed to get model info'
            }), 500
    
    logger.info(f"Application initialized in {env} mode")
    
    return app


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
