import { gatewayApi, trialApi } from './endpoints';

/**
 * Gateway Service - Business logic for gateway operations
 * Handles data transformation, caching, and complex operations
 */
class GatewayService {
  constructor() {
    this.statusCache = new Map();
    this.cacheTimeout = 30000; // 30 seconds
  }

  /**
   * Get all gateway statuses with caching
   */
  async getAllGateways() {
    try {
      const response = await gatewayApi.getStatus();
      return this.transformGatewayData(response.data);
    } catch (error) {
      console.error('Failed to fetch gateway status:', error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Get single gateway status
   */
  async getGateway(gatewayName) {
    try {
      const response = await gatewayApi.getSingleStatus(gatewayName);
      return this.transformSingleGateway(response.data);
    } catch (error) {
      console.error(`Failed to fetch gateway ${gatewayName}:`, error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Restart a gateway container
   */
  async restartGateway(gatewayName) {
    try {
      const response = await gatewayApi.restart(gatewayName);
      return {
        success: true,
        message: response.data.message,
        gateway: gatewayName,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error(`Failed to restart gateway ${gatewayName}:`, error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Get gateway logs
   */
  async getGatewayLogs(gatewayName, lines = 100) {
    try {
      const response = await gatewayApi.getLogs(gatewayName, lines);
      return {
        gateway: gatewayName,
        logs: response.data.logs,
        lines: response.data.lines_requested,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error(`Failed to fetch logs for ${gatewayName}:`, error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Reset trial for a single gateway
   */
  async resetGatewayTrial(gatewayName) {
    try {
      const response = await trialApi.resetSingle(gatewayName);
      return {
        ...response.data,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error(`Failed to reset trial for ${gatewayName}:`, error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Reset trials for all gateways
   */
  async resetAllTrials() {
    try {
      const response = await trialApi.resetAll();
      return {
        ...response.data,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Failed to reset all trials:', error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Reset trials for emergency gateways only
   */
  async resetEmergencyTrials() {
    try {
      const response = await trialApi.resetEmergency();
      return {
        ...response.data,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      console.error('Failed to reset emergency trials:', error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Get trial status summary
   */
  async getTrialStatus() {
    try {
      const response = await trialApi.getStatus();
      return this.transformTrialStatus(response.data);
    } catch (error) {
      console.error('Failed to fetch trial status:', error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Get trial service configuration
   */
  async getTrialConfig() {
    try {
      const response = await trialApi.getConfig();
      return response.data;
    } catch (error) {
      console.error('Failed to fetch trial config:', error);
      throw this.handleApiError(error);
    }
  }

  /**
   * Transform gateway data for UI consumption
   */
  transformGatewayData(data) {
    if (!data || !data.gateways) {
      return { gateways: [], total: 0, summary: this.getEmptySummary() };
    }

    const gateways = data.gateways.map(gateway => this.transformSingleGateway(gateway));
    const summary = this.calculateSummary(gateways);

    return {
      gateways,
      total: data.total || gateways.length,
      summary,
      timestamp: data.timestamp || new Date().toISOString()
    };
  }

  /**
   * Transform single gateway data
   */
  transformSingleGateway(gateway) {
    return {
      ...gateway,
      statusColor: this.getStatusColor(gateway.status),
      trialColor: this.getTrialColor(gateway.trial),
      displayName: gateway.name?.toUpperCase() || 'Unknown',
      lastCheckFormatted: this.formatLastCheck(gateway.last_check),
      trialFormatted: this.formatTrialInfo(gateway.trial),
      actions: this.getAvailableActions(gateway)
    };
  }

  /**
   * Transform trial status data
   */
  transformTrialStatus(data) {
    return {
      ...data,
      summary: {
        total: data.total_gateways || 0,
        healthy: data.healthy_trials || 0,
        emergency: data.emergency_trials || 0,
        expired: data.expired_trials || 0,
        unknown: data.unknown_trials || 0
      },
      gateways: (data.gateways || []).map(gateway => ({
        ...gateway,
        trialFormatted: this.formatTrialInfo(gateway.trial),
        trialColor: this.getTrialColor(gateway.trial)
      }))
    };
  }

  /**
   * Calculate summary statistics
   */
  calculateSummary(gateways) {
    return gateways.reduce((summary, gateway) => {
      // Status summary
      if (gateway.status === 'healthy') summary.healthy++;
      else if (gateway.status === 'unhealthy') summary.unhealthy++;
      else if (gateway.status === 'starting') summary.starting++;
      else summary.unknown++;

      // Trial summary
      if (gateway.trial?.expired) summary.expired++;
      else if (gateway.trial?.emergency) summary.emergency++;

      return summary;
    }, { healthy: 0, unhealthy: 0, starting: 0, unknown: 0, emergency: 0, expired: 0 });
  }

  /**
   * Get empty summary for error states
   */
  getEmptySummary() {
    return { healthy: 0, unhealthy: 0, starting: 0, unknown: 0, emergency: 0, expired: 0 };
  }

  /**
   * Get status color for UI
   */
  getStatusColor(status) {
    switch (status?.toLowerCase()) {
      case 'healthy': return 'success';
      case 'unhealthy': return 'danger';
      case 'starting': return 'attention';
      case 'unknown':
      default: return 'secondary';
    }
  }

  /**
   * Get trial color for UI
   */
  getTrialColor(trial) {
    if (!trial) return 'secondary';
    if (trial.expired) return 'danger';
    if (trial.emergency) return 'severe';
    return 'success';
  }

  /**
   * Format last check time
   */
  formatLastCheck(lastCheck) {
    if (!lastCheck) return 'Never';
    
    try {
      const date = new Date(lastCheck);
      const now = new Date();
      const diffMs = now - date;
      const diffSeconds = Math.floor(diffMs / 1000);
      const diffMinutes = Math.floor(diffSeconds / 60);

      if (diffSeconds < 60) return `${diffSeconds}s ago`;
      if (diffMinutes < 60) return `${diffMinutes}m ago`;
      return date.toLocaleTimeString();
    } catch (error) {
      return 'Invalid time';
    }
  }

  /**
   * Format trial information
   */
  formatTrialInfo(trial) {
    if (!trial) return { display: 'Unknown', state: 'unknown' };
    
    return {
      display: trial.remaining_display || 'Unknown',
      state: trial.trial_state || 'unknown',
      emergency: trial.emergency || false,
      expired: trial.expired || false,
      hours: trial.remaining_hours || 0
    };
  }

  /**
   * Get available actions for a gateway
   */
  getAvailableActions(gateway) {
    const actions = ['view', 'logs'];
    
    if (gateway.container_status === 'running') {
      actions.push('restart');
    }
    
    if (gateway.trial && !gateway.trial.expired) {
      actions.push('reset-trial');
    }
    
    return actions;
  }

  /**
   * Handle API errors consistently
   */
  handleApiError(error) {
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response;
      return {
        type: 'api_error',
        status,
        message: data?.error || data?.message || `HTTP ${status} Error`,
        details: data?.details || null
      };
    } else if (error.request) {
      // Network error
      return {
        type: 'network_error',
        message: 'Unable to connect to server',
        details: 'Please check your connection and try again'
      };
    } else {
      // Other error
      return {
        type: 'unknown_error',
        message: error.message || 'An unexpected error occurred',
        details: null
      };
    }
  }
}

// Export singleton instance
const gatewayServiceInstance = new GatewayService();
export default gatewayServiceInstance;