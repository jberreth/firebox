#!/bin/bash
# =============================================================================
# Firebox Gateway Stack Management Script
# Provides easy management of the Ignition gateway Docker Compose stack
# =============================================================================

set -euo pipefail

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/docker-compose.yml"
ENV_FILE="${SCRIPT_DIR}/.env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO:${NC} $1"
}

# Function to check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info &> /dev/null; then
        error "Docker daemon is not running"
        exit 1
    fi
    
    # Check if compose file exists
    if [[ ! -f "$COMPOSE_FILE" ]]; then
        error "Docker Compose file not found: $COMPOSE_FILE"
        exit 1
    fi
    
    # Check if env file exists
    if [[ ! -f "$ENV_FILE" ]]; then
        warn ".env file not found: $ENV_FILE"
        warn "Creating default .env file..."
        create_default_env
    fi
    
    log "Prerequisites check passed"
}

# Function to create default .env file
create_default_env() {
    cat > "$ENV_FILE" << 'EOF'
# =============================================================================
# Firebox Environment Configuration
# =============================================================================

# Network Configuration
HOST_IP=localhost
LOG_LEVEL=INFO
TZ=America/Boise

# Database Configuration
DB_NAME=firebox
DB_USER=firebox
DB_PASSWORD=secure_password_change_me

# Security
JWT_SECRET=your_jwt_secret_change_me

# Selenium Configuration (for trial reset)
SELENIUM_HEADLESS=true
SELENIUM_TIMEOUT=30

# Logging
LOG_FORMAT=json
EOF
    
    info "Created default .env file. Please review and update the configuration."
}

# Function to show status of all services
show_status() {
    log "Checking gateway stack status..."
    
    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" ps
    else
        docker compose -f "$COMPOSE_FILE" ps
    fi
}

# Function to start all services
start_all() {
    log "Starting complete gateway stack..."
    
    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" up -d
    else
        docker compose -f "$COMPOSE_FILE" up -d
    fi
    
    log "Gateway stack started. Use 'show_status' to check service status."
}

# Function to start specific gateways
start_gateways() {
    local gateways=("$@")
    
    if [[ ${#gateways[@]} -eq 0 ]]; then
        log "Starting all gateways..."
        gateways=("vigvis" "cvsigdt1" "cvsigdt2" "vigds3" "vigds4" "vigdev" "vigsvc" "vigsvr")
    else
        log "Starting specific gateways: ${gateways[*]}"
    fi
    
    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" up -d "${gateways[@]}"
    else
        docker compose -f "$COMPOSE_FILE" up -d "${gateways[@]}"
    fi
}

# Function to stop all services
stop_all() {
    log "Stopping complete gateway stack..."
    
    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" down
    else
        docker compose -f "$COMPOSE_FILE" down
    fi
    
    log "Gateway stack stopped."
}

# Function to stop specific gateways
stop_gateways() {
    local gateways=("$@")
    
    if [[ ${#gateways[@]} -eq 0 ]]; then
        error "Please specify gateway names to stop"
        exit 1
    fi
    
    log "Stopping gateways: ${gateways[*]}"
    
    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" stop "${gateways[@]}"
    else
        docker compose -f "$COMPOSE_FILE" stop "${gateways[@]}"
    fi
}

# Function to restart specific gateways
restart_gateways() {
    local gateways=("$@")
    
    if [[ ${#gateways[@]} -eq 0 ]]; then
        log "Restarting all gateways..."
        gateways=("vigvis" "cvsigdt1" "cvsigdt2" "vigds3" "vigds4" "vigdev" "vigsvc" "vigsvr")
    else
        log "Restarting specific gateways: ${gateways[*]}"
    fi
    
    if command -v docker-compose &> /dev/null; then
        docker-compose -f "$COMPOSE_FILE" restart "${gateways[@]}"
    else
        docker compose -f "$COMPOSE_FILE" restart "${gateways[@]}"
    fi
}

# Function to show logs
show_logs() {
    local service="$1"
    local tail_lines="${2:-100}"
    
    if [[ -z "$service" ]]; then
        log "Showing logs for all services (last $tail_lines lines)..."
        if command -v docker-compose &> /dev/null; then
            docker-compose -f "$COMPOSE_FILE" logs --tail="$tail_lines"
        else
            docker compose -f "$COMPOSE_FILE" logs --tail="$tail_lines"
        fi
    else
        log "Showing logs for $service (last $tail_lines lines)..."
        if command -v docker-compose &> /dev/null; then
            docker-compose -f "$COMPOSE_FILE" logs --tail="$tail_lines" "$service"
        else
            docker compose -f "$COMPOSE_FILE" logs --tail="$tail_lines" "$service"
        fi
    fi
}

# Function to clean up (remove containers, volumes, networks)
cleanup() {
    warn "This will remove all containers, volumes, and networks for the gateway stack."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log "Cleaning up gateway stack..."
        
        if command -v docker-compose &> /dev/null; then
            docker-compose -f "$COMPOSE_FILE" down -v --remove-orphans
        else
            docker compose -f "$COMPOSE_FILE" down -v --remove-orphans
        fi
        
        log "Cleanup completed."
    else
        info "Cleanup cancelled."
    fi
}

# Function to show help
show_help() {
    cat << EOF
🔥 Firebox Gateway Stack Management

USAGE:
    $0 COMMAND [ARGS...]

COMMANDS:
    start                   Start all services (infrastructure + gateways)
    start-gateways [names]  Start only gateways (all or specific ones)
    stop                    Stop all services
    stop-gateways <names>   Stop specific gateways
    restart [names]         Restart gateways (all or specific ones)
    status                  Show status of all services
    logs [service] [lines]  Show logs (default: all services, 100 lines)
    cleanup                 Remove all containers, volumes, and networks
    check                   Check prerequisites
    help                    Show this help message

GATEWAY NAMES:
    vigvis cvsigdt1 cvsigdt2 vigds3 vigds4 vigdev vigsvc vigsvr

EXAMPLES:
    $0 start                        # Start complete stack
    $0 start-gateways vigvis vigdev # Start only VIGVIS and VIGDEV
    $0 restart vigvis               # Restart VIGVIS gateway
    $0 logs vigvis 50               # Show last 50 log lines for VIGVIS
    $0 status                       # Show status of all services

CONFIGURATION:
    Edit .env file to configure environment variables
    Gateway configurations are in config/gateways/*.env
EOF
}

# Main script logic
main() {
    case "${1:-help}" in
        "start")
            check_prerequisites
            start_all
            ;;
        "start-gateways")
            check_prerequisites
            shift
            start_gateways "$@"
            ;;
        "stop")
            stop_all
            ;;
        "stop-gateways")
            shift
            stop_gateways "$@"
            ;;
        "restart")
            check_prerequisites
            shift
            restart_gateways "$@"
            ;;
        "status")
            show_status
            ;;
        "logs")
            shift
            show_logs "${1:-}" "${2:-100}"
            ;;
        "cleanup")
            cleanup
            ;;
        "check")
            check_prerequisites
            log "All checks passed!"
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            error "Unknown command: $1"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Run the main function with all arguments
main "$@"