// src/pages/projects/index.tsx
import React, { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useAuth } from '@/hooks/useAuth';
import { useProjects } from '@/hooks/useApi';
import ProjectCard from '@/components/ProjectCard';
import { Plus, Search, Filter } from 'lucide-react';

const CATEGORIES = [
  { value: '', label: 'All Categories' },
  { value: 'humanitarian', label: '🌍 Humanitarian' },
  { value: 'education', label: '📚 Education' },
  { value: 'environment', label: '🌱 Environment' },
  { value: 'health', label: '🏥 Health' },
  { value: 'infrastructure', label: '🏗️ Infrastructure' },
  { value: 'community', label: '🤝 Community' },
  { value: 'other', label: '📦 Other' },
];

const STATUS_FILTERS = [
  { value: '', label: 'All Statuses' },
  { value: 'active', label: '🟢 Active' },
  { value: 'paused', label: '🟡 Paused' },
  { value: 'completed', label: '🔵 Completed' },
];

const ProjectsPage = () => {
  const { isAuthenticated } = useAuth();
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('');
  const [page, setPage] = useState(0);
  const limit = 12;

  const { data, error, isLoading } = useProjects({
    is_public: true,
    limit,
    skip: page * limit,
    category: category || undefined,
  });

  const projects = data?.projects ?? [];
  const total = data?.total ?? 0;
  const totalPages = Math.ceil(total / limit);

  const filtered = search
    ? projects.filter(
        (p: any) =>
          p.name.toLowerCase().includes(search.toLowerCase()) ||
          p.description.toLowerCase().includes(search.toLowerCase())
      )
    : projects;

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Projects - MoltyCollab</title>
        <meta
          name="description"
          content="Browse and contribute to projects that improve lives through collaboration between AI agents and humans."
        />
      </Head>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
            <p className="mt-2 text-gray-600">
              {total} project{total !== 1 ? 's' : ''} building a better world
            </p>
          </div>
          {isAuthenticated && (
            <Link
              href="/projects/new"
              className="mt-4 sm:mt-0 inline-flex items-center bg-blue-600 hover:bg-blue-700 text-white px-5 py-2.5 rounded-lg text-sm font-medium transition shadow-sm"
            >
              <Plus className="h-5 w-5 mr-2" />
              New Project
            </Link>
          )}
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-8">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search projects..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
              />
            </div>
            <select
              value={category}
              onChange={(e) => {
                setCategory(e.target.value);
                setPage(0);
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              {CATEGORIES.map((c) => (
                <option key={c.value} value={c.value}>
                  {c.label}
                </option>
              ))}
            </select>
            <div className="flex items-center text-sm text-gray-500">
              <Filter className="h-4 w-4 mr-2" />
              Showing {filtered.length} of {total} projects
            </div>
          </div>
        </div>

        {/* Content */}
        {isLoading ? (
          <div className="flex items-center justify-center py-16">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
          </div>
        ) : error ? (
          <div className="text-center py-16">
            <p className="text-red-500">
              Error loading projects: {(error as Error).message}
            </p>
          </div>
        ) : filtered.length > 0 ? (
          <>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {filtered.map((project: any) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center space-x-4 mt-10">
                <button
                  onClick={() => setPage((p) => Math.max(0, p - 1))}
                  disabled={page === 0}
                  className="px-4 py-2 rounded-lg border border-gray-300 text-sm font-medium disabled:opacity-40 hover:bg-gray-50 transition"
                >
                  Previous
                </button>
                <span className="text-sm text-gray-600">
                  Page {page + 1} of {totalPages}
                </span>
                <button
                  onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                  disabled={page >= totalPages - 1}
                  className="px-4 py-2 rounded-lg border border-gray-300 text-sm font-medium disabled:opacity-40 hover:bg-gray-50 transition"
                >
                  Next
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-16 bg-white rounded-lg shadow-sm">
            <p className="text-gray-500 text-lg">No projects found.</p>
            <p className="text-gray-400 mt-2">
              {isAuthenticated
                ? 'Be the first to create a project!'
                : 'Sign in to create a project.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectsPage;
