#!/usr/bin/env python3
"""
Simple test script for gateway ping functionality without complex dependencies
"""
import os
import sys

def get_gateway_config(gateway_name):
    """Get gateway configuration from env files"""
    try:
        env_file_path = f"/opt/firebox/config/gateways/{gateway_name}.env"
        
        if not os.path.exists(env_file_path):
            print(f"Gateway config file not found: {env_file_path}")
            return None
        
        config = {}
        with open(env_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value
        
        # Extract relevant information
        return {
            'name': gateway_name,
            'hostname': config.get('CONTAINER_HOSTNAME', gateway_name.lower()),
            'http_port': config.get('HTTP_PORT'),
            'service_name': config.get('SERVICE_NAME', gateway_name.lower())
        }
        
    except Exception as e:
        print(f"Failed to get gateway config for {gateway_name}: {e}")
        return None

def get_configured_connections():
    """Get all configured gateway connections"""
    expected_connections = [
        # VIGVIS connects to all others
        {'source': 'VIGVIS', 'target': 'CVSIGDT1'},
        {'source': 'VIGVIS', 'target': 'CVSIGDT2'},
        {'source': 'VIGVIS', 'target': 'VIGDS3'},
        {'source': 'VIGVIS', 'target': 'VIGDS4'},
        {'source': 'VIGVIS', 'target': 'VIGDEV'},
        {'source': 'VIGVIS', 'target': 'VIGSVC'},
        
        # Development and Service connect to VIGVIS
        {'source': 'VIGDEV', 'target': 'VIGVIS'},
        {'source': 'VIGSVC', 'target': 'VIGVIS'},
        
        # Data collection gateways connect to Service
        {'source': 'CVSIGDT1', 'target': 'VIGSVC'},
        {'source': 'CVSIGDT2', 'target': 'VIGSVC'},
        {'source': 'VIGDS3', 'target': 'VIGSVC'},
        {'source': 'VIGDS4', 'target': 'VIGSVC'},
    ]
    
    return expected_connections

def test_gateway_config():
    """Test gateway configuration loading"""
    print("🔥 Testing Gateway Configuration")
    print("=" * 50)
    
    # Test a few gateway configs
    test_gateways = ['VIGVIS', 'CVSIGDT1', 'VIGDEV', 'VIGSVC']
    
    for gateway in test_gateways:
        config = get_gateway_config(gateway)
        if config:
            print(f"\n✅ {gateway} config loaded:")
            print(f"   Hostname: {config['hostname']}")
            print(f"   HTTP Port: {config['http_port']}")
            print(f"   Service Name: {config['service_name']}")
        else:
            print(f"\n❌ Failed to load {gateway} config")
    
    # Test connections
    print(f"\n🌐 Configured Connections:")
    print("=" * 30)
    connections = get_configured_connections()
    
    for i, conn in enumerate(connections, 1):
        print(f"{i:2d}. {conn['source']} → {conn['target']}")
    
    print(f"\nTotal connections configured: {len(connections)}")

if __name__ == "__main__":
    test_gateway_config()