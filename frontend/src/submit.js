// submit.js

import { useState } from 'react';
import { useStore } from './store';
import { shallow } from 'zustand/shallow';

export const SubmitButton = () => {
  const [executionLogs, setExecutionLogs] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  const { nodes, edges } = useStore(
    (state) => ({
      nodes: state.nodes,
      edges: state.edges,
    }),
    shallow
  );

  // Original submit — validates DAG structure
  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:8000/pipelines/parse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nodes, edges }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const result = await response.json();

      const message = `
Pipeline Analysis:
• Number of Nodes: ${result.num_nodes}
• Number of Edges: ${result.num_edges}
• Is Directed Acyclic Graph: ${result.is_dag ? 'Yes ✓' : 'No ✗'}
      `;

      alert(message.trim());
    } catch (error) {
      alert(`Failed to submit pipeline.\n\n${error.message}`);
    }
  };

  // New — executes the pipeline and shows logs
  const handleRun = async () => {
    setIsRunning(true);
    setExecutionLogs(null);

    try {
      const response = await fetch('http://localhost:8000/pipelines/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nodes, edges }),
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || `Request failed with status ${response.status}`);
      }

      const result = await response.json();
      setExecutionLogs(result.execution_log);
    } catch (error) {
      alert(`Failed to run pipeline.\n\n${error.message}`);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="submit-container">
      {/* Original validate button */}
      <button className="submit-button" onClick={handleSubmit}>
        Submit Pipeline
      </button>

      {/* New run button */}
      <button
        className="submit-button run-button"
        onClick={handleRun}
        disabled={isRunning}
        style={{ marginLeft: '10px', backgroundColor: isRunning ? '#555' : '#22c55e' }}
      >
        {isRunning ? 'Running...' : '▶ Run Pipeline'}
      </button>

      {/* Execution logs panel */}
      {executionLogs && (
        <div style={{
          marginTop: '16px',
          background: '#1e1e1e',
          border: '1px solid #333',
          borderRadius: '8px',
          padding: '12px',
          maxWidth: '400px',
          maxHeight: '300px',
          overflowY: 'auto',
          fontSize: '13px',
          color: '#fff',
        }}>
          <strong style={{ color: '#22c55e' }}>✅ Execution Log</strong>
          {executionLogs.map((log, index) => (
            <div key={index} style={{
              marginTop: '8px',
              padding: '8px',
              background: log.status === 'success' ? '#14532d' : '#7f1d1d',
              borderRadius: '6px',
            }}>
              <div><strong>Node:</strong> {log.node_id} ({log.node_type})</div>
              <div><strong>Status:</strong> {log.status === 'success' ? '✅ Success' : '❌ Failed'}</div>
              <div><strong>Output:</strong> {JSON.stringify(log.output)}</div>
              {log.error && <div style={{ color: '#f87171' }}><strong>Error:</strong> {log.error}</div>}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};