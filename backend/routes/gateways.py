from flask import Blueprint, jsonify, request
from utils import get_logger, RequestValidator, GatewayStatusSchema
from marshmallow import ValidationError
from services.docker_service import DockerService
from services.gateway_service import GatewayService
import os

gateways_bp = Blueprint('gateways', __name__)
logger = get_logger('gateways')

# Global service instances - will be initialized when first needed
docker_service = None
gateway_service = None

def get_gateway_service():
    """Get or initialize the gateway service"""
    global docker_service, gateway_service
    
    if gateway_service is None:
        docker_service = DockerService()
        gateway_service = GatewayService(docker_service)
        
        # Set host IP from environment or default to localhost
        host_ip = os.getenv('HOST_IP', 'localhost')
        gateway_service.set_host_ip(host_ip)
        
        logger.info("Gateway services initialized", host_ip=host_ip)
    
    return gateway_service

@gateways_bp.route('/status')
def get_gateway_status():
    """Get status of all gateways"""
    try:
        logger.info("Getting gateway status")
        
        gateway_service = get_gateway_service()
        gateways = gateway_service.get_all_gateways()
        
        logger.info("Gateway status retrieved", gateway_count=len(gateways))
        return jsonify({
            'gateways': gateways,
            'total': len(gateways),
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
        
        gateway_service = get_gateway_service()
        gateway_data = gateway_service.get_gateway_by_name(gateway_name)
        
        if gateway_data:
            logger.info("Gateway status retrieved", gateway=gateway_name)
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
        
        gateway_service = get_gateway_service()
        success, message = gateway_service.restart_gateway(gateway_name)
        
        if success:
            logger.info("Gateway restart successful", gateway=gateway_name)
            return jsonify({
                'message': message,
                'gateway': gateway_name,
                'action': 'restart',
                'success': True
            })
        else:
            logger.error("Gateway restart failed", gateway=gateway_name, message=message)
            return jsonify({
                'error': message,
                'gateway': gateway_name,
                'action': 'restart',
                'success': False
            }), 400
        
    except Exception as e:
        logger.error("Failed to restart gateway", gateway=gateway_name, error=str(e))
        return jsonify({'error': 'Failed to restart gateway'}), 500

@gateways_bp.route('/list')
def list_gateways():
    """List all available gateways"""
    try:
        logger.info("Listing all gateways")
        
        gateway_service = get_gateway_service()
        all_gateways = gateway_service.get_all_gateways()
        
        # Extract just the names and basic info
        gateway_list = []
        for gateway in all_gateways:
            gateway_list.append({
                'name': gateway['name'],
                'port': gateway.get('port'),
                'status': gateway.get('status'),
                'container_status': gateway.get('container_status')
            })
        
        logger.info("Gateway list retrieved", gateway_count=len(gateway_list))
        return jsonify({
            'gateways': gateway_list,
            'count': len(gateway_list)
        })
        
    except Exception as e:
        logger.error("Failed to list gateways", error=str(e))
        return jsonify({'error': 'Failed to list gateways'}), 500

@gateways_bp.route('/<gateway_name>/logs')
def get_gateway_logs(gateway_name):
    """Get logs from a specific gateway container"""
    try:
        logger.info("Getting gateway logs", gateway=gateway_name)
        
        # Get number of lines from query parameter, default to 100
        lines = request.args.get('lines', 100, type=int)
        
        gateway_service = get_gateway_service()
        logs = gateway_service.get_gateway_logs(gateway_name, lines)
        
        logger.info("Gateway logs retrieved", gateway=gateway_name, lines=lines)
        return jsonify({
            'gateway': gateway_name,
            'logs': logs,
            'lines_requested': lines
        })
        
    except Exception as e:
        logger.error("Failed to get gateway logs", gateway=gateway_name, error=str(e))
        return jsonify({'error': 'Failed to retrieve gateway logs'}), 500

@gateways_bp.route('/ping', methods=['POST'])
def ping_gateway():
    """Test connectivity between gateways"""
    try:
        data = request.get_json()
        source_gateway = data.get('source')
        target_gateway = data.get('target')
        
        if not source_gateway or not target_gateway:
            return jsonify({'error': 'Both source and target gateways are required'}), 400
            
        logger.info("Testing gateway connectivity", source=source_gateway, target=target_gateway)
        
        gateway_service = get_gateway_service()
        result = gateway_service.ping_gateway(source_gateway, target_gateway)
        
        logger.info("Gateway ping completed", 
                   source=source_gateway, 
                   target=target_gateway, 
                   success=result.get('success', False))
        
        return jsonify(result)
        
    except Exception as e:
        logger.error("Failed to ping gateway", error=str(e))
        return jsonify({'error': 'Failed to ping gateway'}), 500

@gateways_bp.route('/connectivity')
def test_connectivity():
    """Test connectivity between all configured gateway connections"""
    try:
        logger.info("Testing all gateway connections")
        
        gateway_service = get_gateway_service()
        results = gateway_service.test_all_connections()
        
        logger.info("Gateway connectivity test completed", tested_connections=len(results))
        return jsonify({
            'results': results,
            'total_tests': len(results),
            'timestamp': request._environ.get('REQUEST_START_TIME', 0)
        })
        
    except Exception as e:
        logger.error("Failed to test connectivity", error=str(e))
        return jsonify({'error': 'Failed to test connectivity'}), 500