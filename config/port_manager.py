#!/usr/bin/env python3
"""
Firebox Port Configuration Manager

This utility manages port allocation and configuration for all gateways
and infrastructure services in the Firebox system.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class PortManager:
    """Manages port allocation and configuration for Firebox gateways."""
    
    def __init__(self, config_dir: str = "/opt/firebox/config"):
        self.config_dir = Path(config_dir)
        self.network_config_file = self.config_dir / "network.env"
        
        # Port offset definitions
        self.port_offsets = {
            'http': 0,
            'https': 1, 
            'gan': 2,
            'trace': 3,
            'metrics': 4
        }
        
        # Gateway definitions
        self.gateways = {
            'VIGDEV': {'base_port': 8088, 'description': 'Development Gateway'},
            'VIGVIS': {'base_port': 8188, 'description': 'Visualization Gateway'},
            'VIGSVR': {'base_port': 8288, 'description': 'Server Gateway'},
            'VIGSVC': {'base_port': 8388, 'description': 'Service Gateway'},
            'CVSIGDT1': {'base_port': 8488, 'description': 'CVS Integration Gateway 1'},
            'CVSIGDT2': {'base_port': 8588, 'description': 'CVS Integration Gateway 2'},
            'VIGDS3': {'base_port': 8688, 'description': 'Datacenter Gateway 3'},
            'VIGDS4': {'base_port': 8788, 'description': 'Datacenter Gateway 4'},
        }
        
        # Infrastructure services
        self.infrastructure = {
            'firebox_frontend': 3000,
            'firebox_backend': 5000,
            'prometheus': 9090,
            'grafana': 3001,
            'cadvisor': 8081,  # Changed from 8080 to avoid conflict
            'node_exporter': 9100,
            'traefik_http': 80,
            'traefik_https': 443,
            'traefik_dashboard': 8080,
            'postgres': 5432,
            'redis': 6379
        }

    def get_gateway_ports(self, gateway_name: str) -> Dict[str, int]:
        """Get all port assignments for a specific gateway."""
        if gateway_name not in self.gateways:
            raise ValueError(f"Unknown gateway: {gateway_name}")
        
        base_port = self.gateways[gateway_name]['base_port']
        ports = {}
        
        for service, offset in self.port_offsets.items():
            ports[service] = base_port + offset
            
        return ports

    def get_all_gateway_ports(self) -> Dict[str, Dict[str, int]]:
        """Get port assignments for all gateways."""
        all_ports = {}
        for gateway_name in self.gateways:
            all_ports[gateway_name] = self.get_gateway_ports(gateway_name)
        return all_ports

    def check_port_conflicts(self) -> List[Tuple[str, str, int]]:
        """Check for port conflicts across all services."""
        conflicts = []
        used_ports = {}
        
        # Check gateway ports
        for gateway_name in self.gateways:
            gateway_ports = self.get_gateway_ports(gateway_name)
            for service, port in gateway_ports.items():
                port_key = f"{gateway_name}_{service}"
                if port in used_ports:
                    conflicts.append((port_key, used_ports[port], port))
                else:
                    used_ports[port] = port_key
        
        # Check infrastructure ports
        for service, port in self.infrastructure.items():
            if port in used_ports:
                conflicts.append((service, used_ports[port], port))
            else:
                used_ports[port] = service
                
        return conflicts

    def generate_docker_compose_ports(self, gateway_name: str) -> Dict[str, str]:
        """Generate Docker Compose port mappings for a gateway."""
        gateway_ports = self.get_gateway_ports(gateway_name)
        
        compose_ports = {
            'http': f"{gateway_ports['http']}:8088",
            'https': f"{gateway_ports['https']}:8043", 
            'gan': f"{gateway_ports['gan']}:8060",
            'trace': f"{gateway_ports['trace']}:8088/udp",  # For tracing
            'metrics': f"{gateway_ports['metrics']}:9464"   # Prometheus metrics
        }
        
        return compose_ports

    def generate_gateway_urls(self, gateway_name: str, host_ip: str = "localhost") -> Dict[str, str]:
        """Generate access URLs for a gateway."""
        gateway_ports = self.get_gateway_ports(gateway_name)
        
        urls = {
            'http': f"http://{host_ip}:{gateway_ports['http']}",
            'https': f"https://{host_ip}:{gateway_ports['https']}",
            'metrics': f"http://{host_ip}:{gateway_ports['metrics']}/metrics"
        }
        
        return urls

    def export_port_configuration(self, format: str = "json") -> str:
        """Export complete port configuration in specified format."""
        config = {
            'gateways': self.get_all_gateway_ports(),
            'infrastructure': self.infrastructure,
            'port_offsets': self.port_offsets,
            'conflicts': self.check_port_conflicts()
        }
        
        if format.lower() == "json":
            return json.dumps(config, indent=2)
        elif format.lower() == "env":
            return self._export_as_env_file(config)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _export_as_env_file(self, config: Dict) -> str:
        """Export configuration as environment file format."""
        lines = ["# Generated Port Configuration"]
        
        # Gateway ports
        lines.append("\n# Gateway Ports")
        for gateway, ports in config['gateways'].items():
            for service, port in ports.items():
                lines.append(f"{gateway}_{service.upper()}_PORT={port}")
        
        # Infrastructure ports  
        lines.append("\n# Infrastructure Ports")
        for service, port in config['infrastructure'].items():
            lines.append(f"{service.upper()}_PORT={port}")
            
        return "\n".join(lines)

    def validate_configuration(self) -> bool:
        """Validate the current port configuration."""
        conflicts = self.check_port_conflicts()
        
        if conflicts:
            print("❌ Port conflicts detected:")
            for service1, service2, port in conflicts:
                print(f"  Port {port}: {service1} conflicts with {service2}")
            return False
        else:
            print("✅ No port conflicts detected")
            return True

    def print_port_summary(self):
        """Print a summary of all port assignments."""
        print("🔥 Firebox Port Configuration Summary")
        print("=" * 50)
        
        print("\n📡 Gateway Ports:")
        for gateway_name in self.gateways:
            ports = self.get_gateway_ports(gateway_name)
            desc = self.gateways[gateway_name]['description']
            print(f"  {gateway_name} ({desc}):")
            for service, port in ports.items():
                print(f"    {service.capitalize()}: {port}")
        
        print("\n🏗️ Infrastructure Ports:")
        for service, port in self.infrastructure.items():
            print(f"  {service.replace('_', ' ').title()}: {port}")
        
        conflicts = self.check_port_conflicts()
        if conflicts:
            print("\n⚠️ Port Conflicts:")
            for service1, service2, port in conflicts:
                print(f"  Port {port}: {service1} ↔ {service2}")


def main():
    """Command-line interface for port management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Firebox Port Configuration Manager")
    parser.add_argument("--validate", action="store_true", help="Validate port configuration")
    parser.add_argument("--summary", action="store_true", help="Print port summary")
    parser.add_argument("--export", choices=["json", "env"], help="Export configuration")
    parser.add_argument("--gateway", help="Show ports for specific gateway")
    
    args = parser.parse_args()
    
    port_manager = PortManager()
    
    if args.validate:
        port_manager.validate_configuration()
    elif args.summary:
        port_manager.print_port_summary()
    elif args.export:
        print(port_manager.export_port_configuration(args.export))
    elif args.gateway:
        if args.gateway in port_manager.gateways:
            ports = port_manager.get_gateway_ports(args.gateway)
            print(f"Ports for {args.gateway}:")
            for service, port in ports.items():
                print(f"  {service}: {port}")
        else:
            print(f"Unknown gateway: {args.gateway}")
            print(f"Available gateways: {', '.join(port_manager.gateways.keys())}")
    else:
        port_manager.print_port_summary()


if __name__ == "__main__":
    main()