import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue'
import path from 'path';

// https://vitejs.dev/config
export default defineConfig({
  base: `/src/`,
  resolve: {
    // Some libs that can run in both Web and Node.js, such as `axios`, we need to tell Vite to build them in Node.js.
    browserField: false,
    mainFields: ['module', 'jsnext:main', 'jsnext'],
    alias: {
      '@': path.resolve(__dirname, 'src'),
    }
  },
  plugins: [vue()],
  build: {
    sourcemap: true,
  },
});

