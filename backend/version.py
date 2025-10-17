"""
Firebox Dashboard Version Information
"""

__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
__title__ = "Firebox Dashboard"
__description__ = "Modern web interface for Ignition Sandbox management"
__author__ = "Firebox Development Team"
__license__ = "MIT"
__copyright__ = "2025 Firebox Development Team"

# Release Information
RELEASE_DATE = "2025-10-17"
RELEASE_TYPE = "stable"
BUILD_NUMBER = "20251017.1"

# Component Versions
FLASK_VERSION = "2.3.3"
REACT_VERSION = "18.2.0"
PRIMER_VERSION = "36.0.0"
SELENIUM_VERSION = "4.15.2"
DOCKER_VERSION = "6.1.3"

# API Information
API_VERSION = "v1"
API_BASE_PATH = "/api"

# Feature Flags
FEATURES = {
    "gateway_monitoring": True,
    "trial_management": True,
    "selenium_automation": True,
    "docker_integration": True,
    "structured_logging": True,
    "prometheus_metrics": True,
    "authentication": False,  # Planned for v1.1
    "database_integration": False,  # Optional for v1.0
    "advanced_monitoring": False,  # Planned for v1.2
}

# System Requirements
REQUIREMENTS = {
    "python": ">=3.8",
    "node": ">=18.0",
    "docker": ">=20.10",
    "docker_compose": ">=2.0",
}

def get_version():
    """Return the current version string."""
    return __version__

def get_version_info():
    """Return version information as a dictionary."""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "title": __title__,
        "description": __description__,
        "release_date": RELEASE_DATE,
        "release_type": RELEASE_TYPE,
        "build_number": BUILD_NUMBER,
        "api_version": API_VERSION,
        "features": FEATURES,
        "requirements": REQUIREMENTS,
    }

def is_feature_enabled(feature_name):
    """Check if a feature is enabled."""
    return FEATURES.get(feature_name, False)