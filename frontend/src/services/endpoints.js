import api from './api';

// Gateway API endpoints
export const gatewayApi = {
  // Get all gateway statuses
  getStatus: () => api.get('/gateways/status'),
  
  // Get single gateway status
  getSingleStatus: (gatewayName) => api.get(`/gateways/${gatewayName}/status`),
  
  // Restart a gateway
  restart: (gatewayName) => api.post(`/gateways/${gatewayName}/restart`),
  
  // List all available gateways
  list: () => api.get('/gateways/list'),
  
  // Get gateway logs
  getLogs: (gatewayName, lines = 100) => api.get(`/gateways/${gatewayName}/logs?lines=${lines}`),
};

// System API endpoints
export const systemApi = {
  // Get system health
  getHealth: () => api.get('/system/health'),
  
  // Get system information
  getInfo: () => api.get('/system/info'),
  
  // Get system logs
  getLogs: (params = {}) => api.get('/system/logs', { params }),
};

// Trial API endpoints
export const trialApi = {
  // Reset trial for a specific gateway
  resetSingle: (gatewayName) => api.post(`/trial/reset/${gatewayName}`),
  
  // Reset trials for all gateways
  resetAll: () => api.post('/trial/reset/all'),
  
  // Reset trials for emergency gateways only
  resetEmergency: () => api.post('/trial/reset/emergency'),
  
  // Legacy reset endpoint (supports both single and bulk)
  reset: (gatewayName = 'all', force = false) => 
    api.post('/trial/reset', { gateway_name: gatewayName, force }),
  
  // Get trial status summary for all gateways
  getStatus: () => api.get('/trial/status'),
  
  // Get trial service configuration
  getConfig: () => api.get('/trial/config'),
  
  // Check trial reset requirements
  checkRequirements: () => api.get('/trial/check'),
};

// Health check endpoint
export const healthApi = {
  check: () => api.get('/health'),
  detailed: () => api.get('/health/detailed'),
};

// Combined API object for easy importing
const fireboxApi = {
  gateways: gatewayApi,
  system: systemApi,
  trial: trialApi,
  health: healthApi,
};

export default fireboxApi;