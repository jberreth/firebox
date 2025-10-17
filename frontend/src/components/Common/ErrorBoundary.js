import React from 'react';
import { Box, Heading, Text, Button, Flash } from '@primer/react';
import { AlertIcon, SyncIcon } from '@primer/octicons-react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // Log the error to console and any error reporting service
    console.error('Error Boundary caught an error:', error, errorInfo);
    
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // You could also log the error to an error reporting service here
    // errorReportingService.logError(error, errorInfo);
  }

  handleReload = () => {
    // Clear error state and reload the page
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.reload();
  };

  handleRetry = () => {
    // Just clear the error state to retry rendering
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      // Fallback UI
      return (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            p: 4,
            bg: 'canvas.default',
            color: 'fg.default'
          }}
        >
          <Box sx={{ textAlign: 'center', maxWidth: '500px' }}>
            <AlertIcon size={48} sx={{ color: 'danger.fg', mb: 3 }} />
            
            <Heading sx={{ mb: 2, fontSize: 4 }}>
              Oops! Something went wrong
            </Heading>
            
            <Text sx={{ mb: 4, color: 'fg.muted', fontSize: 2 }}>
              An unexpected error occurred while rendering this page. 
              This has been logged and will be investigated.
            </Text>
            
            {process.env.NODE_ENV === 'development' && this.state.error && (
              <Flash variant="danger" sx={{ mb: 4, textAlign: 'left' }}>
                <Text sx={{ fontFamily: 'mono', fontSize: 1, wordBreak: 'break-all' }}>
                  <strong>Error:</strong> {this.state.error.toString()}
                  <br />
                  <strong>Component Stack:</strong>
                  <pre>{this.state.errorInfo.componentStack}</pre>
                </Text>
              </Flash>
            )}
            
            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
              <Button onClick={this.handleRetry} sx={{ mr: 2 }}>
                <SyncIcon size={16} sx={{ mr: 1 }} />
                Try Again
              </Button>
              
              <Button variant="outline" onClick={this.handleReload}>
                Reload Page
              </Button>
            </Box>
          </Box>
        </Box>
      );
    }

    // No error, render children normally
    return this.props.children;
  }
}

export default ErrorBoundary;