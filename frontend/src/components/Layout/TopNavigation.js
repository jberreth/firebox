import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { 
  Box, 
  Text, 
  Button,
  Octicon
} from '@primer/react';
import { 
  FlameIcon,
  HomeIcon,
  ServerIcon,
  GearIcon,
  GraphIcon
} from '@primer/octicons-react';

const TopNavigation = () => {
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: HomeIcon },
    { path: '/gateways', label: 'Gateways', icon: ServerIcon },
    { path: '/system', label: 'System', icon: GraphIcon },
    { path: '/settings', label: 'Settings', icon: GearIcon }
  ];

  return (
    <Box 
      sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        maxWidth: '1280px',
        mx: 'auto',
        px: 4,
        py: 3
      }}
    >
      {/* Logo and Brand */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <Octicon icon={FlameIcon} size={24} sx={{ color: 'danger.fg' }} />
        <Text 
          as="h1" 
          sx={{ 
            fontSize: 3, 
            fontWeight: 'bold', 
            color: 'fg.default',
            m: 0
          }}
        >
          Firebox
        </Text>
      </Box>

      {/* Horizontal Navigation Menu */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Button
              key={item.path}
              as={Link}
              to={item.path}
              variant={isActive ? "primary" : "invisible"}
              size="medium"
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 2,
                px: 3,
                py: 2,
                textDecoration: 'none',
                fontSize: 1,
                fontWeight: isActive ? 'semibold' : 'normal',
                color: isActive ? 'btn.primary.text' : 'fg.default',
                '&:hover': {
                  textDecoration: 'none',
                  bg: isActive ? 'btn.primary.hoverBg' : 'btn.hoverBg'
                }
              }}
            >
              <Octicon icon={item.icon} size={16} />
              {item.label}
            </Button>
          );
        })}
      </Box>

      {/* User Actions */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        {/* Emergency Reset Button */}
        <Button 
          variant="danger" 
          size="small"
          sx={{ 
            fontSize: 0,
            px: 3,
            py: 1
          }}
        >
          Emergency Reset
        </Button>
      </Box>
    </Box>
  );
};

export default TopNavigation;