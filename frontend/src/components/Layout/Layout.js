import React from 'react';
import { Box } from '@primer/react';
import TopNavigation from './TopNavigation';

const Layout = ({ children }) => {
  return (
    <Box sx={{ minHeight: '100vh', bg: 'canvas.subtle' }}>
      {/* Top Navigation Bar */}
      <Box 
        sx={{
          bg: 'canvas.default', // Light background for header
          borderBottom: '1px solid',
          borderColor: 'border.default',
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
          bg: 'canvas.subtle' // Darker background for main content
        }}
      >
        {children}
      </Box>
    </Box>
  );
};

export default Layout;