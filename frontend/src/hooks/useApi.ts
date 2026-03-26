// src/hooks/useApi.ts
import useSWR from 'swr';
import apiClient from '@/services/apiClient';

// Define a fetcher function for SWR
const fetcher = (url: string) => apiClient.get(url).then(res => res.data);

// Generic hook for fetching data with SWR
export const useApi = <T>(url: string, options?: any) => {
  const { data, error, mutate, isLoading } = useSWR<T>(url, fetcher, options);

  return {
    data,
    error,
    mutate, // Function to manually trigger a re-fetch
    isLoading,
  };
};

// Specific hooks for common entities

// Hook for fetching user data
export const useUser = (id: number) => {
  return useApi<any>(`/users/${id}`);
};

// Hook for fetching all users
export const useUsers = (params?: { skip?: number; limit?: number }) => {
  const queryParams = new URLSearchParams();
  if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
  if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
  
  return useApi<any>(`/users/?${queryParams.toString()}`);
};

// Hook for fetching a project by ID
export const useProject = (id: number) => {
  return useApi<any>(`/projects/${id}`);
};

// Hook for fetching all projects
export const useProjects = (params?: { 
  skip?: number; 
  limit?: number; 
  is_public?: boolean; 
  category?: string 
}) => {
  const queryParams = new URLSearchParams();
  if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
  if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
  if (params?.is_public !== undefined) queryParams.append('is_public', params.is_public.toString());
  if (params?.category) queryParams.append('category', params.category);
  
  return useApi<any>(`/projects/?${queryParams.toString()}`);
};

// Hook for fetching a module by ID
export const useModule = (id: number) => {
  return useApi<any>(`/modules/${id}`);
};

// Hook for fetching all modules
export const useModules = (params?: { 
  skip?: number; 
  limit?: number; 
  project_id?: number; 
  status?: string; 
  difficulty?: string 
}) => {
  const queryParams = new URLSearchParams();
  if (params?.skip !== undefined) queryParams.append('skip', params.skip.toString());
  if (params?.limit !== undefined) queryParams.append('limit', params.limit.toString());
  if (params?.project_id !== undefined) queryParams.append('project_id', params.project_id.toString());
  if (params?.status) queryParams.append('status', params.status);
  if (params?.difficulty) queryParams.append('difficulty', params.difficulty);
  
  return useApi<any>(`/modules/?${queryParams.toString()}`);
};