# 🔥 Firebox v1.0

A modern web interface for managing Ignition Sandbox environments with comprehensive gateway monitoring, trial period management, and automated reset capabilities.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Status](https://img.shields.io/badge/status-stable-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 🎯 **Core Functionality (v1.0)**
- ✅ **Real-time Gateway Monitoring**: Live health status tracking for Ignition containers
- ✅ **Trial Period Management**: Monitor trial periods with emergency reset capabilities  
- ✅ **Container Management**: Restart gateway containers with one click
- ✅ **Selenium Trial Reset**: Automated browser-based trial period resets
- ✅ **Modern Web Interface**: Primer React components with responsive design
- ✅ **Comprehensive APIs**: RESTful endpoints with structured error handling
- ✅ **Docker Integration**: Full Docker container inspection and management
- ✅ **Structured Logging**: JSON-formatted logs with request tracing

### 📊 **Dashboard Features**
- Gateway status cards with real-time health indicators
- Trial period monitoring with emergency alerts
- Container restart functionality
- Bulk trial reset operations
- Responsive design for all device sizes

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local development)
- Python 3.8+ (for local development)

### Production Deployment
```bash
# Clone repository
git clone <repository-url>
cd firebox

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start all services
docker-compose up -d

# Access dashboard
open http://localhost:3000
```

### Development Setup
```bash
# Backend (Terminal 1)
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python test_server.py

# Frontend (Terminal 2) 
cd frontend
npm install
npm start

# Access development servers
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

## 🏗️ Architecture

### Backend Stack
- **Framework**: Flask 2.3 with application factory pattern
- **Database**: PostgreSQL with SQLAlchemy ORM (configured, optional for v1.0)
- **Container Management**: Docker SDK for Python with real-time inspection
- **Trial Reset**: Selenium WebDriver with Chrome for automation
- **Monitoring**: Prometheus client with custom metrics
- **Logging**: Structlog with JSON output and request tracing

### Frontend Stack  
- **Framework**: React 18 with modern hooks and functional components
- **UI Library**: GitHub Primer React for consistent modern interface
- **State Management**: React Query for server state and caching
- **Routing**: React Router v6 with nested routes
- **HTTP Client**: Axios with interceptors and error handling
- **Styling**: Primer CSS system with responsive utilities

### Infrastructure
- **Reverse Proxy**: Traefik v2 with automatic service discovery
- **Monitoring**: Prometheus + Grafana + cAdvisor stack
- **Container Orchestration**: Docker Compose with development profiles
- **Development**: Hot reload enabled for both backend and frontend

## 📡 API Endpoints

### Gateway Management
```http
GET    /api/health              # System health check
GET    /api/gateways/status     # All gateway statuses
GET    /api/gateways/list       # Gateway list
GET    /api/gateways/{name}/status          # Single gateway status  
POST   /api/gateways/{name}/restart         # Restart container
GET    /api/gateways/{name}/logs?lines=100  # Container logs
```

### Trial Management  
```http
GET    /api/trial/status                # Trial status summary
POST   /api/trial/reset/{name}          # Reset single gateway trial
POST   /api/trial/reset/all             # Reset all trials
POST   /api/trial/reset/emergency       # Reset emergency trials only
GET    /api/trial/config                # Trial service configuration
```

## 🔧 Configuration

### Environment Variables
```bash
# Core Configuration
HOST_IP=localhost                    # Host IP for container access
COMPOSE_PROJECT_NAME=firebox        # Docker Compose project name

# Service Ports  
FRONTEND_PORT=3000                  # React development server
BACKEND_PORT=5000                   # Flask API server
GRAFANA_PORT=3001                   # Grafana dashboard
PROMETHEUS_PORT=9090                # Prometheus metrics

# Database (Optional)
DB_HOST=postgres
DB_NAME=firebox
DB_USER=firebox  
DB_PASSWORD=secure_password_here

# Selenium Configuration
SELENIUM_HEADLESS=true              # Run browser in headless mode
RESET_TIMEOUT=30                    # Trial reset timeout (seconds)
IGNITION_USERNAME=admin             # Default Ignition username
IGNITION_PASSWORD=password          # Default Ignition password

# Logging
LOG_LEVEL=INFO                      # Logging level
LOG_FORMAT=json                     # Log format (json/text)
LOG_DIR=/opt/firebox/backend/logs   # Log directory
```

## 🧪 Development

### Project Structure
```
firebox/
├── backend/                 # Flask API server
│   ├── app.py              # Application factory
│   ├── test_server.py      # Development server with mock data
│   ├── services/           # Business logic layer
│   │   ├── docker_service.py      # Docker container management
│   │   ├── gateway_service.py     # Gateway business logic
│   │   └── trial_reset_service.py # Selenium trial automation
│   ├── routes/             # API endpoint definitions
│   │   ├── health.py       # Health check endpoints
│   │   ├── gateways.py     # Gateway management APIs
│   │   └── trial.py        # Trial reset APIs
│   └── utils/              # Utility functions
├── frontend/               # React dashboard
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API integration layer
│   │   └── utils/          # Frontend utilities
│   └── public/             # Static assets
├── docker-compose.yml      # Development orchestration
└── docs/                   # Documentation
```

### Development Commands
```bash
# Backend development
cd backend && source venv/bin/activate
python test_server.py              # Start with mock data
python app.py                      # Start full server (requires DB)

# Frontend development  
cd frontend
npm start                          # Start development server
npm run build                      # Production build
npm test                           # Run tests

# Docker development
docker-compose up                  # Start all services
docker-compose up -d               # Start in background
docker-compose logs -f backend     # Follow backend logs
docker-compose down                # Stop all services
```

## 📋 Version 1.0 Status

### ✅ Completed Features
- [x] **Full-Stack Architecture**: Flask backend + React frontend with modern tooling
- [x] **Gateway Status Monitoring**: Real-time Docker container inspection and health checks
- [x] **Trial Period Management**: Comprehensive trial monitoring with emergency reset capabilities
- [x] **Selenium Automation**: Complete browser automation for trial resets with error handling
- [x] **Modern UI Framework**: GitHub Primer React components with responsive design
- [x] **API Integration**: Complete REST API with React Query integration and caching
- [x] **Development Environment**: Hot reload, structured logging, and development tooling
- [x] **Container Management**: Docker service integration for container lifecycle management

### 🔄 In Progress
- [ ] **Production Docker Configuration**: Production-ready containers and orchestration
- [ ] **Gateway Integration Testing**: Real Ignition container testing and validation
- [ ] **Traefik Configuration**: SSL termination and production routing setup

### 📅 Roadmap (Future Versions)
- [ ] **Authentication System**: JWT-based user authentication and authorization
- [ ] **Database Integration**: PostgreSQL integration for persistent data storage  
- [ ] **Advanced Monitoring**: Prometheus metrics and Grafana dashboard integration
- [ ] **Backup Management**: Automated gateway backup and restore functionality
- [ ] **Multi-Environment Support**: Development, staging, and production environment profiles

## 🐛 Known Issues

### v1.0 Limitations
- **Mock Data**: Current test server uses mock data for development
- **Authentication**: No user authentication system implemented yet
- **Database**: PostgreSQL configured but not required for basic functionality
- **SSL**: HTTPS not configured for production deployment

### Workarounds
- Use `test_server.py` for frontend development without full backend dependencies
- Manual configuration required for production SSL certificates
- Gateway integration requires existing Ignition containers to be configured

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Follow the development setup instructions above
4. Make changes and test thoroughly
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Code Standards
- **Backend**: Follow PEP 8, use type hints, include docstrings
- **Frontend**: Use ESLint configuration, follow React hooks patterns
- **Testing**: Write unit tests for new functionality
- **Documentation**: Update README and docs for new features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **GitHub Primer**: UI component library and design system
- **Ignition by Inductive Automation**: Industrial automation platform
- **Docker Community**: Containerization platform and ecosystem
- **React & Flask Communities**: Framework development and support

---

**Version**: 1.0.0  
**Last Updated**: October 17, 2025  
**Status**: Stable Development Build