// src/services/projectService.ts
import apiClient from './apiClient';
import { Project, CreateProjectDto } from '@/types/Project';

export const projectService = {
  // Get all projects
  async getAllProjects(params?: {
    skip?: number;
    limit?: number;
    is_public?: boolean;
    category?: string;
  }): Promise<{ projects: Project[]; total: number }> {
    const response = await apiClient.get('/projects/', { params });
    return response.data;
  },

  // Get project by ID
  async getProjectById(id: number): Promise<Project> {
    const response = await apiClient.get(`/projects/${id}`);
    return response.data;
  },

  // Get project by slug
  async getProjectBySlug(slug: string): Promise<Project> {
    const response = await apiClient.get(`/projects/slug/${slug}`);
    return response.data;
  },

  // Create a new project
  async createProject(projectData: CreateProjectDto): Promise<Project> {
    const response = await apiClient.post('/projects/', projectData);
    return response.data;
  },

  // Update a project
  async updateProject(id: number, projectData: Partial<Project>): Promise<Project> {
    const response = await apiClient.put(`/projects/${id}`, projectData);
    return response.data;
  },

  // Delete a project
  async deleteProject(id: number): Promise<void> {
    await apiClient.delete(`/projects/${id}`);
  }
};