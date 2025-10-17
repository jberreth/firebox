# 🚀 Deployment Guide - Firebox Dashboard v1.0

Complete deployment instructions for development, staging, and production environments.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Ubuntu 20.04+, CentOS 8+, or equivalent Linux distribution
- **Docker**: 20.10+ with Docker Compose 2.0+
- **Memory**: Minimum 4GB RAM, Recommended 8GB+ for full stack
- **Storage**: 20GB available disk space for containers and logs
- **Network**: Ports 3000, 5000, 8080, 9090, 3001 available

### Required Software
```bash
# Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Docker Compose (if not included)
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Node.js 18+ (for development)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python 3.8+ (for development)
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
```

---

## 🛠️ Development Deployment

### Quick Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/firebox-dashboard.git
cd firebox-dashboard

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start development services
docker-compose up -d

# Access services
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000  
# Grafana: http://localhost:3001
# Prometheus: http://localhost:9090
```

### Manual Development Setup
```bash
# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start backend (Terminal 1)
python test_server.py              # Mock data server
# OR
python app.py                      # Full server (requires Docker)

# Frontend setup  
cd frontend
npm install

# Start frontend (Terminal 2)
npm start

# Access development servers
# Frontend: http://localhost:3000
# Backend: http://localhost:5000
```

### Development Configuration
Create `.env` file:
```bash
# Development Environment
NODE_ENV=development
FLASK_ENV=development

# Host Configuration
HOST_IP=localhost
COMPOSE_PROJECT_NAME=firebox-dev

# Service Ports
FRONTEND_PORT=3000
BACKEND_PORT=5000
GRAFANA_PORT=3001
PROMETHEUS_PORT=9090

# Database (optional for development)
DB_HOST=localhost
DB_NAME=firebox_dev
DB_USER=firebox
DB_PASSWORD=dev_password

# Selenium Configuration
SELENIUM_HEADLESS=false            # For debugging
RESET_TIMEOUT=60
IGNITION_USERNAME=admin
IGNITION_PASSWORD=password

# Logging
LOG_LEVEL=DEBUG
LOG_FORMAT=text                    # Human-readable for development
```

---

## 🏗️ Production Deployment

### Production Requirements
- **SSL Certificate**: Valid SSL certificate for HTTPS
- **Domain Name**: Configured domain pointing to server
- **Firewall**: Proper firewall configuration with required ports
- **Monitoring**: Log aggregation and monitoring setup
- **Backup Strategy**: Database and configuration backup plan

### Production Setup
```bash
# Clone repository
git clone https://github.com/yourusername/firebox-dashboard.git
cd firebox-dashboard

# Configure production environment
cp .env.example .env.prod
# Edit .env.prod with production settings

# Build production images
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d

# Verify deployment
docker-compose -f docker-compose.prod.yml ps
```

### Production Environment Configuration
Create `.env.prod`:
```bash
# Production Environment
NODE_ENV=production
FLASK_ENV=production

# Host Configuration
HOST_IP=your-server-ip
DOMAIN=your-domain.com
COMPOSE_PROJECT_NAME=firebox-prod

# Service Ports (internal)
FRONTEND_PORT=3000
BACKEND_PORT=5000
GRAFANA_PORT=3001
PROMETHEUS_PORT=9090

# SSL Configuration
SSL_EMAIL=admin@your-domain.com
SSL_CERT_PATH=/etc/ssl/certs/your-domain.crt
SSL_KEY_PATH=/etc/ssl/private/your-domain.key

# Database Configuration
DB_HOST=postgres
DB_NAME=firebox
DB_USER=firebox
DB_PASSWORD=your_secure_password_here

# Selenium Configuration  
SELENIUM_HEADLESS=true
RESET_TIMEOUT=30
IGNITION_USERNAME=admin
IGNITION_PASSWORD=your_ignition_password

# Security
SECRET_KEY=your_flask_secret_key_here
JWT_SECRET=your_jwt_secret_here

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_DIR=/var/log/firebox

# Monitoring
PROMETHEUS_RETENTION=30d
GRAFANA_ADMIN_PASSWORD=your_grafana_password
```

### Production Docker Compose
Create `docker-compose.prod.yml`:
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - NODE_ENV=production
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`${DOMAIN}`)"
      - "traefik.http.routers.frontend.tls.certresolver=letsencrypt"
      - "traefik.http.services.frontend.loadbalancer.server.port=80"

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    restart: unless-stopped
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ${LOG_DIR}:/app/logs
    depends_on:
      - postgres
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.backend.rule=Host(`${DOMAIN}`) && PathPrefix(`/api`)"
      - "traefik.http.routers.backend.tls.certresolver=letsencrypt"

  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      - POSTGRES_DB=${DB_NAME}
      - POSTGRES_USER=${DB_USER}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups

  traefik:
    image: traefik:v2.10
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./traefik/traefik.yml:/traefik.yml
      - ./traefik/dynamic.yml:/dynamic.yml
      - traefik_ssl:/ssl
    command:
      - --certificatesresolvers.letsencrypt.acme.email=${SSL_EMAIL}
      - --certificatesresolvers.letsencrypt.acme.storage=/ssl/acme.json

  prometheus:
    image: prom/prometheus:latest
    restart: unless-stopped
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - --storage.tsdb.retention.time=${PROMETHEUS_RETENTION}
      - --config.file=/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning

volumes:
  postgres_data:
  prometheus_data:
  grafana_data:
  traefik_ssl:
```

---

## 🌐 Traefik Configuration

### traefik/traefik.yml
```yaml
api:
  dashboard: true
  insecure: false

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entrypoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

providers:
  docker:
    exposedByDefault: false
  file:
    filename: /dynamic.yml

certificatesResolvers:
  letsencrypt:
    acme:
      tlsChallenge: {}
      storage: /ssl/acme.json

log:
  level: INFO

accessLog: {}
```

### traefik/dynamic.yml
```yaml
http:
  middlewares:
    security-headers:
      headers:
        accessControlAllowMethods:
          - GET
          - OPTIONS
          - PUT
          - POST
          - DELETE
        accessControlAllowOriginList:
          - https://your-domain.com
        accessControlMaxAge: 100
        hostsProxyHeaders:
          - "X-Forwarded-Host"
        sslRedirect: true
        stsSeconds: 31536000
        stsIncludeSubdomains: true
        stsPreload: true
        forceSTSHeader: true

tls:
  options:
    default:
      sslProtocols:
        - "TLSv1.2"
        - "TLSv1.3"
      cipherSuites:
        - "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
        - "TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305"
        - "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
```

---

## 📊 Monitoring Setup

### Prometheus Configuration
Create `monitoring/prometheus.yml`:
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "alert_rules.yml"

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'firebox-backend'
    static_configs:
      - targets: ['backend:5000']
    metrics_path: '/api/metrics'

  - job_name: 'docker'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093
```

### Grafana Dashboard
Import dashboard configuration from `monitoring/grafana/dashboards/firebox.json`.

---

## 🔒 Security Configuration

### Firewall Setup (UFW)
```bash
# Enable firewall
sudo ufw enable

# Allow SSH
sudo ufw allow ssh

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow development ports (development only)
sudo ufw allow 3000/tcp  # React dev server
sudo ufw allow 5000/tcp  # Flask dev server

# Deny all other incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### Docker Security
```bash
# Create docker user
sudo useradd -r -s /bin/false docker-user

# Set proper permissions
sudo chown -R docker-user:docker-user /opt/firebox
sudo chmod 750 /opt/firebox

# Secure Docker socket (production)
sudo chmod 660 /var/run/docker.sock
sudo chown root:docker /var/run/docker.sock
```

### SSL Certificate Setup
```bash
# Using Let's Encrypt (automatic)
# Traefik will handle certificate generation

# Using custom certificates
sudo mkdir -p /etc/ssl/firebox
sudo cp your-domain.crt /etc/ssl/firebox/
sudo cp your-domain.key /etc/ssl/firebox/
sudo chmod 600 /etc/ssl/firebox/your-domain.key
```

---

## 🧪 Validation & Testing

### Deployment Validation
```bash
# Check all services are running
docker-compose ps

# Test API endpoints
curl -f http://localhost:5000/api/health
curl -f http://localhost:5000/api/gateways/status

# Test frontend
curl -f http://localhost:3000

# Check logs
docker-compose logs backend
docker-compose logs frontend

# Monitor resource usage
docker stats
```

### Health Check Script
Create `scripts/health-check.sh`:
```bash
#!/bin/bash

echo "🔍 Firebox Health Check"
echo "======================"

# Check Docker services
echo "📦 Docker Services:"
docker-compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

# Check API health
echo -e "\n🔌 API Health:"
curl -s http://localhost:5000/api/health | jq '.data.status' || echo "❌ API Unavailable"

# Check frontend
echo -e "\n🌐 Frontend:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200" && echo "✅ Frontend OK" || echo "❌ Frontend Unavailable"

# Check disk space
echo -e "\n💾 Disk Space:"
df -h / | tail -1 | awk '{print $4 " available (" $5 " used)"}'

# Check memory
echo -e "\n🧠 Memory Usage:"
free -h | grep Mem | awk '{print $3 "/" $2 " (" $4 " available)"}'
```

---

## 📁 Backup & Recovery

### Database Backup
```bash
# Create backup script
cat > scripts/backup-db.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/database"
mkdir -p $BACKUP_DIR

docker-compose exec -T postgres pg_dump -U firebox firebox | gzip > $BACKUP_DIR/firebox_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
EOF

chmod +x scripts/backup-db.sh

# Setup cron job
echo "0 2 * * * /opt/firebox/scripts/backup-db.sh" | crontab -
```

### Configuration Backup
```bash
# Backup script for configurations
cat > scripts/backup-config.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/config"
mkdir -p $BACKUP_DIR

tar -czf $BACKUP_DIR/config_$DATE.tar.gz \
  .env.prod \
  docker-compose.prod.yml \
  traefik/ \
  monitoring/ \
  --exclude=*.log
EOF
```

---

## 🚨 Troubleshooting

### Common Issues

**Services won't start:**
```bash
# Check logs
docker-compose logs [service-name]

# Check ports
sudo netstat -tulpn | grep :3000
sudo netstat -tulpn | grep :5000

# Restart services
docker-compose restart
```

**Database connection errors:**
```bash
# Check PostgreSQL service
docker-compose exec postgres pg_isready -U firebox

# Check environment variables
docker-compose exec backend env | grep DB_

# Reset database
docker-compose down -v
docker-compose up -d postgres
```

**SSL certificate issues:**
```bash
# Check certificate expiry
openssl x509 -in /etc/ssl/firebox/your-domain.crt -text -noout | grep "Not After"

# Renew Let's Encrypt certificate
docker-compose exec traefik traefik --help
```

### Performance Issues
```bash
# Monitor resource usage
docker stats --no-stream

# Check disk space
df -h

# Check logs for errors
docker-compose logs --tail=100 backend | grep ERROR
```

### Logging & Debugging
```bash
# Increase log level for debugging
echo "LOG_LEVEL=DEBUG" >> .env

# Follow real-time logs
docker-compose logs -f backend

# Check specific service logs
journalctl -u docker -f
```

---

**Document Version**: 1.0.0  
**Last Updated**: October 17, 2025  
**Tested Environments**: Ubuntu 22.04, Docker 24.0+, Compose 2.20+