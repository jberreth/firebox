import { useQuery } from 'react-query';
import fireboxApi from '../services/endpoints';
import { REFRESH_INTERVALS } from '../utils/constants';

/**
 * Hook for fetching gateway status data
 */
export const useGateways = () => {
  return useQuery(
    'gateways',
    () => fireboxApi.gateways.getStatus(),
    {
      refetchInterval: REFRESH_INTERVALS.GATEWAY_STATUS,
      select: (response) => response.data,
      onError: (error) => {
        console.error('Failed to fetch gateways:', error);
      },
    }
  );
};

/**
 * Hook for fetching single gateway status
 */
export const useGateway = (gatewayName) => {
  return useQuery(
    ['gateway', gatewayName],
    () => fireboxApi.gateways.getSingleStatus(gatewayName),
    {
      enabled: !!gatewayName,
      refetchInterval: REFRESH_INTERVALS.GATEWAY_STATUS,
      select: (response) => response.data,
      onError: (error) => {
        console.error(`Failed to fetch gateway ${gatewayName}:`, error);
      },
    }
  );
};

/**
 * Hook for fetching gateway list
 */
export const useGatewayList = () => {
  return useQuery(
    'gateway-list',
    () => fireboxApi.gateways.list(),
    {
      select: (response) => response.data,
      staleTime: 5 * 60 * 1000, // 5 minutes
      onError: (error) => {
        console.error('Failed to fetch gateway list:', error);
      },
    }
  );
};

/**
 * Hook for fetching trial status
 */
export const useTrialStatus = (gatewayName) => {
  return useQuery(
    ['trial-status', gatewayName],
    () => fireboxApi.trial.getStatus(gatewayName),
    {
      enabled: !!gatewayName,
      refetchInterval: REFRESH_INTERVALS.TRIAL_STATUS,
      select: (response) => response.data,
      onError: (error) => {
        console.error(`Failed to fetch trial status for ${gatewayName}:`, error);
      },
    }
  );
};

/**
 * Hook for fetching trial automation status
 */
export const useTrialAutomation = () => {
  return useQuery(
    'trial-automation',
    () => fireboxApi.trial.getAutomationStatus(),
    {
      refetchInterval: REFRESH_INTERVALS.TRIAL_STATUS,
      select: (response) => response.data,
      onError: (error) => {
        console.error('Failed to fetch trial automation status:', error);
      },
    }
  );
};