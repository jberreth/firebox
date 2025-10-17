import React from 'react';
import { Box, Heading, Text } from '@primer/react';

const Gateways = () => {
  return (
    <Box>
      <Heading sx={{ fontSize: 5, mb: 2 }}>Gateways</Heading>
      <Text sx={{ color: 'fg.muted', fontSize: 2 }}>
        Detailed gateway management and configuration
      </Text>
      <Box sx={{ mt: 4, p: 4, border: '1px solid', borderColor: 'border.default', borderRadius: 2 }}>
        <Text>Gateway management interface coming soon...</Text>
      </Box>
    </Box>
  );
};

export default Gateways;