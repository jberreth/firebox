import React, { useState } from 'react';
import { 
  Box, 
  Heading, 
  Text,
  Button,
  ButtonGroup,
  Flash,
  ActionMenu,
  ActionList,
  Dialog
} from '@primer/react';
import { 
  SyncIcon, 
  ServerIcon, 
  KebabHorizontalIcon, 
  PlayIcon, 
  ZapIcon,
  LogIcon 
} from '@primer/octicons-react';
import { useGateways, useRestartGateway } from '../hooks/useGateways';
import { useResetTrial, useResetAllTrials, useResetEmergencyTrials } from '../hooks/useTrials';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import StatusBadge from '../components/Common/StatusBadge';

const Gateways = () => {
  const [selectedGateway, setSelectedGateway] = useState(null);
  const [showLogsDialog, setShowLogsDialog] = useState(false);
  const [notifications, setNotifications] = useState([]);

  const { 
    data: gatewayData, 
    isLoading: gatewaysLoading, 
    error: gatewaysError,
    refetch: refetchGateways
  } = useGateways();

  const restartMutation = useRestartGateway();
  const resetTrialMutation = useResetTrial();
  const resetAllMutation = useResetAllTrials();
  const resetEmergencyMutation = useResetEmergencyTrials();

  const handleRefresh = () => {
    refetchGateways();
  };

  const handleRestartGateway = async (gatewayName) => {
    try {
      await restartMutation.mutateAsync(gatewayName);
      addNotification('success', `Gateway ${gatewayName} restart initiated`);
    } catch (error) {
      addNotification('error', `Failed to restart ${gatewayName}: ${error.message}`);
    }
  };

  const handleResetTrial = async (gatewayName) => {
    try {
      await resetTrialMutation.mutateAsync(gatewayName);
      addNotification('success', `Trial reset initiated for ${gatewayName}`);
    } catch (error) {
      addNotification('error', `Failed to reset trial for ${gatewayName}: ${error.message}`);
    }
  };

  const handleResetAllTrials = async () => {
    try {
      const result = await resetAllMutation.mutateAsync();
      addNotification('success', `Bulk reset completed: ${result.successful_resets} successful, ${result.failed_resets} failed`);
    } catch (error) {
      addNotification('error', `Failed to reset all trials: ${error.message}`);
    }
  };

  const handleResetEmergencyTrials = async () => {
    try {
      const result = await resetEmergencyMutation.mutateAsync();
      addNotification('success', `Emergency reset completed: ${result.successful_resets} successful, ${result.failed_resets} failed`);
    } catch (error) {
      addNotification('error', `Failed to reset emergency trials: ${error.message}`);
    }
  };

  const addNotification = (type, message) => {
    const notification = {
      id: Date.now(),
      type,
      message
    };
    setNotifications(prev => [...prev, notification]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== notification.id));
    }, 5000);
  };

  const dismissNotification = (id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  // Prepare data for table
  const tableData = gatewayData?.gateways?.map(gateway => ({
    id: gateway.name,
    gateway: gateway,
    name: gateway.displayName || gateway.name,
    status: gateway.status,
    port: gateway.port,
    trial: gateway.trialFormatted,
    responseTime: gateway.response_time,
    actions: gateway.actions || []
  })) || [];

  const emergencyCount = gatewayData?.summary?.emergency || 0;

  return (
    <Box>
      {/* Page Header */}
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Box>
          <Heading sx={{ fontSize: 5, mb: 1, display: 'flex', alignItems: 'center', gap: 2 }}>
            <ServerIcon size={24} />
            Gateways
          </Heading>
          <Text sx={{ color: 'fg.muted', fontSize: 2 }}>
            Manage and monitor your Ignition gateway containers
          </Text>
        </Box>
        
        <ButtonGroup>
          <Button 
            variant="danger" 
            size="small"
            onClick={handleResetAllTrials}
            disabled={resetAllMutation.isLoading || !gatewayData?.gateways?.length}
          >
            <ZapIcon size={16} sx={{ mr: 1 }} />
            Reset All Trials
          </Button>
          {emergencyCount > 0 && (
            <Button 
              variant="danger"
              onClick={handleResetEmergencyTrials}
              disabled={resetEmergencyMutation.isLoading}
            >
              <ZapIcon size={16} sx={{ mr: 1 }} />
              Emergency Reset ({emergencyCount})
            </Button>
          )}
          <Button onClick={handleRefresh} disabled={gatewaysLoading}>
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

      {/* Error Message */}
      {gatewaysError && (
        <Flash variant="danger" sx={{ mb: 4 }}>
          Failed to load gateways: {gatewaysError.type === 'network_error' ? gatewaysError.details : gatewaysError.message}
        </Flash>
      )}

      {/* Gateway Table */}
      {gatewaysLoading ? (
        <LoadingSpinner message="Loading gateways..." />
      ) : gatewayData?.gateways?.length > 0 ? (
        <Box sx={{ 
          border: '1px solid', 
          borderColor: 'border.default', 
          borderRadius: 2, 
          overflow: 'hidden' 
        }}>
          {/* Table Header */}
          <Box sx={{ 
            bg: 'canvas.subtle', 
            p: 3, 
            borderBottom: '1px solid', 
            borderColor: 'border.default',
            display: 'grid',
            gridTemplateColumns: '2fr 1fr 1.5fr 1fr 1fr',
            gap: 3,
            fontWeight: 'bold'
          }}>
            <Text>Gateway</Text>
            <Text>Status</Text>
            <Text>Trial Status</Text>
            <Text>Response Time</Text>
            <Text>Actions</Text>
          </Box>
          
          {/* Table Body */}
          {tableData.map((row, index) => (
            <Box
              key={row.id}
              sx={{
                p: 3,
                borderBottom: index < tableData.length - 1 ? '1px solid' : 'none',
                borderColor: 'border.default',
                display: 'grid',
                gridTemplateColumns: '2fr 1fr 1.5fr 1fr 1fr',
                gap: 3,
                alignItems: 'center',
                '&:hover': {
                  bg: 'canvas.subtle'
                }
              }}
            >
              {/* Gateway Name */}
              <Box>
                <Text sx={{ fontWeight: 'bold' }}>{row.name}</Text>
                <Text sx={{ fontSize: 1, color: 'fg.muted' }}>Port {row.port}</Text>
              </Box>
              
              {/* Status */}
              <StatusBadge 
                status={row.status} 
                variant={row.gateway.statusColor}
              />
              
              {/* Trial Status */}
              <Box>
                <Text sx={{ fontSize: 1, mb: 1 }}>
                  {row.trial?.display || 'Unknown'}
                </Text>
                <StatusBadge 
                  status={row.gateway.trial?.expired ? 'expired' : row.gateway.trial?.emergency ? 'emergency' : 'active'}
                  variant={row.gateway.trialColor}
                  size="small"
                />
              </Box>
              
              {/* Response Time */}
              <Text sx={{ fontSize: 1 }}>
                {row.responseTime ? `${row.responseTime}ms` : 'N/A'}
              </Text>
              
              {/* Actions */}
              <ActionMenu>
                <ActionMenu.Button
                  icon={KebabHorizontalIcon}
                  size="small"
                  aria-label={`Actions for ${row.name}`}
                />
                <ActionMenu.Overlay>
                  <ActionList>
                    <ActionList.Item 
                      onSelect={() => handleRestartGateway(row.gateway.name)}
                      disabled={restartMutation.isLoading || row.gateway.container_status !== 'running'}
                    >
                      <ActionList.LeadingVisual>
                        <PlayIcon />
                      </ActionList.LeadingVisual>
                      Restart Container
                    </ActionList.Item>
                    <ActionList.Item 
                      onSelect={() => handleResetTrial(row.gateway.name)}
                      disabled={resetTrialMutation.isLoading || row.gateway.trial?.expired}
                    >
                      <ActionList.LeadingVisual>
                        <ZapIcon />
                      </ActionList.LeadingVisual>
                      Reset Trial
                    </ActionList.Item>
                    <ActionList.Divider />
                    <ActionList.Item 
                      onSelect={() => {
                        setSelectedGateway(row.gateway);
                        setShowLogsDialog(true);
                      }}
                    >
                      <ActionList.LeadingVisual>
                        <LogIcon />
                      </ActionList.LeadingVisual>
                      View Logs
                    </ActionList.Item>
                  </ActionList>
                </ActionMenu.Overlay>
              </ActionMenu>
            </Box>
          ))}
        </Box>
      ) : (
        <Box sx={{ textAlign: 'center', py: 6, border: '1px solid', borderColor: 'border.default', borderRadius: 2 }}>
          <ServerIcon size={48} sx={{ color: 'fg.muted', mb: 3 }} />
          <Heading sx={{ fontSize: 3, mb: 2 }}>No Gateways Found</Heading>
          <Text sx={{ color: 'fg.muted', mb: 3 }}>
            No Ignition gateway containers are currently running or detected.
          </Text>
          <Button onClick={handleRefresh}>
            <SyncIcon size={16} sx={{ mr: 1 }} />
            Refresh
          </Button>
        </Box>
      )}

      {/* Summary */}
      {gatewayData?.summary && (
        <Box sx={{ mt: 4, p: 3, bg: 'canvas.subtle', borderRadius: 2 }}>
          <Text sx={{ fontSize: 1, color: 'fg.muted' }}>
            Summary: {gatewayData.total} gateways • 
            {gatewayData.summary.healthy} healthy • 
            {gatewayData.summary.unhealthy} unhealthy • 
            {gatewayData.summary.starting} starting
            {gatewayData.summary.emergency > 0 && (
              <Text sx={{ color: 'severe.fg', ml: 1 }}>
                • ⚠ {gatewayData.summary.emergency} emergency
              </Text>
            )}
          </Text>
        </Box>
      )}

      {/* Logs Dialog */}
      {showLogsDialog && selectedGateway && (
        <Dialog
          isOpen={showLogsDialog}
          onDismiss={() => setShowLogsDialog(false)}
          aria-labelledby="logs-dialog-title"
        >
          <Dialog.Header id="logs-dialog-title">
            Gateway Logs - {selectedGateway.displayName}
          </Dialog.Header>
          <Box sx={{ p: 3 }}>
            <Text>Logs functionality will be implemented in the next iteration.</Text>
          </Box>
        </Dialog>
      )}
    </Box>
  );
};

export default Gateways;