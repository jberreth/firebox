#!/bin/bash
# =============================================================================
# Gateway Connection Topology Summary
# Shows the gateway-to-gateway connection configuration
# =============================================================================

echo "🔥 Firebox Gateway Connection Topology"
echo "========================================"
echo ""

echo "📡 Gateway Network Architecture:"
echo ""
echo "┌─────────────────────────────────────────────────────────────────┐"
echo "│                          VIGVIS (Hub)                          │"
echo "│                     Visualization Gateway                       │"
echo "│                        Port: 8071                              │"
echo "│ ┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐  │"
echo "│ │         │         │         │         │         │         │  │"
echo "└─┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼──┘"
echo "  │         │         │         │         │         │         │"
echo "  v         v         v         v         v         v         │"
echo "┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   │"
echo "│CVSIGDT1│ │CVSIGDT2│ │VIGDS3 │ │VIGDS4 │ │VIGDEV │ │VIGSVC │   │"
echo "│ 8051  │ │ 8052  │ │ 8053  │ │ 8054  │ │ 8070  │ │ 8073  │   │"
echo "└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───────┘ └───┬───┘   │"
echo "    │         │         │         │                     │     │"
echo "    └─────────┼─────────┼─────────┼─────────────────────┘     │"
echo "              │         │         │                           │"
echo "              └─────────┼─────────┘                           │"
echo "                        │                                     │"
echo "                        └─────────────────────────────────────┘"
echo ""
echo "Connection Details:"
echo "==================="

echo ""
echo "🎯 VIGVIS (Visualization Hub) connects to ALL other gateways:"
echo "   • CVSIGDT1 (8051) - CVS Integration 1"
echo "   • CVSIGDT2 (8052) - CVS Integration 2" 
echo "   • VIGDS3 (8053) - Datacenter 3"
echo "   • VIGDS4 (8054) - Datacenter 4"
echo "   • VIGDEV (8070) - Development"
echo "   • VIGSVC (8073) - Service Gateway"

echo ""
echo "🔧 VIGDEV (Development) connects to:"
echo "   • VIGVIS (8071) - Visualization Hub"

echo ""
echo "⚙️  VIGSVC (Service Gateway) connects to:"
echo "   • VIGVIS (8071) - Visualization Hub"

echo ""
echo "📊 CVS Integration Gateways connect to Service:"
echo "   • CVSIGDT1 → VIGSVC (8073)"
echo "   • CVSIGDT2 → VIGSVC (8073)"

echo ""
echo "🏢 Datacenter Gateways connect to Service:"
echo "   • VIGDS3 → VIGSVC (8073)"
echo "   • VIGDS4 → VIGSVC (8073)"

echo ""
echo "🔧 VIGSVR (Server Gateway):"
echo "   • No outgoing connections configured"

echo ""
echo "📋 Configuration Files:"
echo "======================="
for env_file in /opt/firebox/config/gateways/*.env; do
    gateway_name=$(basename "$env_file" .env)
    echo "   • $gateway_name: $(dirname "$env_file")/$(basename "$env_file")"
done

echo ""
echo "🌐 All gateways use IP-based port allocation:"
echo "   • HTTP ports: 8000 + IP last octet"
echo "   • HTTPS ports: 8400 + IP last octet"
echo "   • GAN ports: 8600 + IP last octet"
echo "   • Trace ports: 10000 + IP last octet"
echo "   • Metrics ports: 11000 + IP last octet"