import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  FormControl,
  Select,
  Text,
  Flash,
  Spinner,
  Octicon
} from '@primer/react';
import {
  PulseIcon,
  CheckIcon,
  XIcon,
  ClockIcon,
  GlobeIcon
} from '@primer/octicons-react';

const GatewayPingTool = () => {
  const [gateways, setGateways] = useState([]);
  const [sourceGateway, setSourceGateway] = useState('');
  const [targetGateway, setTargetGateway] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [pingResult, setPingResult] = useState(null);
  const [testingAll, setTestingAll] = useState(false);
  const [allResults, setAllResults] = useState([]);

  // Fetch available gateways on component mount
  useEffect(() => {
    fetchGateways();
  }, []);

  const fetchGateways = async () => {
    try {
      const response = await fetch('/api/gateways/list');
      const data = await response.json();
      setGateways(data.gateways || []);
    } catch (error) {
      console.error('Failed to fetch gateways:', error);
    }
  };

  const handlePingTest = async () => {
    if (!sourceGateway || !targetGateway) {
      return;
    }

    setIsLoading(true);
    setPingResult(null);

    try {
      const response = await fetch('/api/gateways/ping', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          source: sourceGateway,
          target: targetGateway,
        }),
      });

      const result = await response.json();
      setPingResult(result);
    } catch (error) {
      setPingResult({
        success: false,
        error: 'Failed to perform ping test',
        source: sourceGateway,
        target: targetGateway,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestAllConnections = async () => {
    setTestingAll(true);
    setAllResults([]);

    try {
      const response = await fetch('/api/gateways/connectivity');
      const data = await response.json();
      setAllResults(data.results || []);
    } catch (error) {
      console.error('Failed to test all connections:', error);
    } finally {
      setTestingAll(false);
    }
  };

  const getStatusIcon = (success) => {
    if (success) {
      return <Octicon icon={CheckIcon} sx={{ color: 'success.fg' }} />;
    }
    return <Octicon icon={XIcon} sx={{ color: 'danger.fg' }} />;
  };

  const formatResponseTime = (responseTime) => {
    if (responseTime == null) return 'N/A';
    return `${responseTime}ms`;
  };

  return (
    <Box sx={{ p: 3, border: '1px solid', borderColor: 'border.default', borderRadius: 2 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
        <Octicon icon={GlobeIcon} sx={{ mr: 2 }} />
        <Text sx={{ fontSize: 2, fontWeight: 'bold' }}>Gateway Connectivity Test</Text>
      </Box>

      {/* Individual Ping Test */}
      <Box sx={{ mb: 4 }}>
        <Text sx={{ fontSize: 1, fontWeight: 'bold', mb: 2 }}>Test Individual Connection</Text>
        
        <Box sx={{ display: 'flex', gap: 3, alignItems: 'flex-end', mb: 3 }}>
          <Box sx={{ flex: 1 }}>
            <FormControl>
              <FormControl.Label>Source Gateway</FormControl.Label>
              <Select
                value={sourceGateway}
                onChange={(e) => setSourceGateway(e.target.value)}
                sx={{ width: '100%' }}
              >
                <Select.Option value="">Select source...</Select.Option>
                {gateways.map((gateway) => (
                  <Select.Option key={gateway.name} value={gateway.name}>
                    {gateway.name}
                  </Select.Option>
                ))}
              </Select>
            </FormControl>
          </Box>

          <Box sx={{ flex: 1 }}>
            <FormControl>
              <FormControl.Label>Target Gateway</FormControl.Label>
              <Select
                value={targetGateway}
                onChange={(e) => setTargetGateway(e.target.value)}
                sx={{ width: '100%' }}
              >
                <Select.Option value="">Select target...</Select.Option>
                {gateways.map((gateway) => (
                  <Select.Option key={gateway.name} value={gateway.name}>
                    {gateway.name}
                  </Select.Option>
                ))}
              </Select>
            </FormControl>
          </Box>

          <Button
            onClick={handlePingTest}
            disabled={!sourceGateway || !targetGateway || isLoading}
            sx={{ display: 'flex', alignItems: 'center', gap: 2 }}
          >
            {isLoading ? (
              <Spinner size="small" />
            ) : (
              <Octicon icon={PulseIcon} />
            )}
            Ping Test
          </Button>
        </Box>

        {/* Individual Ping Result */}
        {pingResult && (
          <Box sx={{ mb: 3 }}>
            <Flash variant={pingResult.success ? 'success' : 'danger'}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                {getStatusIcon(pingResult.success)}
                <Box>
                  <Text sx={{ fontWeight: 'bold' }}>
                    {pingResult.source} → {pingResult.target}
                  </Text>
                  {pingResult.success ? (
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mt: 1 }}>
                      <Text sx={{ fontSize: 0 }}>
                        Response Time: {formatResponseTime(pingResult.response_time)}
                      </Text>
                      <Text sx={{ fontSize: 0 }}>
                        Method: {pingResult.method}
                      </Text>
                    </Box>
                  ) : (
                    <Text sx={{ fontSize: 0, mt: 1 }}>
                      Error: {pingResult.error}
                    </Text>
                  )}
                </Box>
              </Box>
            </Flash>
          </Box>
        )}
      </Box>

      {/* Test All Connections */}
      <Box sx={{ borderTop: '1px solid', borderColor: 'border.default', pt: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Text sx={{ fontSize: 1, fontWeight: 'bold' }}>Test All Configured Connections</Text>
          <Button
            onClick={handleTestAllConnections}
            disabled={testingAll}
            variant="primary"
            sx={{ display: 'flex', alignItems: 'center', gap: 2 }}
          >
            {testingAll ? (
              <Spinner size="small" />
            ) : (
              <Octicon icon={GlobeIcon} />
            )}
            Test All
          </Button>
        </Box>

        {/* All Connections Results */}
        {allResults.length > 0 && (
          <Box sx={{ display: 'grid', gap: 2 }}>
            {allResults.map((result, index) => (
              <Box
                key={index}
                sx={{
                  p: 2,
                  border: '1px solid',
                  borderColor: result.success ? 'success.muted' : 'danger.muted',
                  borderRadius: 2,
                  backgroundColor: result.success ? 'success.subtle' : 'danger.subtle',
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    {getStatusIcon(result.success)}
                    <Text sx={{ fontWeight: 'bold' }}>
                      {result.source} → {result.target}
                    </Text>
                  </Box>
                  
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 3, fontSize: 0 }}>
                    {result.success && (
                      <>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Octicon icon={ClockIcon} />
                          <Text>{formatResponseTime(result.response_time)}</Text>
                        </Box>
                        <Text sx={{ color: 'fg.muted' }}>
                          via {result.method}
                        </Text>
                      </>
                    )}
                    {!result.success && (
                      <Text sx={{ color: 'danger.fg', fontSize: 0 }}>
                        {result.error}
                      </Text>
                    )}
                  </Box>
                </Box>
              </Box>
            ))}
          </Box>
        )}

        {testingAll && (
          <Box sx={{ textAlign: 'center', py: 4 }}>
            <Spinner size="medium" />
            <Text sx={{ display: 'block', mt: 2, color: 'fg.muted' }}>
              Testing gateway connections...
            </Text>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default GatewayPingTool;