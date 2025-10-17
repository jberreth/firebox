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
  // Reset trial for a gateway
  reset: (gatewayName, force = false) => 
    api.post('/trial/reset', { gateway_name: gatewayName, force }),
  
  // Get trial status for a gateway
  getStatus: (gatewayName) => api.get(`/trial/status/${gatewayName}`),
  
  // Bulk reset trials
  bulkReset: (gateways, force = false) => 
    api.post('/trial/bulk-reset', { gateways, force }),
  
  // Get automation status
  getAutomationStatus: () => api.get('/trial/automation/status'),
};

// Health check endpoint
export const healthApi = {
  check: () => api.get('/health'),
  metrics: () => api.get('/metrics'),
};

// Combined API object for easy importing
const fireboxApi = {
  gateways: gatewayApi,
  system: systemApi,
  trial: trialApi,
  health: healthApi,
};

export default fireboxApi;