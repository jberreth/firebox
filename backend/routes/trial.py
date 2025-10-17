from flask import Blueprint, jsonify, request
from utils import get_logger, RequestValidator, TrialResetRequestSchema
from marshmallow import ValidationError
import subprocess
import os

trial_bp = Blueprint('trial', __name__)
logger = get_logger('trial')

@trial_bp.route('/reset', methods=['POST'])
def reset_trial():
    """Reset trial period for a gateway using Selenium automation"""
    try:
        # Validate request
        data = RequestValidator.validate_json_request(request, TrialResetRequestSchema)
        gateway_name = data['gateway_name']
        force = data.get('force', False)
        
        logger.info("Trial reset requested", gateway=gateway_name, force=force)
        
        # Mock implementation - will be replaced with actual Selenium service
        logger.info("Trial reset initiated", gateway=gateway_name)
        
        return jsonify({
            'message': f'Trial reset initiated for {gateway_name}',
            'gateway': gateway_name,
            'status': 'initiated',
            'force': force
        })
        
    except ValidationError as e:
        logger.warning("Trial reset validation error", error=str(e))
        return jsonify({'error': 'Validation error', 'details': str(e)}), 400
    except Exception as e:
        logger.error("Failed to reset trial", error=str(e))
        return jsonify({'error': 'Failed to reset trial'}), 500

@trial_bp.route('/status/<gateway_name>')
def get_trial_status(gateway_name):
    """Get detailed trial status for a specific gateway"""
    try:
        logger.info("Getting trial status", gateway=gateway_name)
        
        # Mock implementation
        if gateway_name in ['CVSIGDT1', 'CVSIGDT2', 'VIGDS3']:
            trial_data = {
                'gateway': gateway_name,
                'trial_state': 'TRIAL',
                'remaining_hours': 168 if gateway_name == 'CVSIGDT1' else 72,
                'remaining_display': '7 days' if gateway_name == 'CVSIGDT1' else '3 days',
                'expired': False,
                'emergency': gateway_name == 'VIGDS3',
                'last_reset': '2025-10-10T10:00:00Z',
                'reset_count': 2
            }
            return jsonify(trial_data)
        else:
            return jsonify({'error': 'Gateway not found'}), 404
            
    except Exception as e:
        logger.error("Failed to get trial status", gateway=gateway_name, error=str(e))
        return jsonify({'error': 'Failed to retrieve trial status'}), 500

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