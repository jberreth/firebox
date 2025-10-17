import { useQuery, useMutation, useQueryClient } from 'react-query';
import { trialApi } from '../services/endpoints';
import gatewayService from '../services/gatewayService';

/**
 * Hook for fetching trial status summary
 */
export const useTrialStatus = () => {
  return useQuery(
    'trial-status',
    () => gatewayService.getTrialStatus(),
    {
      refetchInterval: 60000, // 1 minute
      onError: (error) => {
        console.error('Failed to fetch trial status:', error);
      },
    }
  );
};

/**
 * Hook for resetting a single gateway trial
 */
export const useResetTrial = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    (gatewayName) => gatewayService.resetGatewayTrial(gatewayName),
    {
      onSuccess: (data, gatewayName) => {
        // Invalidate related queries
        queryClient.invalidateQueries('gateways');
        queryClient.invalidateQueries('trial-status');
        queryClient.invalidateQueries(['gateway', gatewayName]);
        console.log(`Trial reset completed for ${gatewayName}`);
      },
      onError: (error, gatewayName) => {
        console.error(`Failed to reset trial for ${gatewayName}:`, error);
      },
    }
  );
};

/**
 * Hook for resetting all gateway trials
 */
export const useResetAllTrials = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    () => gatewayService.resetAllTrials(),
    {
      onSuccess: (data) => {
        // Invalidate all gateway and trial data
        queryClient.invalidateQueries('gateways');
        queryClient.invalidateQueries('trial-status');
        console.log(`Bulk trial reset completed - ${data.successful_resets} successful, ${data.failed_resets} failed`);
      },
      onError: (error) => {
        console.error('Failed to reset all trials:', error);
      },
    }
  );
};

/**
 * Hook for resetting emergency trials only
 */
export const useResetEmergencyTrials = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    () => gatewayService.resetEmergencyTrials(),
    {
      onSuccess: (data) => {
        // Invalidate all gateway and trial data
        queryClient.invalidateQueries('gateways');
        queryClient.invalidateQueries('trial-status');
        console.log(`Emergency trial reset completed - ${data.successful_resets} successful, ${data.failed_resets} failed`);
      },
      onError: (error) => {
        console.error('Failed to reset emergency trials:', error);
      },
    }
  );
};

/**
 * Hook for fetching trial service configuration
 */
export const useTrialConfig = () => {
  return useQuery(
    'trial-config',
    () => gatewayService.getTrialConfig(),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      onError: (error) => {
        console.error('Failed to fetch trial config:', error);
      },
    }
  );
};

/**
 * Hook for checking trial reset requirements
 */
export const useTrialRequirements = () => {
  return useQuery(
    'trial-requirements',
    () => trialApi.checkRequirements(),
    {
      select: (response) => response.data,
      staleTime: 10 * 60 * 1000, // 10 minutes
      onError: (error) => {
        console.error('Failed to check trial requirements:', error);
      },
    }
  );
};