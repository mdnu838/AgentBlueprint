import React, { useState, useEffect } from 'react';
import ReactFlow, { Background, Controls } from 'reactflow';
import 'reactflow/dist/style.css';
import { runWorkflow, getWorkflowStatus } from './api';

const initialNodes = [
  {
    id: '1',
    position: { x: 250, y: 50 },
    data: { label: 'Start' },
    style: { border: '1px solid #777', padding: 10, background: '#fff' }
  },
  {
    id: '2',
    position: { x: 250, y: 200 },
    data: { label: 'Agent: Researcher' },
    style: { border: '1px solid #777', padding: 10, background: '#e0f7fa' }
  },
  {
    id: '3',
    position: { x: 250, y: 350 },
    data: { label: 'Agent: Writer' },
    style: { border: '1px solid #777', padding: 10, background: '#e0f7fa' }
  }
];

const initialEdges = [
  { id: 'e1-2', source: '1', target: '2', animated: true },
  { id: 'e2-3', source: '2', target: '3', animated: true }
];

const sampleYaml = `
workflow:
  type: sequential
  steps:
    - agent: researcher
    - agent: writer
`;

function App() {
  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);
  const [yaml, setYaml] = useState(sampleYaml);
  const [inputData, setInputData] = useState('Write a report on AI');
  const [backend, setBackend] = useState('local');
  const [runId, setRunId] = useState(null);
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);

  const handleRun = async () => {
    try {
      const data = await runWorkflow(yaml, inputData, backend);
      setRunId(data.run_id);
      setStatus(data.status);
      setResult(null);
    } catch (e) {
      alert("Error starting workflow: " + e.message);
    }
  };

  useEffect(() => {
    let interval;
    if (runId && (status === 'pending' || status === 'running')) {
      interval = setInterval(async () => {
        try {
          const data = await getWorkflowStatus(runId);
          setStatus(data.status);
          if (data.status === 'completed' || data.status === 'success') {
            setResult(data.result);
            clearInterval(interval);
          } else if (data.status === 'error' || data.status === 'failed') {
             setResult(data.error);
             clearInterval(interval);
          }
        } catch (e) {
          console.error("Error polling:", e);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [runId, status]);

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'sans-serif' }}>
      <div style={{ width: '30%', padding: '20px', borderRight: '1px solid #ccc', display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <h2>AgentBlueprint</h2>

        <div>
          <label>Workflow YAML:</label>
          <textarea
            value={yaml}
            onChange={e => setYaml(e.target.value)}
            style={{ width: '100%', height: '150px', fontFamily: 'monospace' }}
          />
        </div>

        <div>
          <label>Input Data:</label>
          <input
            type="text"
            value={inputData}
            onChange={e => setInputData(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>

        <div>
          <label>Backend:</label>
          <select value={backend} onChange={e => setBackend(e.target.value)} style={{ width: '100%' }}>
            <option value="local">Local</option>
            <option value="celery">Celery</option>
            <option value="temporal">Temporal</option>
          </select>
        </div>

        <button onClick={handleRun} style={{ padding: '10px', background: '#007bff', color: '#fff', border: 'none', cursor: 'pointer' }}>
          Run Workflow
        </button>

        {runId && (
          <div style={{ marginTop: '20px', padding: '10px', background: '#f8f9fa', border: '1px solid #ddd' }}>
            <p><strong>Run ID:</strong> <br/> {runId}</p>
            <p><strong>Status:</strong> {status}</p>
            {result && (
              <div>
                <strong>Result:</strong>
                <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word', fontSize: '12px' }}>
                  {JSON.stringify(result, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </div>

      <div style={{ flex: 1, position: 'relative' }}>
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </div>
  );
}

export default App;
