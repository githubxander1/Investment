// vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  base: '/public/', // 设置静态文件的基础路径
  build: {
    outDir: 'dist',
  },
  plugins: [vue()],
  server: {
    open: true,
//    origin: 'http://localhost',
//    hmr: { overlay: false },
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
    },
  },
});