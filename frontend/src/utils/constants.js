// Application constants

// Gateway status types
export const GATEWAY_STATUS = {
  HEALTHY: 'healthy',
  UNHEALTHY: 'unhealthy',
  STARTING: 'starting',
  STOPPED: 'stopped',
  UNKNOWN: 'unknown',
};

// Gateway status color mapping for Primer UI
export const GATEWAY_STATUS_COLORS = {
  [GATEWAY_STATUS.HEALTHY]: 'success',
  [GATEWAY_STATUS.UNHEALTHY]: 'danger',
  [GATEWAY_STATUS.STARTING]: 'attention',
  [GATEWAY_STATUS.STOPPED]: 'secondary',
  [GATEWAY_STATUS.UNKNOWN]: 'secondary',
};

// Trial status constants
export const TRIAL_STATUS = {
  ACTIVE: 'active',
  EXPIRED: 'expired',
  EMERGENCY: 'emergency',
  UNKNOWN: 'unknown',
};

// Trial status color mapping
export const TRIAL_STATUS_COLORS = {
  [TRIAL_STATUS.ACTIVE]: 'success',
  [TRIAL_STATUS.EXPIRED]: 'danger',
  [TRIAL_STATUS.EMERGENCY]: 'attention',
  [TRIAL_STATUS.UNKNOWN]: 'secondary',
};

// System health thresholds
export const HEALTH_THRESHOLDS = {
  CPU: {
    WARNING: 70,
    CRITICAL: 90,
  },
  MEMORY: {
    WARNING: 80,
    CRITICAL: 95,
  },
  DISK: {
    WARNING: 80,
    CRITICAL: 95,
  },
};

// Refresh intervals (in milliseconds)
export const REFRESH_INTERVALS = {
  GATEWAY_STATUS: 30000, // 30 seconds
  SYSTEM_HEALTH: 15000,  // 15 seconds
  TRIAL_STATUS: 60000,   // 1 minute
  LOGS: 5000,           // 5 seconds
};

// Navigation routes
export const ROUTES = {
  DASHBOARD: '/',
  GATEWAYS: '/gateways',
  SYSTEM: '/system',
  SETTINGS: '/settings',
};

// Local storage keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'authToken',
  USER_PREFERENCES: 'userPreferences',
  SIDEBAR_COLLAPSED: 'sidebarCollapsed',
};

// Default pagination
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  PAGE_SIZE_OPTIONS: [10, 20, 50, 100],
};

// Error messages
export const ERROR_MESSAGES = {
  NETWORK_ERROR: 'Network error. Please check your connection.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  NOT_FOUND: 'The requested resource was not found.',
  GENERIC_ERROR: 'An unexpected error occurred. Please try again.',
  VALIDATION_ERROR: 'Please check your input and try again.',
};

// Success messages
export const SUCCESS_MESSAGES = {
  GATEWAY_RESTARTED: 'Gateway restarted successfully',
  TRIAL_RESET: 'Trial period reset successfully',
  SETTINGS_SAVED: 'Settings saved successfully',
};

// API configuration
export const API_CONFIG = {
  TIMEOUT: 10000, // 10 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
};

// Chart colors (GitHub-style)
export const CHART_COLORS = {
  PRIMARY: '#2f81f7',
  SUCCESS: '#3fb950',
  WARNING: '#d29922',
  DANGER: '#f85149',
  SECONDARY: '#656d76',
  ACCENT: '#a5a5a5',
};

// Breakpoints for responsive design
export const BREAKPOINTS = {
  SM: '544px',
  MD: '768px',
  LG: '1012px',
  XL: '1280px',
};

export default {
  GATEWAY_STATUS,
  GATEWAY_STATUS_COLORS,
  TRIAL_STATUS,
  TRIAL_STATUS_COLORS,
  HEALTH_THRESHOLDS,
  REFRESH_INTERVALS,
  ROUTES,
  STORAGE_KEYS,
  PAGINATION,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  API_CONFIG,
  CHART_COLORS,
  BREAKPOINTS,
};