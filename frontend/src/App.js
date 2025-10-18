import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@primer/react';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard';
import Gateways from './pages/Gateways';
import System from './pages/System';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound';
import ErrorBoundary from './components/Common/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <Box sx={{ minHeight: '100vh', bg: '#0d1117' }}> {/* GitHub dark background */}
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/gateways" element={<Gateways />} />
            <Route path="/system" element={<System />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Layout>
      </Box>
    </ErrorBoundary>
  );
}

export default App;