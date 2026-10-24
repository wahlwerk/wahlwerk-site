import App from './App.svelte';
import 'katex/dist/katex.min.css';
import './app.css';
import { installTokens } from './lib/tokens';

// Design tokens become CSS custom properties on :root before anything
// renders, so every component can style itself with var(--...).
installTokens();

const app = new App({ target: document.getElementById('app')! });

export default app;
