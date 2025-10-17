import React from 'react';
import { Box, Heading, Text } from '@primer/react';

const Settings = () => {
  return (
    <Box>
      <Heading sx={{ fontSize: 5, mb: 2 }}>Settings</Heading>
      <Text sx={{ color: 'fg.muted', fontSize: 2 }}>
        Configuration and preferences
      </Text>
      <Box sx={{ mt: 4, p: 4, border: '1px solid', borderColor: 'border.default', borderRadius: 2 }}>
        <Text>Settings interface coming soon...</Text>
      </Box>
    </Box>
  );
};

export default Settings;