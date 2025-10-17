import { useQuery, useMutation, useQueryClient } from 'react-query';
import { gatewayApi } from '../services/endpoints';
import gatewayService from '../services/gatewayService';
import { REFRESH_INTERVALS } from '../utils/constants';

/**
 * Hook for fetching gateway status data
 */
export const useGateways = () => {
  return useQuery(
    'gateways',
    () => gatewayService.getAllGateways(),
    {
      refetchInterval: REFRESH_INTERVALS.GATEWAY_STATUS,
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
    () => gatewayService.getGateway(gatewayName),
    {
      enabled: !!gatewayName,
      refetchInterval: REFRESH_INTERVALS.GATEWAY_STATUS,
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
    () => gatewayApi.list(),
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
 * Hook for restarting a gateway
 */
export const useRestartGateway = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    (gatewayName) => gatewayService.restartGateway(gatewayName),
    {
      onSuccess: (data, gatewayName) => {
        // Invalidate and refetch gateway data
        queryClient.invalidateQueries('gateways');
        queryClient.invalidateQueries(['gateway', gatewayName]);
        console.log(`Gateway ${gatewayName} restart initiated`);
      },
      onError: (error, gatewayName) => {
        console.error(`Failed to restart gateway ${gatewayName}:`, error);
      },
    }
  );
};

/**
 * Hook for fetching gateway logs
 */
export const useGatewayLogs = (gatewayName, lines = 100) => {
  return useQuery(
    ['gateway-logs', gatewayName, lines],
    () => gatewayService.getGatewayLogs(gatewayName, lines),
    {
      enabled: !!gatewayName,
      staleTime: 30 * 1000, // 30 seconds
      onError: (error) => {
        console.error(`Failed to fetch logs for ${gatewayName}:`, error);
      },
    }
  );
};

