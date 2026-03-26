// src/types/User.ts
export interface User {
  id: number;
  github_id: string;
  github_username: string;
  email?: string;
  name?: string;
  avatar_url?: string;
  bio?: string;
  location?: string;
  company?: string;
  is_agent: boolean;
  agent_description?: string;
  expertise_areas?: string;
  reputation_score: number;
  total_contributions: number;
  completed_modules: number;
  is_active: boolean;
  is_verified: boolean;
  created_at: string;
  updated_at?: string;
}