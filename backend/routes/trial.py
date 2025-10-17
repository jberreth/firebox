from flask import Blueprint, jsonify, request
from services.trial_reset_service import TrialResetService
from services.gateway_service import GatewayService
from services.docker_service import DockerService
from utils import get_logger, RequestValidator, TrialResetRequestSchema
from marshmallow import ValidationError
import os

trial_bp = Blueprint('trial', __name__)
logger = get_logger('trial')

# Global service instances
trial_reset_service = None
gateway_service = None

def get_trial_service():
    """Get or initialize the trial reset service"""
    global trial_reset_service, gateway_service
    
    if trial_reset_service is None:
        host_ip = os.getenv('HOST_IP', 'localhost')
        headless = os.getenv('SELENIUM_HEADLESS', 'true').lower() == 'true'
        
        trial_reset_service = TrialResetService(host_ip=host_ip, headless=headless)
        
        # Also initialize gateway service for getting gateway info
        if gateway_service is None:
            docker_service = DockerService()
            gateway_service = GatewayService(docker_service)
            gateway_service.set_host_ip(host_ip)
        
        logger.info("Trial services initialized", host_ip=host_ip, headless=headless)
    
    return trial_reset_service, gateway_service

@trial_bp.route('/reset/<gateway_name>', methods=['POST'])
def reset_gateway_trial(gateway_name):
    """Reset trial for a specific gateway"""
    try:
        logger.info("Trial reset requested", gateway=gateway_name)
        
        trial_service, gw_service = get_trial_service()
        
        # Get gateway information first
        gateway_info = gw_service.get_gateway_by_name(gateway_name)
        if not gateway_info:
            logger.warning("Gateway not found for trial reset", gateway=gateway_name)
            return jsonify({
                'error': 'Gateway not found',
                'gateway': gateway_name
            }), 404
        
        port = gateway_info.get('port')
        if not port:
            logger.error("Gateway port not available", gateway=gateway_name)
            return jsonify({
                'error': 'Gateway port not available',
                'gateway': gateway_name
            }), 400
        
        # Perform the trial reset
        result = trial_service.reset_gateway_trial(gateway_name, port)
        
        if result['success']:
            logger.info("Trial reset completed successfully", gateway=gateway_name)
            return jsonify(result)
        else:
            logger.error("Trial reset failed", gateway=gateway_name, error=result.get('error'))
            return jsonify(result), 500
        
    except Exception as e:
        logger.error("Trial reset endpoint error", gateway=gateway_name, error=str(e))
        return jsonify({
            'error': 'Trial reset service error',
            'message': str(e),
            'gateway': gateway_name
        }), 500

@trial_bp.route('/status')
def get_trial_status():
    """Get trial status for all gateways"""
    try:
        logger.info("Trial status requested")
        
        _, gw_service = get_trial_service()
        
        # Get all gateways
        all_gateways = gw_service.get_all_gateways()
        
        # Compile trial status summary
        trial_summary = {
            'total_gateways': len(all_gateways),
            'healthy_trials': 0,
            'emergency_trials': 0,
            'expired_trials': 0,
            'unknown_trials': 0,
            'gateways': []
        }
        
        for gateway in all_gateways:
            trial_info = gateway.get('trial', {})
            
            gateway_trial = {
                'name': gateway['name'],
                'port': gateway.get('port'),
                'status': gateway.get('status'),
                'trial': trial_info
            }
            
            trial_summary['gateways'].append(gateway_trial)
            
            # Categorize trial status
            if trial_info.get('expired'):
                trial_summary['expired_trials'] += 1
            elif trial_info.get('emergency'):
                trial_summary['emergency_trials'] += 1
            elif trial_info.get('remaining_hours', 0) > 24:
                trial_summary['healthy_trials'] += 1
            else:
                trial_summary['unknown_trials'] += 1
        
        logger.info("Trial status compiled", 
                   total=trial_summary['total_gateways'],
                   healthy=trial_summary['healthy_trials'],
                   emergency=trial_summary['emergency_trials'],
                   expired=trial_summary['expired_trials'])
        
        return jsonify(trial_summary)
        
    except Exception as e:
        logger.error("Trial status endpoint error", error=str(e))
        return jsonify({
            'error': 'Trial status service error',
            'message': str(e)
        }), 500

@trial_bp.route('/bulk-reset', methods=['POST'])
def bulk_reset_trials():
    """Reset trial periods for multiple gateways"""
    try:
        data = request.get_json()
        gateways = data.get('gateways', [])
        force = data.get('force', False)
        
        if not gateways:
            return jsonify({'error': 'No gateways specified'}), 400
            
        logger.info("Bulk trial reset requested", gateways=gateways, force=force)
        
        # Mock implementation
        results = []
        for gateway in gateways:
            results.append({
                'gateway': gateway,
                'status': 'initiated',
                'message': f'Reset initiated for {gateway}'
            })
        
        return jsonify({
            'message': f'Bulk trial reset initiated for {len(gateways)} gateways',
            'results': results,
            'force': force
        })
        
    except Exception as e:
        logger.error("Failed to perform bulk reset", error=str(e))
        return jsonify({'error': 'Failed to perform bulk reset'}), 500

@trial_bp.route('/automation/status')
def get_automation_status():
    """Get status of trial reset automation service"""
    try:
        logger.info("Getting automation status")
        
        # Mock implementation
        automation_status = {
            'enabled': True,
            'last_check': '2025-10-17T12:00:00Z',
            'check_interval': 300,  # 5 minutes
            'active_resets': 0,
            'total_resets_today': 3,
            'service_status': 'running'
        }
        
        return jsonify(automation_status)
        
    except Exception as e:
        logger.error("Failed to get automation status", error=str(e))
        return jsonify({'error': 'Failed to retrieve automation status'}), 500

@trial_bp.route('/config')
def get_trial_config():
    """Get trial reset service configuration"""
    try:
        host_ip = os.getenv('HOST_IP', 'localhost')
        headless = os.getenv('SELENIUM_HEADLESS', 'true').lower() == 'true'
        timeout = int(os.getenv('RESET_TIMEOUT', '30'))
        username = os.getenv('IGNITION_USERNAME', 'admin')
        
        config = {
            'host_ip': host_ip,
            'headless_mode': headless,
            'reset_timeout': timeout,
            'username': username,
            'service_available': True
        }
        
        return jsonify(config)
        
    except Exception as e:
        logger.error("Trial config endpoint error", error=str(e))
        return jsonify({
            'error': 'Trial config service error',
            'message': str(e)
        }), 500

@trial_bp.route('/check')
def check_trial_requirements():
    """Check if trial reset requirements are met"""
    try:
        logger.info("Checking trial reset requirements")
        
        # Check if Chrome/Chromium is available
        chrome_available = os.path.exists('/usr/bin/google-chrome') or os.path.exists('/usr/bin/chromium-browser')
        
        # Check if Selenium dependencies are available
        try:
            import selenium
            selenium_available = True
        except ImportError:
            selenium_available = False
        
        requirements = {
            'chrome_available': chrome_available,
            'selenium_available': selenium_available,
            'ready_for_reset': chrome_available and selenium_available
        }
        
        logger.info("Trial requirements checked", 
                   chrome=chrome_available,
                   selenium=selenium_available)
        
        return jsonify(requirements)
        
    except Exception as e:
        logger.error("Failed to check trial requirements", error=str(e))
        return jsonify({'error': 'Failed to check requirements'}), 500