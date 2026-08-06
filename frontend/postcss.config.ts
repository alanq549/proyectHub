/**
 * postcss.config.ts — ProjectHub
 * Pipeline mínimo: Tailwind → Autoprefixer.
 *
 * NOTA: Vite trae incluido lightningcss por defecto. Este postcss.config
 * es explícito porque Tailwind + plugins (forms/typography) requieren
 * el pipeline PostCSS standard.
 */
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
