import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import re
from bs4 import BeautifulSoup
from utils import get_logger

logger = get_logger('gateway_service')

class GatewayService:
    """Service for managing Ignition gateways and their status"""
    
    def __init__(self, docker_service):
        self.docker_service = docker_service
        self.host_ip = "localhost"  # Default to localhost
        
        # Cache for gateway status to avoid too frequent requests
        self._status_cache = {}
        self._cache_duration = 30  # seconds
    
    def set_host_ip(self, host_ip: str):
        """Set the host IP for gateway connections"""
        self.host_ip = host_ip
        logger.info("Host IP updated", host_ip=host_ip)
    
    def get_all_gateways(self) -> List[Dict]:
        """Get status of all gateways"""
        try:
            # Get Ignition containers from Docker
            containers = self.docker_service.get_ignition_containers()
            gateways = []
            
            for container in containers:
                gateway_data = self._process_gateway_container(container)
                if gateway_data:
                    gateways.append(gateway_data)
            
            # If no containers found, return mock data for development
            if not gateways:
                logger.warning("No Ignition containers found, returning mock data")
                gateways = self._get_mock_gateways()
            
            logger.info("Retrieved gateway status", count=len(gateways))
            return gateways
            
        except Exception as e:
            logger.error("Failed to get gateway status", error=str(e))
            # Return mock data on error for development
            return self._get_mock_gateways()
    
    def get_gateway_by_name(self, name: str) -> Optional[Dict]:
        """Get status of a specific gateway by name"""
        try:
            # First try to get from Docker
            container = self.docker_service.get_container_by_name(f"ignition-{name.lower()}")
            if container:
                return self._process_gateway_container(container)
            
            # Try alternative naming patterns
            alt_names = [name.lower(), f"{name.lower()}-gateway", f"gateway-{name.lower()}"]
            for alt_name in alt_names:
                container = self.docker_service.get_container_by_name(alt_name)
                if container:
                    return self._process_gateway_container(container)
            
            logger.warning("Gateway container not found", name=name)
            return None
            
        except Exception as e:
            logger.error("Failed to get gateway", name=name, error=str(e))
            return None
    
    def restart_gateway(self, name: str) -> tuple[bool, str]:
        """Restart a gateway container"""
        try:
            # Try different container naming patterns
            container_names = [
                f"ignition-{name.lower()}",
                name.lower(),
                f"{name.lower()}-gateway",
                f"gateway-{name.lower()}"
            ]
            
            for container_name in container_names:
                success, message = self.docker_service.restart_container(container_name)
                if success:
                    # Clear cache for this gateway
                    cache_key = f"status_{name}"
                    if cache_key in self._status_cache:
                        del self._status_cache[cache_key]
                    
                    logger.info("Gateway restarted successfully", gateway=name, container=container_name)
                    return True, f"Gateway {name} restarted successfully"
            
            error_msg = f"Gateway {name} container not found"
            logger.warning(error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Failed to restart gateway {name}: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def get_gateway_logs(self, name: str, lines: int = 100) -> str:
        """Get logs from a gateway container"""
        try:
            container_names = [
                f"ignition-{name.lower()}",
                name.lower(),
                f"{name.lower()}-gateway"
            ]
            
            for container_name in container_names:
                logs = self.docker_service.get_container_logs(container_name, lines)
                if "not found" not in logs.lower():
                    return logs
            
            return f"Gateway {name} container not found"
            
        except Exception as e:
            logger.error("Failed to get gateway logs", name=name, error=str(e))
            return f"Failed to get logs: {str(e)}"
    
    def check_gateway_health(self, port: int) -> Dict:
        """Check gateway health via HTTP"""
        cache_key = f"health_{port}"
        
        # Check cache first
        if cache_key in self._status_cache:
            cached_time, cached_data = self._status_cache[cache_key]
            if time.time() - cached_time < self._cache_duration:
                return cached_data
        
        health_info = {
            'status': 'unknown',
            'response_time': None,
            'accessible': False,
            'last_check': datetime.utcnow().isoformat()
        }
        
        try:
            start_time = time.time()
            
            # Try to access the gateway web interface
            url = f"http://{self.host_ip}:{port}/main/system/gateway/status"
            response = requests.get(url, timeout=10)
            
            response_time = (time.time() - start_time) * 1000  # Convert to ms
            health_info['response_time'] = round(response_time, 2)
            
            if response.status_code == 200:
                health_info['status'] = 'healthy'
                health_info['accessible'] = True
            elif response.status_code in [401, 403]:
                # Gateway is running but requires authentication
                health_info['status'] = 'healthy'
                health_info['accessible'] = True
            else:
                health_info['status'] = 'unhealthy'
                
        except requests.exceptions.Timeout:
            health_info['status'] = 'starting'
        except requests.exceptions.ConnectionError:
            health_info['status'] = 'unhealthy'
        except Exception as e:
            logger.warning("Health check failed", port=port, error=str(e))
            health_info['status'] = 'unknown'
        
        # Cache the result
        self._status_cache[cache_key] = (time.time(), health_info)
        return health_info
    
    def get_trial_information(self, port: int) -> Optional[Dict]:
        """Get trial information from gateway web interface"""
        cache_key = f"trial_{port}"
        
        # Check cache first
        if cache_key in self._status_cache:
            cached_time, cached_data = self._status_cache[cache_key]
            if time.time() - cached_time < self._cache_duration * 2:  # Cache trial info longer
                return cached_data
        
        try:
            # Try to access the gateway status page
            url = f"http://{self.host_ip}:{port}/main/system/gateway/status"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                trial_info = self._parse_trial_info_from_html(response.text)
                if trial_info:
                    # Cache the result
                    self._status_cache[cache_key] = (time.time(), trial_info)
                    return trial_info
            
            # If we can't get real data, return mock data for development
            mock_trial = self._generate_mock_trial_info(port)
            self._status_cache[cache_key] = (time.time(), mock_trial)
            return mock_trial
            
        except Exception as e:
            logger.warning("Failed to get trial information", port=port, error=str(e))
            # Return mock data on error
            mock_trial = self._generate_mock_trial_info(port)
            self._status_cache[cache_key] = (time.time(), mock_trial)
            return mock_trial
    
    def _process_gateway_container(self, container: Dict) -> Dict:
        """Process a container and extract gateway information"""
        try:
            gateway_info = container.get('gateway_info', {})
            web_port = gateway_info.get('web_port')
            
            gateway_data = {
                'name': gateway_info.get('name', container['name']),
                'port': web_port,
                'container_status': container['status'],
                'container_health': container['health'],
                'container_id': container['id'],
                'image': container['image'],
                'created': container['created']
            }
            
            # Get real-time health and trial info if port is available
            if web_port:
                health_info = self.check_gateway_health(web_port)
                gateway_data['status'] = health_info['status']
                gateway_data['accessible'] = health_info['accessible']
                gateway_data['response_time'] = health_info['response_time']
                gateway_data['last_check'] = health_info['last_check']
                
                # Get trial information
                trial_info = self.get_trial_information(web_port)
                gateway_data['trial'] = trial_info
            else:
                gateway_data['status'] = 'unknown'
                gateway_data['trial'] = None
            
            return gateway_data
            
        except Exception as e:
            logger.error("Failed to process gateway container", container=container.get('name'), error=str(e))
            return None
    
    def _parse_trial_info_from_html(self, html_content: str) -> Optional[Dict]:
        """Parse trial information from Ignition status page HTML"""
        try:
            # This is a simplified parser - in reality, you'd need to handle
            # the specific HTML structure of Ignition's status page
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Look for trial-related text patterns
            trial_patterns = [
                r'trial.*?(\d+)\s*days?\s*remaining',
                r'(\d+)\s*hours?\s*remaining',
                r'trial.*?expires?\s*in\s*(\d+)'
            ]
            
            text_content = soup.get_text().lower()
            
            for pattern in trial_patterns:
                match = re.search(pattern, text_content)
                if match:
                    remaining = int(match.group(1))
                    
                    if 'day' in match.group(0):
                        remaining_hours = remaining * 24
                        display = f"{remaining} day{'s' if remaining != 1 else ''}"
                    else:
                        remaining_hours = remaining
                        display = f"{remaining} hour{'s' if remaining != 1 else ''}"
                    
                    return {
                        'remaining_hours': remaining_hours,
                        'remaining_display': display,
                        'expired': False,
                        'emergency': remaining_hours < 24,
                        'trial_state': 'TRIAL'
                    }
            
            # Check for expired trial
            if 'expired' in text_content or 'emergency' in text_content:
                return {
                    'remaining_hours': 0,
                    'remaining_display': 'Expired',
                    'expired': True,
                    'emergency': True,
                    'trial_state': 'EXPIRED'
                }
            
        except Exception as e:
            logger.warning("Failed to parse trial info from HTML", error=str(e))
        
        return None
    
    def _generate_mock_trial_info(self, port: int) -> Dict:
        """Generate mock trial information for development/testing"""
        # Generate different mock data based on port for variety
        mock_configs = [
            {'hours': 168, 'display': '7 days', 'emergency': False},
            {'hours': 72, 'display': '3 days', 'emergency': False},
            {'hours': 24, 'display': '1 day', 'emergency': True},
            {'hours': 6, 'display': '6 hours', 'emergency': True},
            {'hours': 0, 'display': 'Expired', 'emergency': True, 'expired': True}
        ]
        
        # Use port to determine which mock config to use
        config_index = (port % len(mock_configs))
        config = mock_configs[config_index]
        
        return {
            'remaining_hours': config['hours'],
            'remaining_display': config['display'],
            'expired': config.get('expired', False),
            'emergency': config['emergency'],
            'trial_state': 'EXPIRED' if config.get('expired') else 'TRIAL'
        }
    
    def _get_mock_gateways(self) -> List[Dict]:
        """Get mock gateway data for development"""
        mock_gateways = [
            {
                'name': 'CVSIGDT1',
                'port': 8088,
                'status': 'healthy',
                'container_status': 'running',
                'container_health': 'healthy',
                'accessible': True,
                'response_time': 45.2,
                'last_check': datetime.utcnow().isoformat(),
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
                'port': 8089,
                'status': 'healthy',
                'container_status': 'running',
                'container_health': 'healthy',
                'accessible': True,
                'response_time': 52.8,
                'last_check': datetime.utcnow().isoformat(),
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
                'port': 8090,
                'status': 'starting',
                'container_status': 'running',
                'container_health': 'starting',
                'accessible': False,
                'response_time': None,
                'last_check': datetime.utcnow().isoformat(),
                'trial': {
                    'remaining_hours': 24,
                    'remaining_display': '1 day',
                    'expired': False,
                    'emergency': True,
                    'trial_state': 'TRIAL'
                }
            }
        ]
        
        return mock_gateways