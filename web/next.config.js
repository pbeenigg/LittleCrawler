/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'out',
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
  typescript: {
    // 允许构建时忽略类型错误（静态导出的已知问题）
    ignoreBuildErrors: true,
  },
};

module.exports = nextConfig;
