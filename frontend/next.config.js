/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    typedRoutes: true,
  },
  env: {
    BACKEND_API_URL: process.env.BACKEND_API_URL || 'http://localhost:8000',
  },
  async redirects() {
    return [
      {
        source: '/dashboard',
        destination: '/auth/login',
        permanent: false,
        missing: [
          {
            type: 'cookie',
            key: 'access_token',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig