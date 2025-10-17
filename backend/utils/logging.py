import os
import sys
import structlog
from datetime import datetime
from flask import g, request
import logging.config

def setup_logging(log_level='INFO', log_format='json', log_dir=None):
    """Setup structured logging with file and console handlers"""
    
    # Use environment variable or default
    if log_dir is None:
        log_dir = os.environ.get('LOG_DIR', './logs')
    
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="ISO"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if log_format == 'json' else structlog.dev.ConsoleRenderer(),
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Standard logging configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'json': {
                'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
            },
            'console': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': log_level,
                'formatter': 'console' if log_format != 'json' else 'json',
                'stream': sys.stdout
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': log_level,
                'formatter': 'json',
                'filename': os.path.join(log_dir, 'firebox.log'),
                'mode': 'a'
            },
            'error_file': {
                'class': 'logging.FileHandler',
                'level': 'ERROR',
                'formatter': 'json',
                'filename': os.path.join(log_dir, 'error.log'),
                'mode': 'a'
            }
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file', 'error_file'],
                'level': log_level,
                'propagate': False
            },
            'werkzeug': {
                'handlers': ['console', 'file'],
                'level': 'WARNING',
                'propagate': False
            }
        }
    }
    
    logging.config.dictConfig(logging_config)
    
    return structlog.get_logger()

def get_logger(name=None):
    """Get a structured logger instance"""
    return structlog.get_logger(name)

def log_request_info():
    """Log request information for debugging"""
    logger = get_logger("request")
    logger.info(
        "Request received",
        method=request.method,
        path=request.path,
        remote_addr=request.remote_addr,
        user_agent=request.headers.get('User-Agent', 'Unknown')
    )

def log_response_info(response):
    """Log response information"""
    logger = get_logger("response")
    logger.info(
        "Response sent",
        status_code=response.status_code,
        content_length=response.content_length
    )
    return response