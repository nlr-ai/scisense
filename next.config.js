/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
  // If you're deploying to a specific path (not root)
  // basePath: '/your-base-path',
};

module.exports = nextConfig;
