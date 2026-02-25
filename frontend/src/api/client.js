import axios from 'axios';

// Production backend URL on Render
const PRODUCTION_BACKEND_URL = 'https://netraai-backend.onrender.com';

const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (window.location.hostname === 'localhost' ? 'http://localhost:8000' : PRODUCTION_BACKEND_URL);

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Dashboard
  getDashboardStats: () => apiClient.get('/api/dashboard/stats'),
  
  // Companies
  getCompanies: (riskCategory = null, limit = 100) => 
    apiClient.get('/api/companies', { params: { risk_category: riskCategory, limit } }),
  
  getCompanyDetail: (companyId) => 
    apiClient.get(`/api/company/${companyId}`),
  
  // Network
  getNetworkGraph: (entityId = null, depth = 2) => 
    apiClient.get('/api/network/graph', { params: { entity_id: entityId, depth } }),
  
  // Investigation
  getInvestigationSummary: (entityId) => 
    apiClient.get(`/api/investigation/summary/${entityId}`),
  
  // Clusters
  getFraudClusters: () => 
    apiClient.get('/api/clusters'),
};

export default apiClient;
