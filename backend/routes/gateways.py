from flask import Blueprint, jsonify, request
from utils import get_logger, RequestValidator, GatewayStatusSchema
from marshmallow import ValidationError

gateways_bp = Blueprint('gateways', __name__)
logger = get_logger('gateways')

@gateways_bp.route('/status')
def get_gateway_status():
    """Get status of all gateways"""
    try:
        logger.info("Getting gateway status")
        
        # This will be implemented with Docker service in next phase
        # For now, return mock data following the documented structure
        mock_gateways = [
            {
                'name': 'CVSIGDT1',
                'status': 'healthy',
                'port': 8088,
                'trial': {
                    'remaining_hours': 168,
                    'remaining_display': '7 days',
                    'expired': False,
                    'emergency': False,
                    'trial_state': 'TRIAL'
                }
            },
            {
                'name': 'CVSIGDT2', 
                'status': 'healthy',
                'port': 8089,
                'trial': {
                    'remaining_hours': 72,
                    'remaining_display': '3 days',
                    'expired': False,
                    'emergency': False,
                    'trial_state': 'TRIAL'
                }
            },
            {
                'name': 'VIGDS3',
                'status': 'starting',
                'port': 8090,
                'trial': {
                    'remaining_hours': 24,
                    'remaining_display': '1 day',
                    'expired': False,
                    'emergency': True,
                    'trial_state': 'TRIAL'
                }
            }
        ]
        
        logger.info("Gateway status retrieved", gateway_count=len(mock_gateways))
        return jsonify({
            'gateways': mock_gateways,
            'total': len(mock_gateways),
            'timestamp': request._environ.get('REQUEST_START_TIME', 0)
        })
        
    except Exception as e:
        logger.error("Failed to get gateway status", error=str(e))
        return jsonify({'error': 'Failed to retrieve gateway status'}), 500

@gateways_bp.route('/<gateway_name>/status')
def get_single_gateway_status(gateway_name):
    """Get status of a specific gateway"""
    try:
        logger.info("Getting single gateway status", gateway=gateway_name)
        
        # Mock implementation - will be replaced with actual Docker service
        if gateway_name == 'CVSIGDT1':
            gateway_data = {
                'name': 'CVSIGDT1',
                'status': 'healthy',
                'port': 8088,
                'trial': {
                    'remaining_hours': 168,
                    'remaining_display': '7 days',
                    'expired': False,
                    'emergency': False,
                    'trial_state': 'TRIAL'
                }
            }
            return jsonify(gateway_data)
        else:
            logger.warning("Gateway not found", gateway=gateway_name)
            return jsonify({'error': 'Gateway not found'}), 404
            
    except Exception as e:
        logger.error("Failed to get gateway status", gateway=gateway_name, error=str(e))
        return jsonify({'error': 'Failed to retrieve gateway status'}), 500

@gateways_bp.route('/<gateway_name>/restart', methods=['POST'])
def restart_gateway(gateway_name):
    """Restart a specific gateway container"""
    try:
        logger.info("Restarting gateway", gateway=gateway_name)
        
        # Mock implementation - will be replaced with actual Docker service
        logger.info("Gateway restart initiated", gateway=gateway_name)
        return jsonify({
            'message': f'Gateway {gateway_name} restart initiated',
            'gateway': gateway_name,
            'action': 'restart'
        })
        
    except Exception as e:
        logger.error("Failed to restart gateway", gateway=gateway_name, error=str(e))
        return jsonify({'error': 'Failed to restart gateway'}), 500

@gateways_bp.route('/list')
def list_gateways():
    """List all available gateways"""
    try:
        logger.info("Listing all gateways")
        
        # Mock implementation
        gateways = ['CVSIGDT1', 'CVSIGDT2', 'VIGDS3', 'VIGDS4', 'VIGDEV', 'VIGSVC', 'VIGVIS']
        
        return jsonify({
            'gateways': gateways,
            'count': len(gateways)
        })
        
    except Exception as e:
        logger.error("Failed to list gateways", error=str(e))
        return jsonify({'error': 'Failed to list gateways'}), 500