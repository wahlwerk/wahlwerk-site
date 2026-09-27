import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

export default defineConfig(({ command }) => ({
  plugins: [svelte()],
  base: './',
  // In dev, serve docs/ at root so fetch('data/elections.json') resolves.
  // In build, publicDir is disabled so docs/ is not copied into itself.
  publicDir: command === 'serve' ? '../docs' : false,
  build: {
    outDir: '../docs',
    emptyOutDir: false, // keep docs/data/, which build.py writes
  },
}));
