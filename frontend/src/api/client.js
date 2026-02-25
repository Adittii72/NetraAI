import axios from 'axios';

// Determine API URL based on environment
const getApiUrl = () => {
  // If REACT_APP_API_URL is set, use it
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // If running on localhost, use local backend
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:8000';
  }
  
  // Otherwise, use production backend
  return 'https://netraai-backend.onrender.com';
};

const API_BASE_URL = getApiUrl();

console.log('API Base URL:', API_BASE_URL); // Debug log

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
