import React from 'react';
import { Label, Octicon } from '@primer/react';
import { 
  CheckIcon, 
  XIcon, 
  ClockIcon, 
  AlertIcon,
  StopIcon
} from '@primer/octicons-react';
import { GATEWAY_STATUS, GATEWAY_STATUS_COLORS } from '../../utils/constants';

const StatusBadge = ({ 
  status, 
  variant,
  type = 'gateway', 
  size = 'medium',
  showIcon = true,
  ...props 
}) => {
  // Determine the appropriate icon based on status and type
  const getStatusIcon = (status, type) => {
    if (type === 'gateway') {
      switch (status) {
        case GATEWAY_STATUS.HEALTHY:
          return CheckIcon;
        case GATEWAY_STATUS.UNHEALTHY:
          return XIcon;
        case GATEWAY_STATUS.STARTING:
          return ClockIcon;
        case GATEWAY_STATUS.STOPPED:
          return StopIcon;
        default:
          return AlertIcon;
      }
    }
    
    // Default icons for other types
    switch (status) {
      case 'success':
      case 'healthy':
      case 'active':
        return CheckIcon;
      case 'error':
      case 'failed':
      case 'unhealthy':
        return XIcon;
      case 'warning':
      case 'attention':
        return AlertIcon;
      case 'loading':
      case 'pending':
        return ClockIcon;
      default:
        return AlertIcon;
    }
  };

  // Determine the variant based on status
  const getStatusVariant = (status, type) => {
    if (type === 'gateway') {
      return GATEWAY_STATUS_COLORS[status] || 'secondary';
    }
    
    // Map common status strings to Primer variants
    switch (status) {
      case 'success':
      case 'healthy':
      case 'active':
      case 'online':
        return 'success';
      case 'error':
      case 'failed':
      case 'unhealthy':
      case 'offline':
        return 'danger';
      case 'warning':
      case 'attention':
      case 'degraded':
        return 'attention';
      case 'loading':
      case 'pending':
      case 'starting':
        return 'accent';
      default:
        return 'secondary';
    }
  };

  const IconComponent = getStatusIcon(status, type);
  const badgeVariant = variant || getStatusVariant(status, type);
  
  // Format the status text
  const formatStatusText = (status) => {
    return status
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  };

  return (
    <Label 
      variant={badgeVariant} 
      size={size}
      sx={{ 
        display: 'inline-flex', 
        alignItems: 'center', 
        gap: 1,
        ...props.sx 
      }}
      {...props}
    >
      {showIcon && <Octicon icon={IconComponent} size={12} />}
      {formatStatusText(status)}
    </Label>
  );
};

export default StatusBadge;