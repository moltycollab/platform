// src/services/apiClient.ts
import axios from 'axios';

const BACKEND_API_URL = process.env.BACKEND_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: `${BACKEND_API_URL}/api/v1`,
  timeout: 10000,
});

// Add a request interceptor to include the token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle token expiration
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Clear the token and redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/auth/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;