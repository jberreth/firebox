import React, { useState } from 'react';
import { 
  Box, 
  Heading, 
  Text,
  Button,
  Flash,
  ButtonGroup
} from '@primer/react';
import { SyncIcon, ServerIcon, PulseIcon, ZapIcon } from '@primer/octicons-react';
import { useGateways } from '../hooks/useGateways';
import { useTrialStatus, useResetEmergencyTrials } from '../hooks/useTrials';
import { useSystemHealth } from '../hooks/useSystem';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import StatusBadge from '../components/Common/StatusBadge';
import { formatDateTime, formatPercentage } from '../utils/formatters';

const Dashboard = () => {
  const [notifications, setNotifications] = useState([]);
  
  const { 
    data: gatewayData, 
    isLoading: gatewaysLoading, 
    error: gatewaysError,
    refetch: refetchGateways
  } = useGateways();

  const { 
    data: trialStatus, 
    isLoading: trialsLoading, 
    error: trialsError,
    refetch: refetchTrials
  } = useTrialStatus();

  const { 
    data: systemHealth, 
    isLoading: healthLoading, 
    error: healthError 
  } = useSystemHealth();

  const emergencyResetMutation = useResetEmergencyTrials();

  const handleRefresh = () => {
    refetchGateways();
    refetchTrials();
  };

  const handleEmergencyReset = async () => {
    try {
      await emergencyResetMutation.mutateAsync();
      setNotifications(prev => [...prev, {
        id: Date.now(),
        type: 'success',
        message: 'Emergency trial reset completed'
      }]);
    } catch (error) {
      setNotifications(prev => [...prev, {
        id: Date.now(),
        type: 'error',
        message: `Emergency reset failed: ${error.message}`
      }]);
    }
  };

  const dismissNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  return (
    <Box>
      {/* Page Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Heading sx={{ fontSize: 5, mb: 1 }}>Dashboard</Heading>
          <Text sx={{ color: 'fg.muted', fontSize: 2 }}>
            Overview of your Ignition Sandbox environment
          </Text>
        </Box>
        
        <ButtonGroup>
          {trialStatus?.summary?.emergency > 0 && (
            <Button 
              variant="danger" 
              onClick={handleEmergencyReset}
              disabled={emergencyResetMutation.isLoading}
            >
              <ZapIcon size={16} sx={{ mr: 1 }} />
              Emergency Reset ({trialStatus.summary.emergency})
            </Button>
          )}
          <Button onClick={handleRefresh} disabled={gatewaysLoading || trialsLoading}>
            <SyncIcon size={16} sx={{ mr: 1 }} />
            Refresh
          </Button>
        </ButtonGroup>
      </Box>

      {/* Notifications */}
      {notifications.map(notification => (
        <Flash 
          key={notification.id}
          variant={notification.type === 'error' ? 'danger' : 'success'}
          sx={{ mb: 2 }}
          onDismiss={() => dismissNotification(notification.id)}
        >
          {notification.message}
        </Flash>
      ))}

      {/* Error Messages */}
      {gatewaysError && (
        <Flash variant="danger" sx={{ mb: 4 }}>
          Failed to load gateway data: {gatewaysError.type === 'network_error' ? gatewaysError.details : gatewaysError.message}
        </Flash>
      )}

      {trialsError && (
        <Flash variant="danger" sx={{ mb: 4 }}>
          Failed to load trial data: {trialsError.message}
        </Flash>
      )}

      {healthError && (
        <Flash variant="danger" sx={{ mb: 4 }}>
          Failed to load system health: {healthError.message}
        </Flash>
      )}

      {/* Main Content Grid */}
      <Box sx={{ display: 'grid', gridTemplateColumns: { base: '1fr', lg: '2fr 1fr' }, gap: 4 }}>
        {/* Left Column - Gateway Overview */}
        <Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Heading sx={{ fontSize: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
              <ServerIcon size={20} />
              Gateway Status
            </Heading>
            {gatewayData?.summary && (
              <Box sx={{ display: 'flex', gap: 2, fontSize: 0 }}>
                <Text sx={{ color: 'success.fg' }}>✓ {gatewayData.summary.healthy}</Text>
                <Text sx={{ color: 'danger.fg' }}>✗ {gatewayData.summary.unhealthy}</Text>
                <Text sx={{ color: 'attention.fg' }}>⟳ {gatewayData.summary.starting}</Text>
                {gatewayData.summary.emergency > 0 && (
                  <Text sx={{ color: 'severe.fg' }}>⚠ {gatewayData.summary.emergency} emergency</Text>
                )}
              </Box>
            )}
          </Box>

          {gatewaysLoading ? (
            <LoadingSpinner message="Loading gateways..." />
          ) : gatewayData?.gateways ? (
            <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 3 }}>
              {gatewayData.gateways.map((gateway) => (
                <Box
                  key={gateway.name}
                  sx={{
                    border: '1px solid',
                    borderColor: 'border.default',
                    borderRadius: 2,
                    p: 3,
                    bg: 'canvas.subtle'
                  }}
                >
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2, gap: 3 }}>
                    <Box sx={{ flex: 1, minWidth: 0 }}>
                      <Heading sx={{ fontSize: 2, mb: 1, pr: 2 }}>{gateway.displayName || gateway.name}</Heading>
                      <Text sx={{ fontSize: 1, color: 'fg.muted' }}>
                        Port {gateway.port} • {gateway.lastCheckFormatted}
                      </Text>
                    </Box>
                    <Box sx={{ flexShrink: 0 }}>
                      <StatusBadge status={gateway.status} variant={gateway.statusColor} />
                    </Box>
                  </Box>

                  {gateway.trial && (
                    <Box sx={{ mt: 2 }}>
                      <Text sx={{ fontSize: 1, color: 'fg.muted', mb: 1 }}>Trial Status</Text>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Text sx={{ fontSize: 1 }}>
                          {gateway.trialFormatted?.display || 'Unknown'}
                        </Text>
                        <StatusBadge 
                          status={gateway.trial.expired ? 'expired' : gateway.trial.emergency ? 'emergency' : 'active'} 
                          variant={gateway.trialColor}
                          size="small"
                        />
                      </Box>
                    </Box>
                  )}

                  {gateway.response_time && (
                    <Box sx={{ mt: 2 }}>
                      <Text sx={{ fontSize: 0, color: 'fg.muted' }}>
                        Response time: {gateway.response_time}ms
                      </Text>
                    </Box>
                  )}
                </Box>
              ))}
            </Box>
          ) : (
            <Text sx={{ color: 'fg.muted', textAlign: 'center', py: 4 }}>
              No gateway data available
            </Text>
          )}

          {gatewayData?.total && (
            <Text sx={{ mt: 3, color: 'fg.muted', fontSize: 1 }}>
              Total: {gatewayData.total} gateways
            </Text>
          )}
        </Box>

        {/* Right Column - System Health */}
        <Box>
          <Heading sx={{ fontSize: 3, mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
            <PulseIcon size={20} />
            System Health
          </Heading>

          {healthLoading ? (
            <LoadingSpinner message="Loading system health..." />
          ) : systemHealth ? (
            <Box
              sx={{
                border: '1px solid',
                borderColor: 'border.default',
                borderRadius: 2,
                p: 3,
                bg: 'canvas.subtle'
              }}
            >
              <Box sx={{ mb: 3 }}>
                <Text sx={{ fontSize: 1, color: 'fg.muted', mb: 1 }}>Last Updated</Text>
                <Text sx={{ fontSize: 1 }}>{formatDateTime(systemHealth.timestamp)}</Text>
              </Box>

              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                <Box>
                  <Text sx={{ fontSize: 1, color: 'fg.muted', mb: 1 }}>CPU Usage</Text>
                  <Text sx={{ fontSize: 2, fontWeight: 'bold' }}>
                    {formatPercentage(systemHealth.cpu_usage)}
                  </Text>
                </Box>

                <Box>
                  <Text sx={{ fontSize: 1, color: 'fg.muted', mb: 1 }}>Memory Usage</Text>
                  <Text sx={{ fontSize: 2, fontWeight: 'bold' }}>
                    {formatPercentage(systemHealth.memory_usage)}
                  </Text>
                </Box>

                <Box>
                  <Text sx={{ fontSize: 1, color: 'fg.muted', mb: 1 }}>Disk Usage</Text>
                  <Text sx={{ fontSize: 2, fontWeight: 'bold' }}>
                    {formatPercentage(systemHealth.disk_usage)}
                  </Text>
                </Box>

                <Box>
                  <Text sx={{ fontSize: 1, color: 'fg.muted', mb: 1 }}>Docker Status</Text>
                  <StatusBadge status={systemHealth.docker_status} type="system" size="small" />
                </Box>

                {systemHealth.container_count !== undefined && (
                  <Box>
                    <Text sx={{ fontSize: 1, color: 'fg.muted', mb: 1 }}>Containers</Text>
                    <Text sx={{ fontSize: 2, fontWeight: 'bold' }}>
                      {systemHealth.container_count}
                    </Text>
                  </Box>
                )}
              </Box>
            </Box>
          ) : (
            <Text sx={{ color: 'fg.muted', textAlign: 'center', py: 4 }}>
              No system health data available
            </Text>
          )}
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;