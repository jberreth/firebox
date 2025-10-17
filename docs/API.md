# 📡 Firebox API Documentation v1.0

Complete API reference for the Firebox backend services.

## Base Configuration

**Base URL**: `http://localhost:5000` (development) | `https://your-domain.com` (production)  
**API Version**: v1.0  
**Content-Type**: `application/json`  
**Authentication**: None (v1.0) | JWT Bearer Token (planned v1.1)

## Response Format

All API responses follow a consistent JSON structure:

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation completed successfully",
  "timestamp": "2025-10-17T10:30:00Z"
}
```

### Error Response  
```json
{
  "success": false,
  "error": {
    "code": "GATEWAY_NOT_FOUND",
    "message": "Gateway 'VIGDEV' not found",
    "details": { /* additional error context */ }
  },
  "timestamp": "2025-10-17T10:30:00Z"
}
```

## Health Endpoints

### GET /api/health

System health check with dependency validation.

**Response**:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "1.0.0",
    "uptime": 3600,
    "services": {
      "docker": "connected",
      "selenium": "available", 
      "database": "optional"
    },
    "environment": "development"
  }
}
```

**Status Codes**:
- `200 OK`: System healthy
- `503 Service Unavailable`: System unhealthy

---

## Gateway Management APIs

### GET /api/gateways/status

Get comprehensive status for all gateways.

**Response**:
```json
{
  "success": true,
  "data": {
    "gateways": [
      {
        "name": "VIGDEV",
        "status": "running",
        "container_id": "abc123def456",
        "health": "healthy",
        "uptime": "2 days, 14 hours",
        "trial_status": "active",
        "trial_days_remaining": 45,
        "ports": {
          "http": 8088,
          "https": 8043
        },
        "version": "8.1.35",
        "last_restart": "2025-10-15T08:30:00Z"
      }
    ],
    "summary": {
      "total": 6,
      "running": 5,
      "stopped": 1,
      "emergency_trials": 2
    }
  }
}
```

**Status Codes**:
- `200 OK`: Status retrieved successfully
- `503 Service Unavailable`: Docker service unavailable

---

### GET /api/gateways/list

Get gateway inventory with configuration details.

**Response**:
```json
{
  "success": true,
  "data": {
    "gateways": [
      {
        "name": "VIGDEV",
        "display_name": "VIG Development",
        "description": "Development gateway for testing",
        "container_name": "ignition-sandbox_vigdev_1", 
        "image": "inductiveautomation/ignition:8.1.35",
        "created": "2025-10-10T12:00:00Z",
        "ports": {
          "http": 8088,
          "https": 8043
        },
        "volumes": [
          "/opt/ignition-sandbox/gateways/VIGDEV/VIGDEV-data:/usr/local/bin/ignition/data"
        ],
        "environment": {
          "IGNITION_EDITION": "standard", 
          "GATEWAY_ADMIN_PASSWORD": "password"
        }
      }
    ]
  }
}
```

---

### GET /api/gateways/{name}/status

Get detailed status for a specific gateway.

**Parameters**:
- `name` (path): Gateway name (e.g., "VIGDEV")

**Response**:
```json
{
  "success": true,
  "data": {
    "name": "VIGDEV",
    "status": "running",
    "container": {
      "id": "abc123def456",
      "name": "ignition-sandbox_vigdev_1",
      "image": "inductiveautomation/ignition:8.1.35",
      "state": "running",
      "health": "healthy",
      "started_at": "2025-10-15T08:30:00Z",
      "uptime_seconds": 176400
    },
    "gateway_info": {
      "version": "8.1.35",
      "edition": "standard",
      "platform": "linux/amd64",
      "java_version": "11.0.20"
    },
    "trial_info": {
      "status": "active",
      "days_remaining": 45,
      "expiry_date": "2025-12-01T00:00:00Z",
      "is_emergency": false,
      "last_reset": "2025-09-16T10:15:00Z"
    },
    "network": {
      "http_port": 8088,
      "https_port": 8043,
      "internal_ip": "172.20.0.5",
      "external_url": "http://localhost:8088"
    },
    "resources": {
      "cpu_usage": 12.5,
      "memory_usage": 512.3,
      "memory_limit": 2048.0,
      "disk_usage": 1024.8
    }
  }
}
```

**Status Codes**:
- `200 OK`: Gateway status retrieved
- `404 Not Found`: Gateway does not exist
- `503 Service Unavailable`: Container service unavailable

---

### POST /api/gateways/{name}/restart

Restart a gateway container.

**Parameters**:
- `name` (path): Gateway name (e.g., "VIGDEV")

**Request Body** (optional):
```json
{
  "timeout": 30,
  "force": false,
  "wait_for_healthy": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "name": "VIGDEV",
    "operation": "restart",
    "status": "completed",
    "container_id": "abc123def456",
    "started_at": "2025-10-17T10:30:00Z",
    "duration_seconds": 25.3,
    "health_check": {
      "status": "healthy",
      "response_time": 1200,
      "url": "http://localhost:8088/system/gwinfo"
    }
  }
}
```

**Status Codes**:
- `200 OK`: Restart completed successfully
- `202 Accepted`: Restart initiated (async operation)
- `404 Not Found`: Gateway does not exist
- `409 Conflict`: Gateway already restarting
- `503 Service Unavailable`: Container service unavailable

---

### GET /api/gateways/{name}/logs

Get container logs for a gateway.

**Parameters**:
- `name` (path): Gateway name
- `lines` (query): Number of log lines to retrieve (default: 100, max: 1000)
- `since` (query): Timestamp to get logs since (ISO 8601 format)
- `follow` (query): Stream logs in real-time (boolean, default: false)

**Example**: `/api/gateways/VIGDEV/logs?lines=200&since=2025-10-17T10:00:00Z`

**Response**:
```json
{
  "success": true,
  "data": {
    "name": "VIGDEV",
    "container_id": "abc123def456",
    "logs": [
      {
        "timestamp": "2025-10-17T10:29:45Z",
        "level": "INFO",
        "message": "Gateway startup completed successfully",
        "source": "ignition.gateway"
      },
      {
        "timestamp": "2025-10-17T10:29:30Z", 
        "level": "INFO",
        "message": "Loading module: Perspective",
        "source": "ignition.modules"
      }
    ],
    "metadata": {
      "total_lines": 1247,
      "returned_lines": 200,
      "truncated": true,
      "log_level_filter": null
    }
  }
}
```

---

## Trial Management APIs

### GET /api/trial/status

Get trial status summary for all gateways.

**Response**:
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_gateways": 6,
      "active_trials": 4,
      "expired_trials": 1,
      "emergency_trials": 2,
      "grace_period": 1
    },
    "gateways": [
      {
        "name": "VIGDEV",
        "trial_status": "active",
        "days_remaining": 45,
        "expiry_date": "2025-12-01T00:00:00Z",
        "is_emergency": false,
        "last_reset": "2025-09-16T10:15:00Z"
      },
      {
        "name": "VIGVIS",
        "trial_status": "emergency",
        "days_remaining": 2,
        "expiry_date": "2025-10-19T00:00:00Z",
        "is_emergency": true,
        "last_reset": "2025-08-20T14:30:00Z"
      }
    ],
    "configuration": {
      "emergency_threshold": 7,
      "auto_reset_enabled": true,
      "reset_schedule": "0 2 * * 0",
      "notification_enabled": true
    }
  }
}
```

---

### POST /api/trial/reset/{name}

Reset trial period for a specific gateway using Selenium automation.

**Parameters**:
- `name` (path): Gateway name (e.g., "VIGDEV")

**Request Body** (optional):
```json
{
  "force": false,
  "timeout": 60,
  "headless": true,
  "wait_for_completion": true
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "name": "VIGDEV",
    "operation": "trial_reset",
    "status": "completed",
    "result": {
      "previous_days": 2,
      "new_days": 120,
      "expiry_date": "2026-02-14T00:00:00Z",
      "reset_timestamp": "2025-10-17T10:30:00Z"
    },
    "automation": {
      "browser": "chrome",
      "headless": true,
      "duration_seconds": 45.2,
      "steps_completed": 8,
      "screenshots": [
        "/logs/trial_reset_VIGDEV_20251017_103000_step1.png"
      ]
    }
  }
}
```

**Status Codes**:
- `200 OK`: Trial reset completed successfully
- `202 Accepted`: Trial reset initiated (async operation)
- `400 Bad Request`: Invalid parameters or gateway not eligible
- `404 Not Found`: Gateway does not exist
- `409 Conflict`: Reset already in progress
- `422 Unprocessable Entity`: Gateway not accessible or trial already active
- `503 Service Unavailable`: Selenium service unavailable

---

### POST /api/trial/reset/all

Reset trial periods for all gateways that meet criteria.

**Request Body** (optional):
```json
{
  "filter": {
    "emergency_only": false,
    "max_days_remaining": 30,
    "include_active": true,
    "exclude_gateways": ["VIGPROD"]
  },
  "options": {
    "timeout": 60,
    "headless": true,
    "parallel": true,
    "max_concurrent": 3
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "operation": "bulk_trial_reset",
    "status": "completed",
    "summary": {
      "total_requested": 5,
      "completed": 4,
      "failed": 1,
      "skipped": 0,
      "duration_seconds": 125.7
    },
    "results": [
      {
        "name": "VIGDEV",
        "status": "completed",
        "previous_days": 15,
        "new_days": 120,
        "duration_seconds": 32.1
      },
      {
        "name": "VIGVIS", 
        "status": "failed",
        "error": "Gateway not accessible",
        "duration_seconds": 45.0
      }
    ]
  }
}
```

---

### POST /api/trial/reset/emergency

Reset trial periods only for gateways in emergency status (≤7 days remaining).

**Request Body** (optional):
```json
{
  "options": {
    "timeout": 60,
    "headless": true,
    "notify": true
  }
}
```

**Response**:
```json
{
  "success": true,
  "data": {
    "operation": "emergency_trial_reset",
    "status": "completed",
    "emergency_gateways": [
      {
        "name": "VIGVIS",
        "status": "completed", 
        "previous_days": 2,
        "new_days": 120,
        "was_emergency": true
      }
    ],
    "summary": {
      "emergency_count": 2,
      "reset_completed": 2,
      "reset_failed": 0,
      "total_duration": 89.4
    }
  }
}
```

---

### GET /api/trial/config

Get trial management service configuration.

**Response**:
```json
{
  "success": true,
  "data": {
    "selenium": {
      "browser": "chrome",
      "headless": true,
      "timeout": 60,
      "implicit_wait": 10,
      "page_load_timeout": 30,
      "screenshot_enabled": true
    },
    "thresholds": {
      "emergency_days": 7,
      "warning_days": 14,
      "notification_days": 21
    },
    "automation": {
      "auto_reset_enabled": true,
      "schedule": "0 2 * * 0",
      "max_concurrent": 3,
      "retry_attempts": 2,
      "retry_delay": 30
    },
    "security": {
      "default_username": "admin",
      "password_configured": true,
      "ssl_verify": false,
      "user_agent": "Firebox-TrialReset/1.0"
    }
  }
}
```

---

## Error Codes Reference

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `GATEWAY_NOT_FOUND` | Gateway does not exist | 404 |
| `CONTAINER_NOT_RUNNING` | Gateway container is not running | 409 |
| `DOCKER_SERVICE_UNAVAILABLE` | Cannot connect to Docker | 503 |
| `SELENIUM_SERVICE_ERROR` | Selenium automation failed | 503 |
| `TRIAL_RESET_IN_PROGRESS` | Reset operation already running | 409 |
| `GATEWAY_NOT_ACCESSIBLE` | Cannot access gateway web interface | 422 |
| `INVALID_PARAMETERS` | Request parameters validation failed | 400 |
| `OPERATION_TIMEOUT` | Operation exceeded timeout limit | 408 |
| `INTERNAL_SERVER_ERROR` | Unexpected server error | 500 |

## Rate Limiting

**Development**: No rate limiting  
**Production**: 100 requests/minute per IP (planned)

## Webhooks (Planned v1.1)

Future support for webhook notifications:
- Gateway status changes
- Trial expiry warnings  
- Reset operation completions
- System alerts and errors

## Authentication (Planned v1.1)

Future JWT-based authentication:
```bash
# Login
POST /api/auth/login
Authorization: Basic base64(username:password)

# Protected requests
Authorization: Bearer <jwt_token>
```

---

**API Version**: 1.0.0  
**Last Updated**: October 17, 2025  
**OpenAPI Spec**: Available at `/api/docs` (planned)