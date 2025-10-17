import React, { useState } from 'react';
import { Box } from '@primer/react';
import Sidebar from './Sidebar';
import Header from './Header';

const Layout = ({ children }) => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
    // Save preference to localStorage
    localStorage.setItem('sidebarCollapsed', JSON.stringify(!sidebarCollapsed));
  };

  // Load sidebar state from localStorage on mount
  React.useEffect(() => {
    const saved = localStorage.getItem('sidebarCollapsed');
    if (saved) {
      setSidebarCollapsed(JSON.parse(saved));
    }
  }, []);

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bg: 'canvas.default' }}>
      {/* Sidebar */}
      <Sidebar collapsed={sidebarCollapsed} onToggle={toggleSidebar} />
      
      {/* Main content area */}
      <Box sx={{ 
        flex: 1, 
        display: 'flex', 
        flexDirection: 'column',
        ml: sidebarCollapsed ? '60px' : '280px',
        transition: 'margin-left 0.2s ease-in-out'
      }}>
        {/* Header */}
        <Header onToggleSidebar={toggleSidebar} />
        
        {/* Page content */}
        <Box 
          as="main" 
          sx={{ 
            flex: 1, 
            p: 4,
            bg: 'canvas.default',
            overflow: 'auto'
          }}
        >
          {children}
        </Box>
      </Box>
    </Box>
  );
};

export default Layout;