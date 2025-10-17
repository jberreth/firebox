import { useQuery } from 'react-query';
import fireboxApi from '../services/endpoints';
import { REFRESH_INTERVALS } from '../utils/constants';

/**
 * Hook for fetching system health data
 */
export const useSystemHealth = () => {
  return useQuery(
    'system-health',
    () => fireboxApi.system.getHealth(),
    {
      refetchInterval: REFRESH_INTERVALS.SYSTEM_HEALTH,
      select: (response) => response.data,
      onError: (error) => {
        console.error('Failed to fetch system health:', error);
      },
    }
  );
};

/**
 * Hook for fetching system information
 */
export const useSystemInfo = () => {
  return useQuery(
    'system-info',
    () => fireboxApi.system.getInfo(),
    {
      select: (response) => response.data,
      staleTime: 10 * 60 * 1000, // 10 minutes
      onError: (error) => {
        console.error('Failed to fetch system info:', error);
      },
    }
  );
};

/**
 * Hook for fetching system logs
 */
export const useSystemLogs = (options = {}) => {
  const { lines = 100, level = 'INFO', enabled = true } = options;
  
  return useQuery(
    ['system-logs', { lines, level }],
    () => fireboxApi.system.getLogs({ lines, level }),
    {
      enabled,
      refetchInterval: REFRESH_INTERVALS.LOGS,
      select: (response) => response.data,
      onError: (error) => {
        console.error('Failed to fetch system logs:', error);
      },
    }
  );
};

/**
 * Hook for application health check
 */
export const useHealthCheck = () => {
  return useQuery(
    'health-check',
    () => fireboxApi.health.check(),
    {
      refetchInterval: 30000, // 30 seconds
      select: (response) => response.data,
      onError: (error) => {
        console.error('Health check failed:', error);
      },
    }
  );
};