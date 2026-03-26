// src/services/moduleService.ts
import apiClient from './apiClient';
import { Module, CreateModuleDto } from '@/types/Module';

export const moduleService = {
  // Get all modules
  async getAllModules(params?: {
    skip?: number;
    limit?: number;
    project_id?: number;
    status?: string;
    difficulty?: string;
  }): Promise<{ modules: Module[]; total: number }> {
    const response = await apiClient.get('/modules/', { params });
    return response.data;
  },

  // Get module by ID
  async getModuleById(id: number): Promise<Module> {
    const response = await apiClient.get(`/modules/${id}`);
    return response.data;
  },

  // Get module by slug
  async getModuleBySlug(slug: string): Promise<Module> {
    const response = await apiClient.get(`/modules/slug/${slug}`);
    return response.data;
  },

  // Create a new module
  async createModule(moduleData: CreateModuleDto): Promise<Module> {
    const response = await apiClient.post('/modules/', moduleData);
    return response.data;
  },

  // Update a module
  async updateModule(id: number, moduleData: Partial<Module>): Promise<Module> {
    const response = await apiClient.put(`/modules/${id}`, moduleData);
    return response.data;
  },

  // Delete a module
  async deleteModule(id: number): Promise<void> {
    await apiClient.delete(`/modules/${id}`);
  },

  // Assign a module to a user
  async assignModule(moduleId: number, userId: number): Promise<Module> {
    const response = await apiClient.post(`/modules/${moduleId}/assign?user_id=${userId}`);
    return response.data;
  },

  // Complete a module
  async completeModule(moduleId: number): Promise<Module> {
    const response = await apiClient.post(`/modules/${moduleId}/complete`);
    return response.data;
  }
};