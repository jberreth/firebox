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
        py: 3,
        bg: '#161b22' // GitHub header background
      }}
    >
      {/* Logo and Brand - GitHub Style */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
        <Octicon icon={FlameIcon} size={32} sx={{ color: '#f85149' }} /> {/* GitHub red accent */}
        <Text 
          as="h1" 
          sx={{ 
            fontSize: 4, 
            fontWeight: 'bold', 
            color: '#f0f6fc', // GitHub primary text white
            m: 0,
            letterSpacing: '-0.5px'
          }}
        >
          Firebox
        </Text>
      </Box>

      {/* Horizontal Navigation Menu - GitHub Style */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 0 }}>
        {navItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Button
              key={item.path}
              as={Link}
              to={item.path}
              variant="invisible"
              size="medium"
              sx={{
                display: 'flex',
                alignItems: 'center',
                gap: 2,
                px: 4,
                py: 3,
                textDecoration: 'none',
                fontSize: 2,
                fontWeight: isActive ? 'semibold' : 'normal',
                color: isActive ? '#f0f6fc' : '#7d8590', // GitHub text colors
                borderBottom: isActive ? '2px solid #fd7e14' : '2px solid transparent', // GitHub orange accent
                borderRadius: 0,
                '&:hover': {
                  textDecoration: 'none',
                  color: '#f0f6fc',
                  bg: 'rgba(177, 186, 196, 0.12)' // GitHub hover background
                },
                '&:focus': {
                  outline: '2px solid #1f6feb',
                  outlineOffset: '-2px'
                }
              }}
            >
              <Octicon 
                icon={item.icon} 
                size={16} 
                sx={{ 
                  color: isActive ? '#f0f6fc' : '#7d8590'
                }} 
              />
              {item.label}
            </Button>
          );
        })}
      </Box>

      {/* User Actions - GitHub Style */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
        {/* Emergency Reset Button */}
        <Button 
          variant="danger" 
          size="small"
          sx={{ 
            fontSize: 1,
            px: 3,
            py: 2,
            bg: '#da3633', // GitHub danger red
            color: '#f0f6fc',
            border: '1px solid rgba(240, 246, 252, 0.1)',
            '&:hover': {
              bg: '#b91c1c'
            }
          }}
        >
          Emergency Reset
        </Button>
      </Box>
    </Box>
  );
};

export default TopNavigation;