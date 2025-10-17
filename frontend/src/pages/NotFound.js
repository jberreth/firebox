import React from 'react';
import { Box, Heading, Text, Button } from '@primer/react';
import { Link as RouterLink } from 'react-router-dom';
import { HomeIcon } from '@primer/octicons-react';

const NotFound = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        textAlign: 'center'
      }}
    >
      <Heading sx={{ fontSize: 6, mb: 2, color: 'fg.muted' }}>404</Heading>
      <Heading sx={{ fontSize: 4, mb: 2 }}>Page Not Found</Heading>
      <Text sx={{ color: 'fg.muted', fontSize: 2, mb: 4, maxWidth: '400px' }}>
        The page you're looking for doesn't exist or has been moved.
      </Text>
      <Button as={RouterLink} to="/" variant="primary">
        <HomeIcon size={16} sx={{ mr: 1 }} />
        Back to Dashboard
      </Button>
    </Box>
  );
};

export default NotFound;