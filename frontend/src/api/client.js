import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chatbot API calls
export const chatbotAPI = {
  sendMessage: (message) =>
    api.post('/chatbot/message', { message }),
  
  detectDisease: (file) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/chatbot/disease-detection', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  getChatHistory: () =>
    api.get('/chatbot/history'),
  
  clearHistory: () =>
    api.post('/chatbot/clear-history'),
  
  getIntents: () =>
    api.get('/chatbot/intents'),
};

// Predictions API calls
export const predictionsAPI = {
  groundwaterPrediction: (data) =>
    api.post('/predictions/groundwater', data),
  
  productionForecast: (data) =>
    api.post('/predictions/production', data),
  
  irrigationSchedule: (data) =>
    api.post('/predictions/irrigation-schedule', data),
  
  fertilizerSchedule: (data) =>
    api.post('/predictions/fertilizer-schedule', data),
  
  optimizeResources: (data) =>
    api.post('/predictions/optimize-resources', data),
};

export default api;
