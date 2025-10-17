#!/usr/bin/env python3

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Simple in-memory storage for testing
mock_gateways = [
    {
        'name': 'CVSIGDT1',
        'displayName': 'CVSIGDT1',
        'port': 8088,
        'status': 'healthy',
        'statusColor': 'success',
        'container_status': 'running',
        'container_health': 'healthy',
        'accessible': True,
        'response_time': 45.2,
        'last_check': '2025-10-17T12:30:00Z',
        'lastCheckFormatted': '2m ago',
        'trial': {
            'remaining_hours': 168,
            'remaining_display': '7 days',
            'expired': False,
            'emergency': False,
            'trial_state': 'TRIAL'
        },
        'trialFormatted': {
            'display': '7 days',
            'state': 'TRIAL',
            'emergency': False,
            'expired': False,
            'hours': 168
        },
        'trialColor': 'success',
        'actions': ['view', 'logs', 'restart', 'reset-trial']
    },
    {
        'name': 'CVSIGDT2',
        'displayName': 'CVSIGDT2',
        'port': 8089,
        'status': 'healthy',
        'statusColor': 'success',
        'container_status': 'running',
        'container_health': 'healthy',
        'accessible': True,
        'response_time': 52.8,
        'last_check': '2025-10-17T12:29:00Z',
        'lastCheckFormatted': '3m ago',
        'trial': {
            'remaining_hours': 72,
            'remaining_display': '3 days',
            'expired': False,
            'emergency': False,
            'trial_state': 'TRIAL'
        },
        'trialFormatted': {
            'display': '3 days',
            'state': 'TRIAL',
            'emergency': False,
            'expired': False,
            'hours': 72
        },
        'trialColor': 'success',
        'actions': ['view', 'logs', 'restart', 'reset-trial']
    },
    {
        'name': 'VIGDS3',
        'displayName': 'VIGDS3',
        'port': 8090,
        'status': 'starting',
        'statusColor': 'attention',
        'container_status': 'running',
        'container_health': 'starting',
        'accessible': False,
        'response_time': None,
        'last_check': '2025-10-17T12:28:00Z',
        'lastCheckFormatted': '4m ago',
        'trial': {
            'remaining_hours': 24,
            'remaining_display': '1 day',
            'expired': False,
            'emergency': True,
            'trial_state': 'TRIAL'
        },
        'trialFormatted': {
            'display': '1 day',
            'state': 'TRIAL',
            'emergency': True,
            'expired': False,
            'hours': 24
        },
        'trialColor': 'severe',
        'actions': ['view', 'logs', 'reset-trial']
    }
]

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': '2025-10-17T12:32:00Z',
        'version': '1.0.0'
    })

@app.route('/api/gateways/status')
def get_gateway_status():
    """Get all gateway statuses"""
    # Calculate summary
    summary = {
        'healthy': sum(1 for g in mock_gateways if g['status'] == 'healthy'),
        'unhealthy': sum(1 for g in mock_gateways if g['status'] == 'unhealthy'),
        'starting': sum(1 for g in mock_gateways if g['status'] == 'starting'),
        'unknown': sum(1 for g in mock_gateways if g['status'] == 'unknown'),
        'emergency': sum(1 for g in mock_gateways if g.get('trial', {}).get('emergency', False)),
        'expired': sum(1 for g in mock_gateways if g.get('trial', {}).get('expired', False))
    }
    
    return jsonify({
        'gateways': mock_gateways,
        'total': len(mock_gateways),
        'summary': summary,
        'timestamp': '2025-10-17T12:32:00Z'
    })

@app.route('/api/gateways/<gateway_name>/status')
def get_single_gateway_status(gateway_name):
    """Get status of a specific gateway"""
    gateway = next((g for g in mock_gateways if g['name'] == gateway_name), None)
    if gateway:
        return jsonify(gateway)
    else:
        return jsonify({'error': 'Gateway not found'}), 404

@app.route('/api/gateways/<gateway_name>/restart', methods=['POST'])
def restart_gateway(gateway_name):
    """Restart a specific gateway container"""
    gateway = next((g for g in mock_gateways if g['name'] == gateway_name), None)
    if gateway:
        return jsonify({
            'message': f'Gateway {gateway_name} restart initiated',
            'gateway': gateway_name,
            'action': 'restart',
            'success': True
        })
    else:
        return jsonify({'error': 'Gateway not found'}), 404

@app.route('/api/gateways/list')
def list_gateways():
    """List all available gateways"""
    gateway_list = []
    for gateway in mock_gateways:
        gateway_list.append({
            'name': gateway['name'],
            'port': gateway['port'],
            'status': gateway['status'],
            'container_status': gateway['container_status']
        })
    
    return jsonify({
        'gateways': gateway_list,
        'count': len(gateway_list)
    })

@app.route('/api/gateways/<gateway_name>/logs')
def get_gateway_logs(gateway_name):
    """Get logs from a specific gateway container"""
    lines = int(request.args.get('lines', 100))
    
    mock_logs = f"""
[2025-10-17 12:30:00] INFO  - Ignition Gateway starting up
[2025-10-17 12:30:01] INFO  - Loading modules...
[2025-10-17 12:30:02] INFO  - Web server started on port {8088 + hash(gateway_name) % 10}
[2025-10-17 12:30:03] INFO  - Gateway ready for connections
[2025-10-17 12:31:00] INFO  - Trial period: 168 hours remaining
    """.strip()
    
    return jsonify({
        'gateway': gateway_name,
        'logs': mock_logs,
        'lines_requested': lines
    })

@app.route('/api/trial/status')
def get_trial_status():
    """Get trial status summary"""
    summary = {
        'total_gateways': len(mock_gateways),
        'healthy_trials': sum(1 for g in mock_gateways if not g.get('trial', {}).get('emergency', False) and not g.get('trial', {}).get('expired', False)),
        'emergency_trials': sum(1 for g in mock_gateways if g.get('trial', {}).get('emergency', False)),
        'expired_trials': sum(1 for g in mock_gateways if g.get('trial', {}).get('expired', False)),
        'unknown_trials': 0
    }
    
    return jsonify({
        **summary,
        'summary': summary,
        'gateways': [{
            'name': g['name'],
            'port': g['port'],
            'status': g['status'],
            'trial': g['trial']
        } for g in mock_gateways]
    })

@app.route('/api/trial/reset/<gateway_name>', methods=['POST'])
def reset_gateway_trial(gateway_name):
    """Reset trial for a specific gateway"""
    gateway = next((g for g in mock_gateways if g['name'] == gateway_name), None)
    if gateway:
        return jsonify({
            'success': True,
            'message': f'Trial reset completed successfully for {gateway_name}',
            'gateway': gateway_name,
            'timestamp': '2025-10-17T12:32:00Z',
            'steps_completed': ['navigate_to_gateway', 'authentication_successful', 'navigate_to_trial_reset', 'trial_reset_executed', 'trial_reset_verified']
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Gateway not found',
            'gateway': gateway_name
        }), 404

@app.route('/api/trial/reset/all', methods=['POST'])
def reset_all_trials():
    """Reset trials for all gateways"""
    return jsonify({
        'total_gateways': len(mock_gateways),
        'successful_resets': len(mock_gateways),
        'failed_resets': 0,
        'gateway_results': [{
            'gateway': g['name'],
            'success': True,
            'message': f'Trial reset completed for {g["name"]}'
        } for g in mock_gateways]
    })

@app.route('/api/trial/reset/emergency', methods=['POST'])
def reset_emergency_trials():
    """Reset trials for emergency gateways only"""
    emergency_gateways = [g for g in mock_gateways if g.get('trial', {}).get('emergency', False)]
    
    return jsonify({
        'total_gateways': len(emergency_gateways),
        'successful_resets': len(emergency_gateways),
        'failed_resets': 0,
        'emergency_reset': True,
        'gateway_results': [{
            'gateway': g['name'],
            'success': True,
            'message': f'Emergency trial reset completed for {g["name"]}'
        } for g in emergency_gateways]
    })

if __name__ == '__main__':
    print("🔥 Firebox Backend Test Server Starting...")
    print("📡 Available endpoints:")
    print("   GET  /api/health")
    print("   GET  /api/gateways/status")
    print("   GET  /api/gateways/list")
    print("   POST /api/gateways/{name}/restart")
    print("   GET  /api/gateways/{name}/logs")
    print("   GET  /api/trial/status")
    print("   POST /api/trial/reset/{name}")
    print("   POST /api/trial/reset/all")
    print("   POST /api/trial/reset/emergency")
    print("")
    print("🚀 Server running at http://localhost:5000")
    print("🔄 CORS enabled for frontend integration")
    print("")
    
    app.run(host='0.0.0.0', port=5000, debug=True)