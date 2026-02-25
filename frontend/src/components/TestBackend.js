import React, { useState } from 'react';

const TestBackend = () => {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const testFetch = async () => {
    try {
      const response = await fetch('https://netraai-backend.onrender.com/api/dashboard/stats', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
      });
      const data = await response.json();
      setResult(JSON.stringify(data, null, 2));
      setError(null);
    } catch (err) {
      setError(err.message);
      setResult(null);
    }
  };

  return (
    <div style={{ padding: '20px', background: '#1a1a2e', color: 'white' }}>
      <h2>Backend Connection Test</h2>
      <button onClick={testFetch} style={{ padding: '10px 20px', marginBottom: '20px' }}>
        Test Backend Connection
      </button>
      {result && (
        <pre style={{ background: '#0f0f1e', padding: '10px', borderRadius: '5px' }}>
          {result}
        </pre>
      )}
      {error && (
        <div style={{ color: 'red', padding: '10px', background: '#2a0000', borderRadius: '5px' }}>
          Error: {error}
        </div>
      )}
    </div>
  );
};

export default TestBackend;
