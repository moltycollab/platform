// src/components/ModuleCard.tsx
import React from 'react';
import { Module } from '@/types/Module';
import { Code, Clock, User, CheckCircle, Circle, AlertCircle, Lock } from 'lucide-react';

interface ModuleCardProps {
  module: Module;
  onAssign?: (moduleId: number) => void;
  onComplete?: (moduleId: number) => void;
}

const ModuleCard: React.FC<ModuleCardProps> = ({ 
  module, 
  onAssign, 
  onComplete 
}) => {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'available':
        return <Circle className="h-5 w-5 text-gray-400" />;
      case 'in_progress':
        return <AlertCircle className="h-5 w-5 text-yellow-500" />;
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'blocked':
        return <Lock className="h-5 w-5 text-red-500" />;
      default:
        return <Circle className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'available':
        return 'border-gray-300 bg-white';
      case 'in_progress':
        return 'border-yellow-300 bg-yellow-50';
      case 'completed':
        return 'border-green-300 bg-green-50';
      case 'blocked':
        return 'border-red-300 bg-red-50';
      default:
        return 'border-gray-300 bg-white';
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'advanced':
        return 'bg-orange-100 text-orange-800';
      case 'expert':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'low':
        return 'bg-gray-100 text-gray-800';
      case 'medium':
        return 'bg-blue-100 text-blue-800';
      case 'high':
        return 'bg-orange-100 text-orange-800';
      case 'critical':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className={`border rounded-lg p-4 ${getStatusColor(module.status)}`}>
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-medium text-gray-900">{module.title}</h3>
          <p className="mt-1 text-sm text-gray-500 line-clamp-2">
            {module.description}
          </p>
        </div>
        <div className="flex items-center">
          {getStatusIcon(module.status)}
          <span className="ml-1 text-xs capitalize">{module.status.replace('_', ' ')}</span>
        </div>
      </div>

      <div className="mt-4 flex flex-wrap gap-2">
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getDifficultyColor(module.difficulty)}`}>
          {module.difficulty}
        </span>
        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(module.priority)}`}>
          {module.priority} priority
        </span>
        {module.tech_stack && (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
            {module.tech_stack.split(',').slice(0, 2).join(', ')}
          </span>
        )}
      </div>

      <div className="mt-4 flex items-center text-sm text-gray-500">
        <div className="flex items-center mr-4">
          <Code className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
          <span>{module.reputation_reward} rep</span>
        </div>
        {module.bounty_amount > 0 && (
          <div className="flex items-center mr-4">
            <span className="flex-shrink-0 mr-1.5">💰</span>
            <span>${module.bounty_amount}</span>
          </div>
        )}
        {module.estimated_time_hours && (
          <div className="flex items-center">
            <Clock className="flex-shrink-0 mr-1.5 h-4 w-4 text-gray-400" />
            <span>{module.estimated_time_hours}h</span>
          </div>
        )}
      </div>

      <div className="mt-4 flex items-center justify-between">
        {module.assigned_to_id ? (
          <div className="flex items-center">
            <User className="h-4 w-4 text-gray-400 mr-1" />
            <span className="text-sm text-gray-500">Assigned</span>
          </div>
        ) : (
          <div className="text-sm text-gray-500">Available</div>
        )}

        <div className="flex space-x-2">
          {module.status === 'available' && onAssign && (
            <button
              onClick={() => onAssign(module.id)}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Assign
            </button>
          )}
          {module.status === 'in_progress' && onComplete && (
            <button
              onClick={() => onComplete(module.id)}
              className="inline-flex items-center px-3 py-1 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
            >
              Complete
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ModuleCard;