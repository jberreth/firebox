# Firebox Project Structure

```
firebox/
├── README.md                   # Project overview and quick start
├── .env.example               # Environment configuration template
├── .env                       # Local environment (not tracked)
├── docker-compose.yml         # Main orchestration
├── docker-compose.override.yml # Local development overrides
├── .gitignore                 # Git ignore rules
│
├── backend/                   # Flask API backend
│   ├── app.py                # Main Flask application
│   ├── config.py             # Configuration management
│   ├── requirements.txt      # Python dependencies
│   ├── Dockerfile           # Backend container
│   ├── routes/              # API route modules
│   │   ├── __init__.py
│   │   ├── gateways.py      # Gateway management endpoints
│   │   ├── system.py        # System health endpoints
│   │   └── trial.py         # Trial management endpoints
│   ├── services/            # Business logic services
│   │   ├── __init__.py
│   │   ├── docker_service.py # Docker API integration
│   │   ├── gateway_service.py # Gateway status logic
│   │   └── trial_service.py  # Trial management logic
│   ├── utils/               # Utility modules
│   │   ├── __init__.py
│   │   ├── logging.py       # Structured logging setup
│   │   └── validators.py    # Input validation
│   └── tests/               # Backend tests
│       ├── __init__.py
│       ├── test_routes.py
│       └── test_services.py
│
├── frontend/                # React frontend
│   ├── package.json        # Node.js dependencies
│   ├── package-lock.json   # Lock file
│   ├── Dockerfile         # Frontend container
│   ├── nginx.conf         # Nginx configuration
│   ├── public/            # Static assets
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/               # React source code
│   │   ├── index.js       # Entry point
│   │   ├── App.js         # Main application
│   │   ├── components/    # Reusable components
│   │   │   ├── Layout/
│   │   │   │   ├── Sidebar.js
│   │   │   │   ├── Header.js
│   │   │   │   └── Footer.js
│   │   │   ├── Gateway/
│   │   │   │   ├── GatewayCard.js
│   │   │   │   ├── GatewayStatus.js
│   │   │   │   └── TrialInfo.js
│   │   │   └── Common/
│   │   │       ├── LoadingSpinner.js
│   │   │       ├── ErrorBoundary.js
│   │   │       └── StatusBadge.js
│   │   ├── pages/         # Page components
│   │   │   ├── Dashboard.js
│   │   │   ├── Gateways.js
│   │   │   ├── System.js
│   │   │   └── Settings.js
│   │   ├── hooks/         # Custom React hooks
│   │   │   ├── useGateways.js
│   │   │   └── useSystem.js
│   │   ├── services/      # API services
│   │   │   ├── api.js
│   │   │   └── endpoints.js
│   │   ├── utils/         # Utility functions
│   │   │   ├── formatters.js
│   │   │   └── constants.js
│   │   └── styles/        # CSS/SCSS files
│   │       ├── global.css
│   │       └── components/
│   └── tests/             # Frontend tests
│       ├── components/
│       └── pages/
│
├── scripts/              # Automation scripts
│   ├── trial_reset.py   # Selenium trial reset
│   ├── health_check.py  # System health monitoring
│   ├── backup_manager.py # Gateway backup management
│   └── setup.sh         # Initial setup script
│
├── config/              # Configuration files
│   ├── traefik/        # Traefik configuration
│   │   ├── traefik.yml
│   │   └── dynamic/
│   ├── grafana/        # Grafana dashboards and config
│   │   ├── dashboards/
│   │   └── provisioning/
│   ├── prometheus/     # Prometheus configuration
│   │   └── prometheus.yml
│   └── nginx/          # Nginx configurations
│       └── default.conf
│
└── docs/               # Documentation
    ├── API.md         # API documentation
    ├── DEPLOYMENT.md  # Deployment guide
    ├── DEVELOPMENT.md # Development setup
    └── ARCHITECTURE.md # System architecture
```

## Key Design Principles

1. **Separation of Concerns**: Clear boundaries between frontend, backend, and infrastructure
2. **Configuration Management**: Environment-based configuration with sensible defaults
3. **Comprehensive Logging**: Structured logging throughout all components
4. **Error Handling**: Robust error handling with graceful degradation
5. **Testing**: Test coverage for critical paths and business logic
6. **Documentation**: Clear, maintainable documentation at all levels
7. **Security**: Security-first approach with minimal exposed surfaces