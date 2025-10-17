from flask import Blueprint, jsonify, request
from utils import get_logger, SystemHealthSchema
import psutil
import time
import docker
from datetime import datetime

system_bp = Blueprint('system', __name__)
logger = get_logger('system')

@system_bp.route('/health')
def get_system_health():
    """Get comprehensive system health information"""
    try:
        logger.info("Getting system health")
        
        # Get system metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Get Docker status
        docker_status = 'healthy'
        container_count = 0
        try:
            client = docker.from_env()
            containers = client.containers.list()
            container_count = len(containers)
        except Exception as e:
            logger.warning("Failed to connect to Docker", error=str(e))
            docker_status = 'unhealthy'
        
        health_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'cpu_usage': cpu_usage,
            'memory_usage': memory.percent,
            'memory_total': memory.total,
            'memory_available': memory.available,
            'disk_usage': (disk.used / disk.total) * 100,
            'disk_total': disk.total,
            'disk_free': disk.free,
            'docker_status': docker_status,
            'container_count': container_count,
            'uptime': time.time() - psutil.boot_time()
        }
        
        logger.info("System health retrieved", 
                   cpu=cpu_usage, 
                   memory=memory.percent, 
                   docker=docker_status)
        
        return jsonify(health_data)
        
    except Exception as e:
        logger.error("Failed to get system health", error=str(e))
        return jsonify({'error': 'Failed to retrieve system health'}), 500

@system_bp.route('/info')
def get_system_info():
    """Get basic system information"""
    try:
        logger.info("Getting system info")
        
        info = {
            'hostname': psutil.disk_usage('/').total,  # Placeholder
            'platform': psutil.os.name,
            'python_version': f"{psutil.sys.version_info.major}.{psutil.sys.version_info.minor}",
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'disk_total': psutil.disk_usage('/').total
        }
        
        return jsonify(info)
        
    except Exception as e:
        logger.error("Failed to get system info", error=str(e))
        return jsonify({'error': 'Failed to retrieve system info'}), 500

@system_bp.route('/logs')
def get_system_logs():
    """Get recent system logs"""
    try:
        # Validate query parameters
        lines = request.args.get('lines', 100, type=int)
        level = request.args.get('level', 'INFO')
        
        if lines > 1000:
            lines = 1000  # Limit to prevent memory issues
            
        logger.info("Getting system logs", lines=lines, level=level)
        
        # Mock implementation - will be replaced with actual log reading
        mock_logs = [
            {
                'timestamp': datetime.utcnow().isoformat(),
                'level': 'INFO',
                'component': 'gateway-monitor',
                'message': 'Gateway status check completed',
                'details': {'gateways_checked': 7, 'healthy': 6, 'unhealthy': 1}
            },
            {
                'timestamp': datetime.utcnow().isoformat(),
                'level': 'WARNING',
                'component': 'trial-monitor',
                'message': 'Gateway trial period low',
                'details': {'gateway': 'VIGDS3', 'remaining_hours': 24}
            }
        ]
        
        return jsonify({
            'logs': mock_logs,
            'total': len(mock_logs),
            'filters': {'lines': lines, 'level': level}
        })
        
    except Exception as e:
        logger.error("Failed to get system logs", error=str(e))
        return jsonify({'error': 'Failed to retrieve logs'}), 500