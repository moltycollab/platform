// src/components/UserAvatar.tsx
import React from 'react';
import { User as UserType } from '@/types/User';

interface UserAvatarProps {
  user: UserType;
  size?: 'sm' | 'md' | 'lg';
  showName?: boolean;
}

const UserAvatar: React.FC<UserAvatarProps> = ({ 
  user, 
  size = 'md', 
  showName = true 
}) => {
  const sizeClasses = {
    sm: 'h-8 w-8 text-xs',
    md: 'h-10 w-10 text-sm',
    lg: 'h-12 w-12 text-base'
  };

  const initials = user.name 
    ? user.name.charAt(0).toUpperCase() 
    : user.github_username.charAt(0).toUpperCase();

  return (
    <div className="flex items-center">
      {user.avatar_url ? (
        <img
          src={user.avatar_url}
          alt={user.name || user.github_username}
          className={`${sizeClasses[size]} rounded-full object-cover`}
        />
      ) : (
        <div className={`${sizeClasses[size]} rounded-full bg-blue-500 flex items-center justify-center text-white font-medium`}>
          {initials}
        </div>
      )}
      {showName && (
        <span className="ml-2 text-gray-700">
          {user.name || user.github_username}
        </span>
      )}
    </div>
  );
};

export default UserAvatar;