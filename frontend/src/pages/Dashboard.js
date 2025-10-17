import React from 'react';
import { 
  Box, 
  Heading, 
  Text,
  Grid,
  Button,
  Flash
} from '@primer/react';
import { SyncIcon, ServerIcon, PulseIcon } from '@primer/octicons-react';
import { useGateways } from '../hooks/useGateways';
import { useSystemHealth } from '../hooks/useSystem';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import StatusBadge from '../components/Common/StatusBadge';
import { formatDateTime, formatPercentage } from '../utils/formatters';

const Dashboard = () => {
  const { 
    data: gatewayData, 
    isLoading: gatewaysLoading, 
    error: gatewaysError,
    refetch: refetchGateways
  } = useGateways();

  const { 
    data: systemHealth, 
    isLoading: healthLoading, 
    error: healthError 
  } = useSystemHealth();

  const handleRefresh = () => {
    refetchGateways();
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
        
        <Button onClick={handleRefresh} disabled={gatewaysLoading}>
          <SyncIcon size={16} sx={{ mr: 1 }} />
          Refresh
        </Button>
      </Box>

      {/* Error Messages */}
      {gatewaysError && (
        <Flash variant="danger" sx={{ mb: 4 }}>
          Failed to load gateway data: {gatewaysError.message}
        </Flash>
      )}

      {healthError && (
        <Flash variant="danger" sx={{ mb: 4 }}>
          Failed to load system health: {healthError.message}
        </Flash>
      )}

      {/* Main Content Grid */}
      <Grid gridTemplateColumns={{ base: '1fr', lg: '2fr 1fr' }} gridGap={4}>
        {/* Left Column - Gateway Overview */}
        <Box>
          <Heading sx={{ fontSize: 3, mb: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
            <ServerIcon size={20} />
            Gateway Status
          </Heading>

          {gatewaysLoading ? (
            <LoadingSpinner message="Loading gateways..." />
          ) : gatewayData?.gateways ? (
            <Grid gridTemplateColumns="repeat(auto-fit, minmax(300px, 1fr))" gridGap={3}>
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
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
                    <Box>
                      <Heading sx={{ fontSize: 2, mb: 1 }}>{gateway.name}</Heading>
                      <Text sx={{ fontSize: 1, color: 'fg.muted' }}>Port {gateway.port}</Text>
                    </Box>
                    <StatusBadge status={gateway.status} type="gateway" />
                  </Box>

                  {gateway.trial && (
                    <Box sx={{ mt: 2 }}>
                      <Text sx={{ fontSize: 1, color: 'fg.muted', mb: 1 }}>Trial Status</Text>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Text sx={{ fontSize: 1 }}>{gateway.trial.remaining_display}</Text>
                        <StatusBadge 
                          status={gateway.trial.expired ? 'expired' : gateway.trial.emergency ? 'emergency' : 'active'} 
                          type="trial"
                          size="small"
                        />
                      </Box>
                    </Box>
                  )}
                </Box>
              ))}
            </Grid>
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
      </Grid>
    </Box>
  );
};

export default Dashboard;