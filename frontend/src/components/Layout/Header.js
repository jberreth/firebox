import React from 'react';
import { Box, Text, Button, Flash } from '@primer/react';
import { ThreeBarsIcon, BellIcon } from '@primer/octicons-react';
import { useHealthCheck } from '../../hooks/useSystem';
import StatusBadge from '../Common/StatusBadge';
import { formatDateTime } from '../../utils/formatters';

const Header = ({ onToggleSidebar }) => {
  const { data: healthData, isError: healthError } = useHealthCheck();

  const currentTime = new Date();

  return (
    <Box
      as="header"
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        p: 3,
        bg: 'canvas.subtle',
        borderBottom: '1px solid',
        borderColor: 'border.default',
        minHeight: '60px'
      }}
    >
      {/* Left section */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
        <Button
          variant="invisible"
          size="small"
          onClick={onToggleSidebar}
          sx={{ p: 1, display: { lg: 'none' } }} // Show only on smaller screens
        >
          <ThreeBarsIcon size={16} />
        </Button>
        
        <Text sx={{ fontSize: 2, color: 'fg.muted' }}>
          {formatDateTime(currentTime, 'EEEE, MMM dd, yyyy HH:mm')}
        </Text>
      </Box>

      {/* Right section */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
        {/* System health indicator */}
        {healthError ? (
          <Flash variant="danger" sx={{ p: 2 }}>
            <Text sx={{ fontSize: 1 }}>Health check failed</Text>
          </Flash>
        ) : (
          <StatusBadge 
            status={healthData?.status || 'unknown'} 
            type="system"
            size="small"
          />
        )}

        {/* Notifications (placeholder) */}
        <Button variant="invisible" size="small" sx={{ p: 1 }}>
          <BellIcon size={16} />
        </Button>

        {/* User menu (placeholder) */}
        <Box
          sx={{
            width: 32,
            height: 32,
            borderRadius: '50%',
            bg: 'accent.subtle',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <Text sx={{ fontSize: 1, fontWeight: 'bold', color: 'accent.fg' }}>
            FB
          </Text>
        </Box>
      </Box>
    </Box>
  );
};

export default Header;