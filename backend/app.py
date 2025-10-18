import os
from flask import Flask, jsonify, request, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

from config import config
from utils import setup_logging, get_logger, log_request_info, log_response_info

# Prometheus metrics
REQUEST_COUNT = Counter('flask_requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('flask_request_duration_seconds', 'Request latency', ['method', 'endpoint'])

def create_app(config_name=None):
    """Application factory function"""
    
    # Determine configuration
    config_name = config_name or os.environ.get('FLASK_CONFIG', 'default')
    
    # Create Flask app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Setup logging
    logger = setup_logging(
        log_level=app.config['LOG_LEVEL'],
        log_format=app.config['LOG_FORMAT'],
        log_dir=app.config['LOG_DIR']
    )
    
    logger.info("Starting Firebox Backend", config=config_name)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Register request/response logging
    @app.before_request
    def before_request():
        g.start_time = time.time()
        log_request_info()
    
    @app.after_request
    def after_request(response):
        # Record metrics
        duration = time.time() - g.start_time
        REQUEST_COUNT.labels(method=request.method, endpoint=request.endpoint, status=response.status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=request.endpoint).observe(duration)
        
        # Log response
        log_response_info(response)
        return response
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint for Docker and load balancers"""
        try:
            # Check database connection
            db.engine.execute('SELECT 1')
            return jsonify({
                'status': 'healthy',
                'timestamp': time.time(),
                'version': '1.0.0',
                'database': 'connected'
            }), 200
        except Exception as e:
            logger.error("Health check failed", error=str(e))
            return jsonify({
                'status': 'unhealthy',
                'timestamp': time.time(),
                'error': str(e)
            }), 503
    
    # Metrics endpoint for Prometheus
    @app.route('/metrics')
    def metrics():
        """Prometheus metrics endpoint"""
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.warning("404 Not Found", path=request.path, method=request.method)
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error("500 Internal Server Error", error=str(error), path=request.path)
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(ValidationError)
    def validation_error(error):
        logger.warning("Validation Error", error=str(error), path=request.path)
        return jsonify({'error': 'Validation error', 'details': str(error)}), 400
    
    # Register blueprints
    from routes.gateways import gateways_bp
    from routes.trial import trial_bp
    
    app.register_blueprint(gateways_bp, url_prefix='/api/gateways')
    app.register_blueprint(trial_bp, url_prefix='/api/trial')
    
    return app

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Import after app creation to avoid circular imports
from marshmallow import ValidationError

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)