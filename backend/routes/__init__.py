from flask import Blueprint
from .gateways import gateways_bp
from .system import system_bp
from .trial import trial_bp

# Main API blueprint
api_bp = Blueprint('api', __name__)

# Register sub-blueprints
api_bp.register_blueprint(gateways_bp, url_prefix='/gateways')
api_bp.register_blueprint(system_bp, url_prefix='/system')
api_bp.register_blueprint(trial_bp, url_prefix='/trial')

@api_bp.route('/')
def api_info():
    """API information endpoint"""
    return {
        'name': 'Firebox API',
        'version': '1.0.0',
        'endpoints': {
            'gateways': '/api/gateways',
            'system': '/api/system',
            'trial': '/api/trial',
            'health': '/health',
            'metrics': '/metrics'
        }
    }