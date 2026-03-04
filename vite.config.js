import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5039,
    proxy: {
      '/api': {
        target: 'http://localhost:5031',
        changeOrigin: true
      }
    }
  }
})