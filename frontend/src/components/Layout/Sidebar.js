import React from 'react';
import { useLocation, Link as RouterLink } from 'react-router-dom';
import { 
  Box, 
  Text, 
  NavList, 
  Tooltip,
  Button,
  Heading
} from '@primer/react';
import { 
  HomeIcon,
  ServerIcon,
  PulseIcon,
  GearIcon,
  ThreeBarsIcon,
  FlameIcon
} from '@primer/octicons-react';
import { ROUTES } from '../../utils/constants';

const Sidebar = ({ collapsed, onToggle }) => {
  const location = useLocation();

  const navigationItems = [
    {
      href: ROUTES.DASHBOARD,
      icon: HomeIcon,
      label: 'Dashboard',
      description: 'Overview and status'
    },
    {
      href: ROUTES.GATEWAYS,
      icon: ServerIcon,
      label: 'Gateways',
      description: 'Gateway management'
    },
    {
      href: ROUTES.SYSTEM,
      icon: PulseIcon,
      label: 'System',
      description: 'System health and logs'
    },
    {
      href: ROUTES.SETTINGS,
      icon: GearIcon,
      label: 'Settings',
      description: 'Configuration and preferences'
    }
  ];

  const NavItem = ({ item }) => {
    const isActive = location.pathname === item.href;
    
    const navItem = (
      <NavList.Item
        as={RouterLink}
        to={item.href}
        aria-current={isActive ? 'page' : undefined}
        sx={{
          color: isActive ? 'accent.fg' : 'fg.default',
          textDecoration: 'none',
          '&:hover': {
            textDecoration: 'none',
            bg: 'neutral.subtle'
          }
        }}
      >
        <NavList.LeadingVisual>
          <item.icon size={16} />
        </NavList.LeadingVisual>
        {!collapsed && item.label}
      </NavList.Item>
    );

    if (collapsed) {
      return (
        <Tooltip text={item.description} direction="e">
          {navItem}
        </Tooltip>
      );
    }

    return navItem;
  };

  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        height: '100vh',
        width: collapsed ? '60px' : '280px',
        bg: 'canvas.subtle',
        borderRight: '1px solid',
        borderColor: 'border.default',
        display: 'flex',
        flexDirection: 'column',
        transition: 'width 0.2s ease-in-out',
        zIndex: 100
      }}
    >
      {/* Header */}
      <Box
        sx={{
          p: 3,
          borderBottom: '1px solid',
          borderColor: 'border.default',
          display: 'flex',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'space-between'
        }}
      >
        {!collapsed && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <FlameIcon size={24} sx={{ color: 'accent.fg' }} />
            <Heading sx={{ fontSize: 3, m: 0 }}>Firebox</Heading>
          </Box>
        )}
        
        {collapsed && (
          <FlameIcon size={24} sx={{ color: 'accent.fg' }} />
        )}
        
        {!collapsed && (
          <Button
            variant="invisible"
            size="small"
            onClick={onToggle}
            sx={{ p: 1 }}
          >
            <ThreeBarsIcon size={16} />
          </Button>
        )}
      </Box>

      {/* Navigation */}
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <NavList sx={{ p: 2 }}>
          {navigationItems.map((item, index) => (
            <NavItem key={index} item={item} />
          ))}
        </NavList>
      </Box>

      {/* Footer / Collapse button for collapsed state */}
      {collapsed && (
        <Box sx={{ p: 2, borderTop: '1px solid', borderColor: 'border.default' }}>
          <Tooltip text="Expand sidebar" direction="e">
            <Button
              variant="invisible"
              size="small"
              onClick={onToggle}
              sx={{ width: '100%', justifyContent: 'center' }}
            >
              <ThreeBarsIcon size={16} />
            </Button>
          </Tooltip>
        </Box>
      )}

      {/* Status indicator */}
      {!collapsed && (
        <Box
          sx={{
            p: 3,
            borderTop: '1px solid',
            borderColor: 'border.default'
          }}
        >
          <Text sx={{ fontSize: 0, color: 'fg.muted' }}>
            Firebox v1.0.0
          </Text>
        </Box>
      )}
    </Box>
  );
};

export default Sidebar;