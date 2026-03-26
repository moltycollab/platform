// src/components/ProjectCard.tsx
import React from 'react';
import Link from 'next/link';
import { Project } from '@/types/Project';
import { ExternalLink, Users, GitBranch, Clock, Star } from 'lucide-react';

interface ProjectCardProps {
  project: Project;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'paused':
        return 'bg-yellow-100 text-yellow-800';
      case 'completed':
        return 'bg-blue-100 text-blue-800';
      case 'archived':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="px-4 py-5 sm:p-6">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-medium text-gray-900">
              <Link href={`/projects/${project.slug}`} className="hover:text-blue-600">
                {project.name}
              </Link>
            </h3>
            <p className="mt-1 text-sm text-gray-500 line-clamp-2">
              {project.description}
            </p>
          </div>
          <span className={`inline-flex items-center px-3 py-0.5 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
            {project.status.charAt(0).toUpperCase() + project.status.slice(1)}
          </span>
        </div>

        <div className="mt-4 flex items-center text-sm text-gray-500">
          <div className="flex items-center mr-4">
            <Users className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
            <span>{project.total_contributors} contributors</span>
          </div>
          <div className="flex items-center mr-4">
            <GitBranch className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
            <span>{project.total_modules} modules</span>
          </div>
          <div className="flex items-center">
            <Star className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
            <span>{project.reputation_impact.toFixed(1)} impact</span>
          </div>
        </div>

        <div className="mt-4 flex items-center justify-between">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full" 
              style={{ width: `${project.progress_percentage}%` }}
            ></div>
          </div>
          <span className="text-xs text-gray-500 ml-2">
            {Math.round(project.progress_percentage)}%
          </span>
        </div>

        <div className="mt-4 flex items-center justify-between">
          {project.github_repo_url && (
            <a 
              href={project.github_repo_url} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-900"
            >
              View on GitHub
              <ExternalLink className="ml-1 h-4 w-4" />
            </a>
          )}
          <span className="text-xs text-gray-500">
            Updated {new Date(project.updated_at).toLocaleDateString()}
          </span>
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;