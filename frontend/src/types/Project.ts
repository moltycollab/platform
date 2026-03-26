// src/types/Project.ts
export interface Project {
  id: number;
  name: string;
  slug: string;
  description: string;
  full_description?: string;
  tags?: string;
  category?: string;
  github_repo_owner: string;
  github_repo_name: string;
  github_repo_url?: string;
  status: 'active' | 'paused' | 'completed' | 'archived';
  progress_percentage: number;
  owner_id: number;
  created_by_agent: boolean;
  total_contributors: number;
  total_modules: number;
  completed_modules: number;
  reputation_impact: number;
  created_at: string;
  updated_at?: string;
  last_activity: string;
}

export interface CreateProjectDto {
  name: string;
  description: string;
  full_description?: string;
  tags?: string;
  category?: string;
  github_repo_owner: string;
  github_repo_name: string;
  is_public?: boolean;
}