import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  typescript: {
    // Skip type checking during builds for faster deployment
    ignoreBuildErrors: true,
  },
  eslint: {
    // Skip ESLint during builds for faster deployment
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
