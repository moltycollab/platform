// src/services/authService.ts
import apiClient from './apiClient';
import { User } from '@/types/User';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export const authService = {
  // Redirect to GitHub OAuth
  redirectToGithubLogin(): void {
    window.location.href = `${apiClient.defaults.baseURL}/auth/github`;
  },

  // Handle GitHub callback and save token
  async handleGithubCallback(code: string): Promise<User> {
    // In a real app, you'd exchange the code for a token on your backend
    // For now, we'll simulate this by making a request to our backend
    const response = await apiClient.get(`/auth/github/callback?code=${code}`);
    
    if (response.data.access_token) {
      // Save the token to localStorage
      localStorage.setItem('access_token', response.data.access_token);
      
      // Return the user data
      return response.data.user;
    }
    
    throw new Error('Failed to authenticate with GitHub');
  },

  // Get current user
  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get('/users/me');
    return response.data;
  },

  // Logout
  logout(): void {
    localStorage.removeItem('access_token');
    window.location.href = '/';
  },

  // Check if user is authenticated
  isAuthenticated(): boolean {
    return !!localStorage.getItem('access_token');
  }
};