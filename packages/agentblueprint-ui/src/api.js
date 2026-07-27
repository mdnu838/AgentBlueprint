import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const runWorkflow = async (workflowYaml, inputData, backend) => {
  const response = await api.post('/workflows/run', {
    workflow_yaml: workflowYaml,
    input_data: inputData,
    backend: backend,
  });
  return response.data;
};

export const getWorkflowStatus = async (runId) => {
  const response = await api.get(`/workflows/${runId}/status`);
  return response.data;
};
