// src/types/Module.ts
export interface Module {
  id: number;
  project_id: number;
  title: string;
  slug: string;
  description: string;
  detailed_specification?: string;
  tech_stack?: string;
  difficulty: 'beginner' | 'medium' | 'advanced' | 'expert';
  estimated_time_hours?: number;
  status: 'available' | 'in_progress' | 'completed' | 'blocked';
  progress_percentage: number;
  priority: 'low' | 'medium' | 'high' | 'critical';
  assigned_to_id?: number;
  started_at?: string;
  completed_at?: string;
  created_by: number;
  reputation_reward: number;
  bounty_amount: number;
  created_at: string;
  updated_at?: string;
}

export interface CreateModuleDto {
  project_id: number;
  title: string;
  description: string;
  detailed_specification?: string;
  tech_stack?: string;
  difficulty?: 'beginner' | 'medium' | 'advanced' | 'expert';
  estimated_time_hours?: number;
  priority?: 'low' | 'medium' | 'high' | 'critical';
  reputation_reward?: number;
  bounty_amount?: number;
}