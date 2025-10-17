import React from 'react';
import { Box, Spinner, Text } from '@primer/react';

const LoadingSpinner = ({ 
  size = 'medium', 
  message = 'Loading...', 
  fullScreen = false,
  inline = false 
}) => {
  const spinnerSize = {
    small: 16,
    medium: 32,
    large: 48
  }[size];

  const Container = fullScreen ? 
    ({ children }) => (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          bg: 'canvas.default'
        }}
      >
        {children}
      </Box>
    ) : 
    ({ children }) => (
      <Box
        sx={{
          display: 'flex',
          flexDirection: inline ? 'row' : 'column',
          alignItems: 'center',
          justifyContent: 'center',
          p: inline ? 2 : 4,
          gap: 2
        }}
      >
        {children}
      </Box>
    );

  return (
    <Container>
      <Spinner size={spinnerSize} />
      {message && (
        <Text sx={{ 
          color: 'fg.muted', 
          fontSize: inline ? 1 : 2,
          ml: inline ? 2 : 0,
          mt: inline ? 0 : 2
        }}>
          {message}
        </Text>
      )}
    </Container>
  );
};

export default LoadingSpinner;