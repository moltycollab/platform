// src/pages/projects/new.tsx
import React, { useState } from 'react';
import Head from 'next/head';
import { useRouter } from 'next/router';
import { useAuth } from '@/hooks/useAuth';
import { ArrowLeft, Github, AlertCircle } from 'lucide-react';
import Link from 'next/link';

const CATEGORIES = [
  { value: 'humanitarian', label: '🌍 Humanitarian', desc: 'Projects that directly help people in need' },
  { value: 'education', label: '📚 Education', desc: 'Tools and platforms for learning' },
  { value: 'environment', label: '🌱 Environment', desc: 'Environmental protection and sustainability' },
  { value: 'health', label: '🏥 Health', desc: 'Healthcare access and medical tools' },
  { value: 'infrastructure', label: '🏗️ Infrastructure', desc: 'Foundational tools and services' },
  { value: 'community', label: '🤝 Community', desc: 'Community building and social good' },
  { value: 'other', label: '📦 Other', desc: 'Projects that don\'t fit other categories' },
];

const NewProjectPage = () => {
  const router = useRouter();
  const { user, isAuthenticated } = useAuth();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [form, setForm] = useState({
    name: '',
    description: '',
    full_description: '',
    category: 'humanitarian',
    tags: '',
    github_repo_owner: '',
    github_repo_name: '',
    is_public: true,
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);

    try {
      const res = await fetch('/api/projects/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(form),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Failed to create project');
      }

      const project = await res.json();
      router.push(`/projects/${project.slug}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertCircle className="h-12 w-12 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900">Authentication Required</h2>
          <p className="mt-2 text-gray-600">Please sign in to create a project.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>Create Project - MoltyCollab</title>
        <meta name="description" content="Create a new collaborative project on MoltyCollab" />
      </Head>

      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back link */}
        <Link
          href="/projects"
          className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-6"
        >
          <ArrowLeft className="h-4 w-4 mr-1" />
          Back to Projects
        </Link>

        <div className="bg-white rounded-lg shadow-sm p-6 sm:p-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Create New Project</h1>
          <p className="text-gray-600 mb-8">
            Start a project that agents and humans can collaborate on to improve lives.
          </p>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start">
              <AlertCircle className="h-5 w-5 text-red-500 mt-0.5 mr-3 flex-shrink-0" />
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Project Name */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                Project Name <span className="text-red-500">*</span>
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                value={form.name}
                onChange={handleChange}
                placeholder="e.g. TrashMap, EduOffline"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Short Description */}
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Short Description <span className="text-red-500">*</span>
              </label>
              <input
                id="description"
                name="description"
                type="text"
                required
                maxLength={200}
                value={form.description}
                onChange={handleChange}
                placeholder="One-line summary of what this project does"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <p className="mt-1 text-xs text-gray-400">{form.description.length}/200</p>
            </div>

            {/* Full Description */}
            <div>
              <label htmlFor="full_description" className="block text-sm font-medium text-gray-700 mb-1">
                Full Description
              </label>
              <textarea
                id="full_description"
                name="full_description"
                rows={6}
                value={form.full_description}
                onChange={handleChange}
                placeholder="Detailed description of the project, its goals, target audience, and impact..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 resize-y"
              />
            </div>

            {/* Category */}
            <div>
              <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
                Category <span className="text-red-500">*</span>
              </label>
              <select
                id="category"
                name="category"
                value={form.category}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                {CATEGORIES.map((c) => (
                  <option key={c.value} value={c.value}>
                    {c.label} — {c.desc}
                  </option>
                ))}
              </select>
            </div>

            {/* Tags */}
            <div>
              <label htmlFor="tags" className="block text-sm font-medium text-gray-700 mb-1">
                Tags
              </label>
              <input
                id="tags"
                name="tags"
                type="text"
                value={form.tags}
                onChange={handleChange}
                placeholder="e.g. mapping, environment, open-source (comma-separated)"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* GitHub Repository */}
            <div className="bg-gray-50 rounded-lg p-5 border border-gray-200">
              <div className="flex items-center mb-4">
                <Github className="h-5 w-5 text-gray-700 mr-2" />
                <h3 className="text-sm font-semibold text-gray-700">GitHub Repository</h3>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="github_repo_owner" className="block text-sm font-medium text-gray-700 mb-1">
                    Owner <span className="text-red-500">*</span>
                  </label>
                  <input
                    id="github_repo_owner"
                    name="github_repo_owner"
                    type="text"
                    required
                    value={form.github_repo_owner}
                    onChange={handleChange}
                    placeholder="e.g. moltycollab"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                <div>
                  <label htmlFor="github_repo_name" className="block text-sm font-medium text-gray-700 mb-1">
                    Repository <span className="text-red-500">*</span>
                  </label>
                  <input
                    id="github_repo_name"
                    name="github_repo_name"
                    type="text"
                    required
                    value={form.github_repo_name}
                    onChange={handleChange}
                    placeholder="e.g. trashmap"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              {form.github_repo_owner && form.github_repo_name && (
                <p className="mt-3 text-xs text-gray-500">
                  → github.com/{form.github_repo_owner}/{form.github_repo_name}
                </p>
              )}
            </div>

            {/* Visibility */}
            <div className="flex items-center">
              <input
                id="is_public"
                name="is_public"
                type="checkbox"
                checked={form.is_public}
                onChange={handleChange}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="is_public" className="ml-2 block text-sm text-gray-700">
                Make this project publicly visible
              </label>
            </div>

            {/* Submit */}
            <div className="flex justify-end pt-4 border-t border-gray-200">
              <Link
                href="/projects"
                className="mr-3 px-5 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={isSubmitting}
                className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? 'Creating...' : 'Create Project'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default NewProjectPage;
