/**
 * tailwind.config.ts — ProjectHub
 * Migración Bootstrap 5.3 → Tailwind v3.4 (Dual-Style Seguro)
 *
 * Reglas activas (ver frontend/documentation/Migracion_Bootstrap_Tailwind_v1.0.md):
 *  • prefix: 'tw-' — evita colisiones con clases Bootstrap durante transición.
 *  • corePlugins.preflight = false — NO sobrescribir reset de Bootstrap.
 *    Se activará en Bloque 7 (Purga Final Bootstrap).
 *  • theme.extend mapea tokens --app-* del main.css unificado.
 *    Los colores SIEMPRE pasan por var(--app-*, fallback) para que un cambio
 *    en main.css se refleje también en Tailwind (single source of truth).
 *  • @tailwindcss/forms strategy:'class' → genera .tw-form-input / .tw-form-select
 *    sin sobrescribir .form-control de Bootstrap.
 *  • @tailwindcss/typography → clase .tw-prose para documentos.
 */
import type { Config } from 'tailwindcss'
import forms from '@tailwindcss/forms'
import typography from '@tailwindcss/typography'

export default {
  // Prefijo obligatorio durante la fase de transición dual con Bootstrap 5.3
  prefix: 'tw-',

  corePlugins: {
    // Desactivado para evitar romper los estilos globales y reseteos de Bootstrap
    preflight: false,
  },
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      /* ================================================================
         COLORS — binding 1:1 con tokens --app-* (main.css Bloque 1/4)
         Uso en componentes: class="tw-bg-primary tw-text-on-surface"
         ================================================================ */
      colors: {
        'primary': {
          DEFAULT: 'var(--app-primary, #0f172a)',
          dark:    'var(--app-primary-dark, #000000)',
          light:   'var(--app-primary-light, #334155)',
        },
        'secondary': {
          DEFAULT: 'var(--app-secondary, #475569)',
          light:   'var(--app-secondary-light, #f1f5f9)',
        },
        'slate': {
          '50':  'var(--app-slate-50,   #f8fafc)',
          '100': 'var(--app-slate-100,  #f1f5f9)',
          '200': 'var(--app-slate-200,  #e2e8f0)',
          '300': 'var(--app-slate-300,  #cbd5e1)',
          '400': 'var(--app-slate-400,  #94a3b8)',
          '500': 'var(--app-slate-500,  #64748b)',
          '600': 'var(--app-slate-600,  #475569)',
          '700': 'var(--app-slate-700,  #334155)',
          '800': 'var(--app-slate-800,  #1e293b)',
          '900': 'var(--app-slate-900,  #0f172a)',
        },
        'black':               'var(--app-black, #000000)',
        'on-primary':          'var(--app-on-primary, #ffffff)',
        'on-surface':          'var(--app-on-surface, #0f172a)',
        'on-surface-variant': 'var(--app-on-surface-variant, #475569)',
        'outline':            'var(--app-outline, #76777d)',
        'outline-variant':    'var(--app-outline-variant, #c6c6cd)',
        'error':               'var(--app-error,   #ba1a1a)',
        'error-bg':            'var(--app-error-bg, rgba(254, 226, 226, 0.8))',
        'success':             'var(--app-success, #15803d)',
        'success-bg':          'var(--app-success-bg, rgba(220, 252, 231, 0.8))',
        'warning':             'var(--app-warning, #b45309)',
        'warning-bg':          'var(--app-warning-bg, rgba(254, 243, 199, 0.8))',
        /* Surface containers — Material Design mapping */
        'surface-container-lowest':  'var(--app-surface-container-lowest,  #ffffff)',
        'surface-container-low':     'var(--app-surface-container-low,     #f2f4f6)',
        'surface-container':         'var(--app-surface-container,         #e8eaed)',
        'surface-container-high':    'var(--app-surface-container-high,    #dcdfe2)',
        'surface-container-highest': 'var(--app-surface-container-highest, #d0d3d6)',
      },

      /* ================================================================
         BORDER RADIUS — tokens glassmorphism unificados
         ================================================================ */
      borderRadius: {
        'pill':      'var(--app-radius-pill,       9999px)',
        'glass-sm':  'var(--app-glass-radius-sm,   0.75rem)',
        'glass-md':  'var(--app-glass-radius-md,   1.1rem)',
        'glass-lg':  'var(--app-glass-radius-lg,   1.25rem)',
        'glass-xl':  'var(--app-glass-radius-xl,   1.5rem)',
        'hero':      'var(--app-hero-radius,       1.75rem)',
        'topbar':    'var(--app-topbar-radius,     1rem)',
        'rail':      'var(--app-rail-radius,       1.25rem)',
        'bottomnav': 'var(--app-bottomnav-radius,  1.5rem)',
        'input':     'var(--app-input-radius,      0.5rem)',
      },

      /* ================================================================
         BOX SHADOW — tokens glassmorphism + elevación
         ================================================================ */
      boxShadow: {
        'glass':            'var(--app-glass-shadow,            0 10px 30px -5px rgba(0,0,0,0.04))',
        'glass-hover':      'var(--app-glass-shadow-hover,      0 20px 40px -10px rgba(0,0,0,0.08))',
        'kpi':              'var(--app-kpi-shadow,              0 15px 30px -10px rgba(15,23,42,0.08))',
        'kpi-hover':        'var(--app-kpi-shadow-hover,        0 25px 45px -10px rgba(15,23,42,0.18))',
        'topbar':           'var(--app-topbar-shadow,           0 4px 15px rgba(0,0,0,0.06))',
        'rail':             'var(--app-rail-shadow,             4px 0 20px rgba(0,0,0,0.06))',
        'bottomnav':        'var(--app-bottomnav-shadow,        0 -4px 20px rgba(0,0,0,0.08))',
        'btn-primary':      'var(--app-btn-primary-shadow,      0 10px 20px -8px rgba(15,23,42,0.45))',
        'btn-primary-hover':'var(--app-btn-primary-shadow-hover,0 14px 26px -8px rgba(15,23,42,0.60))',
        'btn-secondary':    'var(--app-btn-secondary-shadow,    0 10px 20px -8px rgba(75,65,225,0.25))',
        'card-flat':        'var(--app-flat-shadow,             0 1px 3px 0 rgba(0,0,0,0.08), 0 1px 2px -1px rgba(0,0,0,0.06))',
      },

      /* ================================================================
         BACKDROP BLUR — tokens glass
         ================================================================ */
      backdropBlur: {
        'glass':    'var(--app-glass-blur,    16px)',
        'glass-sm': 'var(--app-glass-blur-sm, 12px)',
        'topbar':   'var(--app-topbar-blur,   20px)',
        'rail':     'var(--app-rail-blur,     0px)',
        'bottomnav':'var(--app-bottomnav-blur,12px)',
      },

      /* ================================================================
         FONTS — tipografía global
         ================================================================ */
      fontFamily: {
        sans: [
          'var(--app-font-family, "Inter", system-ui, -apple-system, sans-serif)',
          { fontFeatureSettings: '"cv02", "cv03", "cv04", "cv11"' },
        ],
      },
      fontSize: {
        'hero-title':   ['var(--app-hero-title-size, 3rem)',     { lineHeight: 'var(--app-hero-title-line-height, 1.05)', fontWeight: '900' }],
        'hero-sub':     ['var(--app-hero-sub-size, 1.05rem)',    { lineHeight: 'var(--app-hero-sub-line-height, 1.55)' }],
        'section-title':['var(--app-section-title-size, 1.65rem)',{ lineHeight: '1.3', fontWeight: '800' }],
      },

      /* ================================================================
         BREAKPOINTS — alineados a Bootstrap 5.3 para mantener
         responsive idéntico post-migración
         ================================================================ */
      screens: {
        'sm':   '576px',   /* == Bootstrap .sm  → breakpoint-sm   */
        'md':   '768px',   /* == Bootstrap .md  → breakpoint-md   */
        'lg':   '992px',   /* == Bootstrap .lg  → breakpoint-lg   */
        'xl':   '1200px',  /* == Bootstrap .xl  → breakpoint-xl   */
        '2xl':  '1400px',  /* == Bootstrap .xxl → breakpoint-xxl  */
      },
    },
  },
  plugins: [
    forms({ strategy: 'class' }),
    typography(),
  ],
} satisfies Config
