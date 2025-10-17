import axios from 'axios';

// Get API base URL from environment or use default
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000, // 10 seconds
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens (if needed)
api.interceptors.request.use(
  (config) => {
    // Add timestamp to requests for debugging
    config.metadata = { startTime: new Date() };
    
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors and logging
api.interceptors.response.use(
  (response) => {
    const duration = new Date() - response.config.metadata.startTime;
    console.log(
      `[API] ${response.config.method?.toUpperCase()} ${response.config.url} - ${response.status} (${duration}ms)`
    );
    return response;
  },
  (error) => {
    const duration = error.config?.metadata ? new Date() - error.config.metadata.startTime : 0;
    console.error(
      `[API] ${error.config?.method?.toUpperCase()} ${error.config?.url} - ${error.response?.status || 'ERROR'} (${duration}ms)`,
      error.response?.data || error.message
    );
    
    // Handle specific error cases
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login or clear auth
      localStorage.removeItem('authToken');
      // Could trigger a redirect to login page here
    }
    
    return Promise.reject(error);
  }
);

export default api;