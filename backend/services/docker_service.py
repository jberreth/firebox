import docker
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import re
from utils import get_logger

logger = get_logger('docker_service')

class DockerService:
    """Service for interacting with Docker containers and inspecting Ignition gateways"""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.error("Failed to initialize Docker client", error=str(e))
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Docker is available"""
        try:
            if self.client:
                self.client.ping()
                return True
        except Exception as e:
            logger.error("Docker is not available", error=str(e))
        return False
    
    def get_all_containers(self) -> List[Dict]:
        """Get all containers with basic information"""
        if not self.is_available():
            return []
        
        try:
            containers = self.client.containers.list(all=True)
            container_info = []
            
            for container in containers:
                info = {
                    'id': container.id[:12],
                    'name': container.name,
                    'status': container.status,
                    'image': container.image.tags[0] if container.image.tags else 'unknown',
                    'created': container.attrs['Created'],
                    'ports': self._extract_ports(container),
                    'labels': container.labels,
                    'health': self._get_container_health(container)
                }
                container_info.append(info)
            
            logger.info("Retrieved container information", count=len(container_info))
            return container_info
            
        except Exception as e:
            logger.error("Failed to get containers", error=str(e))
            return []
    
    def get_ignition_containers(self) -> List[Dict]:
        """Get containers that appear to be Ignition gateways"""
        if not self.is_available():
            return []
        
        try:
            all_containers = self.get_all_containers()
            ignition_containers = []
            
            for container in all_containers:
                # Check if container looks like an Ignition gateway
                if self._is_ignition_container(container):
                    # Add Ignition-specific information
                    container['gateway_info'] = self._get_gateway_info(container)
                    ignition_containers.append(container)
            
            logger.info("Found Ignition containers", count=len(ignition_containers))
            return ignition_containers
            
        except Exception as e:
            logger.error("Failed to get Ignition containers", error=str(e))
            return []
    
    def get_container_by_name(self, name: str) -> Optional[Dict]:
        """Get a specific container by name"""
        if not self.is_available():
            return None
        
        try:
            container = self.client.containers.get(name)
            return {
                'id': container.id[:12],
                'name': container.name,
                'status': container.status,
                'image': container.image.tags[0] if container.image.tags else 'unknown',
                'created': container.attrs['Created'],
                'ports': self._extract_ports(container),
                'labels': container.labels,
                'health': self._get_container_health(container),
                'gateway_info': self._get_gateway_info({'name': container.name, 'ports': self._extract_ports(container)})
            }
        except docker.errors.NotFound:
            logger.warning("Container not found", name=name)
            return None
        except Exception as e:
            logger.error("Failed to get container", name=name, error=str(e))
            return None
    
    def restart_container(self, name: str) -> Tuple[bool, str]:
        """Restart a container by name"""
        if not self.is_available():
            return False, "Docker is not available"
        
        try:
            container = self.client.containers.get(name)
            container.restart()
            logger.info("Container restarted successfully", name=name)
            return True, f"Container {name} restarted successfully"
        except docker.errors.NotFound:
            error_msg = f"Container {name} not found"
            logger.warning(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"Failed to restart container {name}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def get_container_logs(self, name: str, lines: int = 100) -> str:
        """Get logs from a container"""
        if not self.is_available():
            return "Docker is not available"
        
        try:
            container = self.client.containers.get(name)
            logs = container.logs(tail=lines, timestamps=True).decode('utf-8')
            return logs
        except docker.errors.NotFound:
            return f"Container {name} not found"
        except Exception as e:
            logger.error("Failed to get container logs", name=name, error=str(e))
            return f"Failed to get logs: {str(e)}"
    
    def _extract_ports(self, container) -> Dict[str, int]:
        """Extract port mappings from container"""
        ports = {}
        try:
            port_bindings = container.attrs.get('NetworkSettings', {}).get('Ports', {})
            for internal_port, bindings in port_bindings.items():
                if bindings:
                    external_port = int(bindings[0]['HostPort'])
                    port_name = internal_port.split('/')[0]
                    ports[port_name] = external_port
        except Exception as e:
            logger.warning("Failed to extract ports", container=container.name, error=str(e))
        return ports
    
    def _get_container_health(self, container) -> str:
        """Get container health status"""
        try:
            health = container.attrs.get('State', {}).get('Health', {})
            if health:
                return health.get('Status', 'unknown')
            
            # If no health check, determine based on status
            status = container.status
            if status == 'running':
                return 'healthy'
            elif status in ['exited', 'dead']:
                return 'unhealthy'
            else:
                return 'starting'
        except Exception:
            return 'unknown'
    
    def _is_ignition_container(self, container: Dict) -> bool:
        """Determine if a container is likely an Ignition gateway"""
        name = container.get('name', '').lower()
        image = container.get('image', '').lower()
        ports = container.get('ports', {})
        
        # Check for Ignition-like patterns
        ignition_patterns = [
            'ignition', 'gateway', 'cvs', 'vig', 'scada'
        ]
        
        # Check name patterns
        for pattern in ignition_patterns:
            if pattern in name:
                return True
        
        # Check for common Ignition ports
        ignition_ports = [8088, 8043, 8060, 8089, 8090, 8091, 8092, 8093, 8094, 8095]
        for port in ignition_ports:
            if str(port) in ports:
                return True
        
        return False
    
    def _get_gateway_info(self, container: Dict) -> Dict:
        """Get Ignition-specific gateway information"""
        gateway_info = {
            'name': self._extract_gateway_name(container.get('name', '')),
            'web_port': self._get_web_port(container.get('ports', {})),
            'status': 'unknown',
            'trial_info': None
        }
        
        # Try to get additional info from the gateway web interface
        web_port = gateway_info['web_port']
        if web_port:
            gateway_info['status'] = self._check_gateway_status(web_port)
            gateway_info['trial_info'] = self._get_trial_info(web_port)
        
        return gateway_info
    
    def _extract_gateway_name(self, container_name: str) -> str:
        """Extract gateway name from container name"""
        # Remove common prefixes/suffixes
        name = container_name.replace('ignition-', '').replace('-gateway', '')
        return name.upper()
    
    def _get_web_port(self, ports: Dict) -> Optional[int]:
        """Get the web interface port for Ignition"""
        # Common Ignition web ports
        web_ports = ['8088', '8043', '8089', '8090', '8091', '8092', '8093', '8094', '8095']
        
        for port in web_ports:
            if port in ports:
                return ports[port]
        
        return None
    
    def _check_gateway_status(self, port: int) -> str:
        """Check if gateway web interface is accessible"""
        try:
            # Try to access the gateway status page
            url = f"http://localhost:{port}/system/gateway/status"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                return 'healthy'
            else:
                return 'unhealthy'
        except requests.exceptions.Timeout:
            return 'starting'
        except requests.exceptions.ConnectionError:
            return 'unhealthy'
        except Exception as e:
            logger.warning("Failed to check gateway status", port=port, error=str(e))
            return 'unknown'
    
    def _get_trial_info(self, port: int) -> Optional[Dict]:
        """Get trial information from gateway"""
        try:
            # This is a simplified version - in reality, you'd need to parse
            # the actual Ignition web interface or use the gateway API
            url = f"http://localhost:{port}/system/gateway/status"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                # Mock trial info - replace with actual parsing
                return {
                    'remaining_hours': 168,  # 7 days
                    'remaining_display': '7 days',
                    'expired': False,
                    'emergency': False,
                    'trial_state': 'TRIAL'
                }
        except Exception as e:
            logger.warning("Failed to get trial info", port=port, error=str(e))
        
        return None
    
    def exec_command(self, container_name: str, command: str) -> Dict:
        """Execute a command in a Docker container"""
        if not self.is_available():
            return {'success': False, 'error': 'Docker not available'}
        
        try:
            # Get the container
            container = self.client.containers.get(container_name)
            
            if container.status != 'running':
                return {
                    'success': False,
                    'error': f'Container {container_name} is not running (status: {container.status})'
                }
            
            # Execute the command
            logger.info("Executing command in container", container=container_name, command=command)
            result = container.exec_run(command, stdout=True, stderr=True)
            
            success = result.exit_code == 0
            output = result.output.decode('utf-8') if result.output else ''
            
            logger.info("Command execution completed", 
                       container=container_name, 
                       exit_code=result.exit_code,
                       success=success)
            
            return {
                'success': success,
                'exit_code': result.exit_code,
                'output': output,
                'command': command,
                'container': container_name
            }
            
        except docker.errors.NotFound:
            logger.error("Container not found", container=container_name)
            return {
                'success': False,
                'error': f'Container {container_name} not found'
            }
        except Exception as e:
            logger.error("Failed to execute command in container", 
                        container=container_name, 
                        command=command, 
                        error=str(e))
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_container_logs(self, container_name: str, lines: int = 100) -> str:
        """Get logs from a container"""
        if not self.is_available():
            return "Docker not available"
        
        try:
            container = self.client.containers.get(container_name)
            logs = container.logs(tail=lines, timestamps=True).decode('utf-8')
            logger.info("Retrieved container logs", container=container_name, lines=lines)
            return logs
            
        except docker.errors.NotFound:
            logger.error("Container not found for logs", container=container_name)
            return f"Container {container_name} not found"
        except Exception as e:
            logger.error("Failed to get container logs", container=container_name, error=str(e))
            return f"Error retrieving logs: {str(e)}"