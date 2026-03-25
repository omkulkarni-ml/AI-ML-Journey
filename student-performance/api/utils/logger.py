"""
Logging configuration.
"""
import logging
import sys
from datetime import datetime
import structlog


def get_logger(name):
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        structlog.BoundLogger: Structured logger
    """
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    return structlog.get_logger(name)


def setup_logging(app):
    """
    Setup logging for Flask application.
    
    Args:
        app: Flask application instance
    """
    # Remove default handlers
    app.logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler to app logger
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    # Log startup
    app.logger.info(f"Application started at {datetime.utcnow().isoformat()}")


class RequestLogger:
    """Middleware to log HTTP requests."""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger('request')
    
    def __call__(self, environ, start_response):
        request_start = datetime.utcnow()
        
        def logging_start_response(status, headers, exc_info=None):
            request_end = datetime.utcnow()
            duration = (request_end - request_start).total_seconds()
            
            self.logger.info(
                "Request completed",
                method=environ.get('REQUEST_METHOD'),
                path=environ.get('PATH_INFO'),
                status=status.split()[0],
                duration_ms=round(duration * 1000, 2),
                user_agent=environ.get('HTTP_USER_AGENT'),
                remote_addr=environ.get('REMOTE_ADDR')
            )
            
            return start_response(status, headers, exc_info)
        
        return self.app(environ, logging_start_response)
