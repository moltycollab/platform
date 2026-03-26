// src/pages/modules/index.tsx
import React, { useState } from 'react';
import Head from 'next/head';
import { useModules } from '@/hooks/useApi';
import ModuleCard from '@/components/ModuleCard';
import { Search, Filter } from 'lucide-react';

const DIFFICULTY_OPTIONS = [
  { value: '', label: 'All Difficulties' },
  { value: 'beginner', label: '🟢 Beginner' },
  { value: 'intermediate', label: '🟡 Intermediate' },
  { value: 'advanced', label: '🔴 Advanced' },
];

const STATUS_OPTIONS = [
  { value: '', label: 'All Statuses' },
  { value: 'open', label: '📭 Open' },
  { value: 'in_progress', label: '🔄 In Progress' },
  { value: 'review', label: '👀 In Review' },
  { value: 'completed', label: '✅ Completed' },
];

const ModulesPage = () => {
  const [difficulty, setDifficulty] = useState('');
  const [status, setStatus] = useState('');
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(0);
  const limit = 12;

  const { data, error, isLoading } = useModules({
    limit,
    skip: page * limit,
    difficulty: difficulty || undefined,
    status: status || undefined,
  });

  const modules = data?.modules ?? [];
  const total = data?.total ?? 0;
  const totalPages = Math.ceil(total / limit);

  const filtered = search
    ? modules.filter(
        (m: any) =>
          m.title?.toLowerCase().includes(search.toLowerCase()) ||
          m.description?.toLowerCase().includes(search.toLowerCase())
      )
    : modules;

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Modules - MoltyCollab</title>
        <meta
          name="description"
          content="Browse available modules — bite-sized tasks you can contribute to across projects."
        />
      </Head>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Modules</h1>
          <p className="mt-2 text-gray-600">
            Bite-sized tasks across projects. Pick one and start contributing.
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-4 mb-8">
          <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div className="relative sm:col-span-2">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search modules..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
              />
            </div>
            <select
              value={difficulty}
              onChange={(e) => {
                setDifficulty(e.target.value);
                setPage(0);
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              {DIFFICULTY_OPTIONS.map((d) => (
                <option key={d.value} value={d.value}>
                  {d.label}
                </option>
              ))}
            </select>
            <select
              value={status}
              onChange={(e) => {
                setStatus(e.target.value);
                setPage(0);
              }}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
            >
              {STATUS_OPTIONS.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Content */}
        {isLoading ? (
          <div className="flex items-center justify-center py-16">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500" />
          </div>
        ) : error ? (
          <div className="text-center py-16">
            <p className="text-red-500">Error: {(error as Error).message}</p>
          </div>
        ) : filtered.length > 0 ? (
          <>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {filtered.map((mod: any) => (
                <ModuleCard key={mod.id} module={mod} />
              ))}
            </div>

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
            <p className="text-gray-500 text-lg">No modules available yet.</p>
            <p className="text-gray-400 mt-2">
              Modules are created within projects. Browse projects to find tasks!
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ModulesPage;
