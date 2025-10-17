import React from 'react';
import { Box, Heading, Text } from '@primer/react';

const System = () => {
  return (
    <Box>
      <Heading sx={{ fontSize: 5, mb: 2 }}>System</Heading>
      <Text sx={{ color: 'fg.muted', fontSize: 2 }}>
        System health monitoring, logs, and diagnostics
      </Text>
      <Box sx={{ mt: 4, p: 4, border: '1px solid', borderColor: 'border.default', borderRadius: 2 }}>
        <Text>System monitoring interface coming soon...</Text>
      </Box>
    </Box>
  );
};

export default System;