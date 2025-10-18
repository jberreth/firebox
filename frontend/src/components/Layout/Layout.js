import React from 'react';
import { Box } from '@primer/react';
import TopNavigation from './TopNavigation';

const Layout = ({ children }) => {
  return (
    <Box sx={{ minHeight: '100vh', bg: '#0d1117' }}> {/* GitHub dark background */}
      {/* Top Navigation Bar - GitHub Header Style */}
      <Box 
        sx={{
          bg: '#161b22', // GitHub header background
          borderBottom: '1px solid #21262d', // GitHub border color
          position: 'sticky',
          top: 0,
          zIndex: 100
        }}
      >
        <TopNavigation />
      </Box>
      
      {/* Main Content Area */}
      <Box 
        as="main" 
        sx={{ 
          maxWidth: '1280px',
          mx: 'auto',
          p: 4,
          bg: '#0d1117' // GitHub main background
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;