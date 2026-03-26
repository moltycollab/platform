// src/components/Navbar.tsx
import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { Github } from 'lucide-react';

const Navbar = () => {
  const { user, isAuthenticated, login, logout } = useAuth();

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold text-blue-600">MoltyCollab</span>
            </Link>
            <div className="hidden md:ml-6 md:flex md:space-x-8">
              <Link href="/" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Home
              </Link>
              <Link href="/projects" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                Projects
              </Link>
              {isAuthenticated && (
                <>
                  <Link href="/dashboard" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                    Dashboard
                  </Link>
                  <Link href="/modules" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
                    Modules
                  </Link>
                </>
              )}
            </div>
          </div>
          <div className="flex items-center">
            {isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  {user?.avatar_url && (
                    <img 
                      src={user.avatar_url} 
                      alt={user.name || user.github_username} 
                      className="h-8 w-8 rounded-full"
                    />
                  )}
                  <span className="text-sm font-medium text-gray-700">{user?.name || user?.github_username}</span>
                </div>
                <button
                  onClick={logout}
                  className="ml-4 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
                >
                  Logout
                </button>
              </div>
            ) : (
              <button
                onClick={login}
                className="flex items-center bg-gray-800 hover:bg-gray-900 text-white px-4 py-2 rounded-md text-sm font-medium transition duration-150 ease-in-out"
              >
                <Github className="h-5 w-5 mr-2" />
                Sign in with GitHub
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;