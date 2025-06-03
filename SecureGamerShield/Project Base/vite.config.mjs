// vite.config.mjs
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react' // nếu bạn dùng React

export default defineConfig({
  plugins: [
    react(),     // hoặc plugin bạn đang dùng
    tailwindcss()
  ]
})
