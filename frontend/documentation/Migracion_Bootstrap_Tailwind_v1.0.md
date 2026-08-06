# Plan de Migración: Bootstrap 5.3 → Tailwind CSS v3
**Versión del Plan**: 1.0 (2026-08-05)
**Arquitecto Responsable**: Arquitecto Senior / Agente TRAE
**Proyecto**: ProjectHub (Vue 3 + TypeScript + Vite + Pinia)
**Estado**: Plan aprobado — Ejecución por Bloques.

---

## 0. Resumen Ejecutivo

| Aspecto | Valor actual | Post-Migración |
|---|---|---|
| Motor de estilos principal | Bootstrap 5.3 (CSS + JS Bundle) | Tailwind CSS v3 (utility-first) |
| Prefijo Tailwind | — | `tw-` (evita colisiones mientras Bootstrap esté activo) |
| Tailwind Preflight | — | **DESACTIVADO** temporalmente. Se activa en Bloque 7 cuando se elimine Bootstrap. |
| Plugins Tailwind | — | `@tailwindcss/forms` (estilos inputs), `@tailwindcss/typography` (`.prose` para documentos) |
| Sistema de tokens | CSS Variables `--app-*` en `main.css` | `tailwind.config.ts → theme.extend` — doble binding temporal con CSS vars. |
| Bootstrap JS | Cargado globalmente `main.ts:7` | **Activo durante migración**. Dropdowns se reemplazan en Bloque 5 por implementación Vue nativa. |
| Estrategia de transición | — | **Dual-Style Seguro**: Bootstrap + Tailwind coexisten en cada componente. Bootstrap se purga al final de cada bloque. |

---

## 1. Hallazgos de Auditoría (Fase de Descubrimiento)

### 1.1 Footprint Actual de Bootstrap

| Métrica | Valor | Observación |
|---|---|---|
| Archivos `.vue` totales | 38 | Incluye placeholders vacíos (History, Settings, Documents) |
| Archivos con al menos 1 clase Bootstrap | 27 | ~71% coverage |
| Ocurrencias totales de clases Bootstrap | **430** | Conteo por grep con patrón utilidades + componentes |
| Clases Bootstrap más usadas (Top 5) | `d-flex`, `gap-*`, `col-*`, `row`, `rounded-*` | 70% son **utilidades de layout**, 30% son componentes (`btn-*`, `card`, `modal`, `form-*`) |

### 1.2 Dependencias de Bootstrap JS (Críticas)

**Bootstrap JS está cargado globalmente** ([main.ts:6-7](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/main.ts#L6-L7)) y se usa en **2 componentes reales**:

| Componente | Atributo / API JS | Propósito | Plan de reemplazo |
|---|---|---|---|
| [AppLayout.vue:22](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L22-L22) | `data-bs-toggle="dropdown"` | Dropdown de menú de usuario en Topbar | Bloque 5: Componente Vue `AppDropdown.vue` (nativo, sin deps) |
| [UserMenu.vue:3](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/components/UserMenu.vue#L3-L3) | `data-bs-toggle="dropdown"` | Dropdown avatar sidebar (mismo patrón) | Bloque 5: Reusar `AppDropdown.vue` |

**Modals**: Híbrido. No usan `new bootstrap.Modal()` — usan `v-if` + clases de estilos Bootstrap. El JS de Bootstrap NO interviene.

| Componente | Markup modal | Plan |
|---|---|---|
| [UserModal.vue:2-4](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/user/components/UserModal.vue#L2-L4) | `.modal .fade .show .d-block` / `.modal-dialog` / `.modal-content` | Bloque 6: Migrar markup a Tailwind (overlay fijo, z-index, backdrop). Igual a CallModal que YA está semi-migrado. |
| [CallModal.vue:2](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/calls/components/CallModal.vue#L2-L2) | `fixed inset-0 z-50 ...` — **ya usa Tailwind-style** | Ya migrado. Buen patrón referencia. |

---

## 2. Estrategia de Migración: Dual-Style Seguro

```
┌────────────────────────────────────────────────────────────┐
│  FASE DE CONVIVENCIA (Bloques 1 → 6)                        │
│  ┌─────────────────────────┐     ┌──────────────────────┐ │
│  │  Bootstrap 5.3 (ACTIVO)  │ ⇄  │ Tailwind v3 (prefijo │ │
│  │  - 430 clases reduciéndose│    │  tw-, Preflight: OFF)│ │
│  │  - Dropdown JS activo     │    │  - theme.extend --app│ │
│  └─────────────────────────┘     └──────────────────────┘ │
│                         ↓                                   │
│  BLOQUE 7 (PURGA FINAL)                                     │
│  • Eliminar imports Bootstrap de main.ts                    │
│  • Quitar prefijo tw- de tailwind.config                    │
│  • Activar Tailwind Preflight                               │
│  • npm uninstall bootstrap bootstrap-icons @popperjs/core   │
└────────────────────────────────────────────────────────────┘
```

**Ventajas**:
- Cero regresiones funcionales (Bootstrap sigue vivo en cada transición).
- Cada bloque es un commit atómico reversible.
- Preflight apagado = Bootstrap reset y Tailwind no pisan estilos del otro.

---

## 3. Setup Inicial (Bloque 0 — Común a Todo el Proyecto)

### 3.1 Instalación de Dependencias

```bash
# Dev dependencies
npm install -D tailwindcss@^3.4 postcss autoprefixer
npm install -D @tailwindcss/forms @tailwindcss/typography
```

### 3.2 `tailwind.config.ts` (Estructura Base)

```typescript
// tailwind.config.ts
export default {
  prefix: 'tw-',                          // <-- PREFIJO OBLIGATORIO (evita conflictos)
  corePlugins: { preflight: false },      // <-- PREFLIGHT OFF mientras Bootstrap vivo
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      // ======================================================
      // BINDING DOBLE DE TOKENS: Tailwind ↔ --app-* CSS
      // Cada key usa var(--app-*, fallback) para mantener
      // compatibilidad con main.css durante la transición.
      // ======================================================
      colors: {
        primary:    { DEFAULT: 'var(--app-primary, #4b41e1)',
                      dark:    'var(--app-primary-dark, #4338ca)',
                      light:   'var(--app-primary-light, #645efb)' },
        secondary:  { DEFAULT: 'var(--app-secondary, #0090a9)',
                      light:   'var(--app-secondary-light, #acedff)' },
        slate:      { /* 50 → 900 mapeados a var(--app-slate-*) */ },
        success:    'var(--app-success, #15803d)',
        warning:    'var(--app-warning, #b45309)',
        error:      'var(--app-error, #ba1a1a)',
      },
      backdropBlur: {
        glass: 'var(--app-glass-blur, blur(16px))',
        'glass-sm': 'var(--app-glass-blur-sm, blur(12px))',
      },
      boxShadow:  { 'glass': 'var(--app-glass-shadow)',
                    'glass-hover': 'var(--app-glass-shadow-hover)' },
      borderRadius: {
        'glass-sm':   'var(--app-glass-radius-sm, 0.75rem)',
        'glass-md':   'var(--app-glass-radius-md, 1.1rem)',
        'glass-lg':   'var(--app-glass-radius-lg, 1.25rem)',
        'glass-xl':   'var(--app-glass-radius-xl, 1.5rem)',
        'pill':       'var(--app-radius-pill, 9999px)',
      },
      fontFamily: { sans: ['var(--app-font-family, Inter)'] },
    },
  },
  plugins: [
    require('@tailwindcss/forms')({ strategy: 'class' }),  // .tw-form-input, .tw-form-select… evita sobrescribir .form-control de Bootstrap
    require('@tailwindcss/typography'),
  ],
}
```

### 3.3 `postcss.config.ts`

```typescript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### 3.4 Inyección Directivas en main.css

```css
/* ============================================================
   [0/4] DIRECTIVAS TAILWIND (prefijo tw-, sin Preflight)
   Se insertan ANTES de los tokens :root para que los tokens
   puedan sobrescribir defaults de los plugins (forms).
   ============================================================ */
@tailwind components;
@tailwind utilities;

/* …resto del archivo: tokens :root, .app-card-glass, aliases… intactos.
   .app-card-glass se mantienen como clases de compatibilidad y se
   reemplazarán por @apply o tw-* inline en Bloque 8 (refactor estético).
*/
```

### 3.5 Validación Post-Setup Obligatoria

✅ `npm.cmd run build-only` exit code 0
✅ `npm.cmd run type-check` → SOLO se ignora error de `eslint-plugin-oxlint` (existente, no relacionado)
✅ Servidor `dev` abre sin errores 404 de CSS

---

## 4. Plan de Bloques de Migración (9 Bloques)

### 📦 Bloque 1: SETUP TAILWIND + DASHBOARD
**Alcance**: 9 archivos, ~180 clases Bootstrap → `tw-*`
**Archivos**: `DashboardView.vue`, `DashboardHeroCard.vue`, `DashboardKpiGrid.vue`, `DashboardRecentProjects.vue`, `DashboardActiveCalls.vue`, `DashboardS3UploadPanel.vue`, `DashboardSystemHealthPanel.vue`, `DashboardSupportCard.vue`
**No tocar**: `AppLayout.vue` (dropdowns JS, Topbar/Rail necesitan Bootstrap para dropdowns)
**Criterio de salida**: Cada `class="row g-4 d-flex …"` → `class="tw-grid tw-gap-4 tw-flex…"`. Botones `.btn-primary` → estilos inline `tw-bg-primary tw-text-white…` o componente `AppButton.vue` (opcional).

### 📦 Bloque 2: AUTH MODULE (Login + Register)
**Alcance**: 8 archivos, ~120 clases Bootstrap
**Archivos**: `LoginView.vue`, `RegisterView.vue`, `AuthSidebar.vue`, `AuthRegisterSidebar.vue`, `AuthLoginMobileHeader.vue`, `AuthRegisterMobileHeader.vue`, `SSOButtons.vue`, `ErrorAlert.vue`, `RegisterSuccessState.vue`
**Riesgo bajo**: 100% markup + utilidades Bootstrap, 0 JS Bootstrap.

### 📦 Bloque 3: LAYOUT + HOMEVIEW
**Alcance**: 4 archivos, ~80 clases Bootstrap + 2 dropdowns
**Archivos**: `AppLayout.vue`, `UserAvatar.vue`, `UserMenu.vue`, `HomeView.vue`
**⚠️ Importante**: Dropdowns `data-bs-toggle="dropdown"` → NO migrar todavía. Bloque 5.
**Estrategia**: Migrar TODAS las clases Bootstrap a `tw-*` PERO dejar `data-bs-toggle` intacto + clases `dropdown-menu` (Bootstrap necesita estas clases para su JS). Cuando Bloque 5 llegue, `dropdown-menu` también se migra.

### 📦 Bloque 4: USER MODULE (Profile + Users CRUD)
**Alcance**: 5 archivos, ~90 clases Bootstrap
**Archivos**: `ProfileView.vue`, `UserListView.vue`, `UserModal.vue`, `UserTable.vue`, `UserAvatar.vue` (si hace falta)
**Punto clave**: UserModal usa `modal fade show d-block` markup — reemplazar por patrón CallModal (fijo, z-50, backdrop).

### 📦 Bloque 5: CALLS MODULE + DROPDOWNS REACTIVOS
**Alcance**: 3 archivos + creación `AppDropdown.vue`
**Archivos**: `CallsListView.vue`, `CallCard.vue`, `CallModal.vue`
**Nuevo componente**: `src/shared/components/AppDropdown.vue` — implementación Vue pura con:
- `v-model` para abierto/cerrado
- Click-outside detection (composable `useClickOutside.ts`)
- ESC para cerrar
- `teleport` a `body` (opcional)
- ARIA `aria-expanded` / `role="menu"` (accesibilidad)
**Después**: Reemplazar en AppLayout.vue + UserMenu.vue los `data-bs-toggle` por `<AppDropdown>`.

### 📦 Bloque 6: MODULES PLACEHOLDER (Projects, Documents, History, Settings)
**Alcance**: 8 archivos (principalmente vacíos, bajo esfuerzo)
**Archivos**: `ProjectsListView.vue`, `ProjectDetailView.vue`, `ProjectCard.vue`, `ProjectFilter.vue`, `DocumentsView.vue`, `DocumentTable.vue`, `HistoryView.vue`, `SettingsView.vue`
**Método**: Aplicar plantilla base `tw-container tw-mx-auto tw-p-4` + Header `tw-flex tw-justify-between…`. Si el archivo está completamente vacío → dejar stub con layout base.

### 📦 Bloque 7: PURGA FINAL DE BOOTSTRAP (Punto de No Retorno)
**Checklist de entrada**:
- [ ] grep por `data-bs-` → 0 resultados
- [ ] grep por clases Bootstrap core (container\|row\|col-\|btn-\|card\|modal\|dropdown\|alert\|badge\|nav-) → 0 resultados en src/**
- [ ] grep por `new bootstrap\|bootstrap.` → 0 resultados

**Pasos**:
1. Eliminar `main.ts:6-7` (import bootstrap CSS + JS)
2. Quitar `prefix: 'tw-'` de `tailwind.config.ts`
3. Cambiar `corePlugins: { preflight: true }` (activar reset Tailwind)
4. **Find & Replace global**: `class="[^"]*tw-([a-z])"` → `class="…\L$1"` (quitar prefijo)
5. `npm uninstall bootstrap bootstrap-icons @popperjs/core`
6. 🔁 Validación exhaustiva manual: Login, Dashboard, User CRUD, Modals, Dropdowns, Responsive Mobile.

### 📦 Bloque 8: REFACTOR ESTÉTICO POST-MIGRACIÓN
- Reemplazar clases de compatibilidad `.app-card-glass` → `tw-backdrop-blur-glass tw-bg-white/82 tw-border-white/90 …`
- Crear componentes reutilizables: `<AppButton variant="primary|outline|ghost" />`, `<AppCard variant="glass|flat" />`, `<AppBadge status="success|warning|error" />`
- Extraer composables: `useBreakpoints`, `useClickOutside`

---

## 5. Matriz de Equivalencias (Bootstrap → Tailwind Prefixed)

> Referencia rápida para migración de cada bloque.

| Bootstrap 5.3 Utility | Tailwind con prefix `tw-` |
|---|---|
| `.d-flex` | `.tw-flex` |
| `.d-none` / `.d-md-block` | `.tw-hidden` / `.md:tw-block` |
| `.flex-column` | `.tw-flex-col` |
| `.justify-content-between` → `.justify-content-start` | `.tw-justify-between` → `.tw-justify-start` |
| `.align-items-center` | `.tw-items-center` |
| `.gap-1` … `.gap-5` | `.tw-gap-1` … `.tw-gap-5` (Tailwind escala x 0.25rem = igual) |
| `.row` | `.tw-grid tw-grid-cols-1 md:tw-grid-cols-2 lg:tw-grid-cols-4 …` (según contexto) |
| `.col-12` / `.col-md-6` / `.col-lg-3` | (se resuelve con `md:tw-col-span-6`, `lg:tw-col-span-3`) |
| `.container` / `.container-fluid` | `.tw-container tw-mx-auto tw-px-4` |
| `.p-2` / `.p-4` / `.px-3` / `.py-2` / `.mb-3` / `.mt-4` | `.tw-p-2` / `.tw-p-4` / `.tw-px-3` / `.tw-py-2` / `.tw-mb-3` / `.tw-mt-4` |
| `.rounded` / `.rounded-3` / `.rounded-4` / `.rounded-circle` | `.tw-rounded` / `.tw-rounded-xl` / `.tw-rounded-2xl` / `.tw-rounded-pill` |
| `.shadow-sm` / `.shadow` / `.shadow-lg` | `.tw-shadow-sm` / `.tw-shadow` / `.tw-shadow-lg` |
| `.text-start` / `.text-center` / `.text-end` | `.tw-text-left` / `.tw-text-center` / `.tw-text-right` |
| `.text-muted` | `.tw-text-slate-500` |
| `.text-primary` / `.text-danger` / `.text-success` / `.text-warning` | `.tw-text-primary` / `.tw-text-error` / `.tw-text-success` / `.tw-text-warning` |
| `.text-dark` | `.tw-text-slate-900` |
| `.text-white` | `.tw-text-white` |
| `.fw-bold` / `.fw-semibold` / `.fw-medium` / `.fw-light` | `.tw-font-bold` / `.tw-font-semibold` / `.tw-font-medium` / `.tw-font-light` |
| `.fs-4` / `.fs-5` / `.fs-6` / `.small` | `.tw-text-2xl` / `.tw-text-xl` / `.tw-text-base` / `.tw-text-xs` |
| `.bg-white` / `.bg-light` / `.bg-light-subtle` | `.tw-bg-white` / `.tw-bg-slate-50` / `.tw-bg-slate-100` |
| `.bg-primary` / `.bg-success-bg` → (tokens) | `.tw-bg-primary` / `.tw-bg-success/10` |
| `.border-0` / `.border` / `.border-bottom` | `.tw-border-0` / `.tw-border` / `.tw-border-b` |
| `.position-relative` / `.position-absolute` / `.position-fixed` | `.tw-relative` / `.tw-absolute` / `.tw-fixed` |
| `.top-0` / `.start-0` / `.end-0` / `.bottom-0` / `.inset-0` | `.tw-top-0` / `.tw-left-0` / `.tw-right-0` / `.tw-bottom-0` / `.tw-inset-0` |
| `.z-1050` (Bootstrap index) | `.tw-z-[1050]` |
| `.overflow-hidden` | `.tw-overflow-hidden` |
| `.object-fit-cover` | `.tw-object-cover` |
| `.w-100` / `.h-100` | `.tw-w-full` / `.tw-h-full` |
| `.min-vh-100` | `.tw-min-h-screen` |
| `.max-w-*` | `.tw-max-w-*` (o `.tw-max-w-[860px]` arbitrario) |

---

## 6. Criterios de Aceptación por Bloque

Cada bloque migrado DEBE cumplir estos 5 checks antes de marcarse como "done":

- [ ] **Compilación** → `npm run build-only` exit code 0
- [ ] **Diagnósticos** → VSCode `GetDiagnostics` sin errores en archivos modificados
- [ ] **Sin duplicados** → grep por `class="[^"]*(row|col-|container|btn-|card|badge|alert|form-|input-group|modal|d-flex|justify-|align-|gap-|p-|m-|rounded|shadow|text-|bg-|border-|fw-|fs-|position-|overflow-|object-fit)[^"]*"` → 0 matches EN LOS ARCHIVOS DEL BLOQUE (fuera del bloque se permiten = migración incremental)
- [ ] **Smoke visual**: Abrir navegador y comparar antes/después:
  - Layout Desktop (≥1024px) igual al original
  - Layout Mobile (<768px) igual al original (rail oculto, bottom nav visible)
  - Estados hover, focus, active de botones y tarjetas iguales
  - Breakpoints responsive respetados
- [ ] **Accesibilidad** → `aria-*`, `role="*"`, labels for inputs intactos. No eliminar `aria-expanded`, `aria-label`, `aria-hidden`, `alt` en imágenes.

---

## 7. Reglas de Oro (No negociables)

1. **No tocar lógica**: Script setup, emits, props, stores, router = READ-ONLY durante migración. Única excepción: Bloque 5 (dropdowns) = reemplazo de template `data-bs-toggle` por componente Vue.
2. **Prefijo `tw-` mandatorio**: Hasta Bloque 7, NUNCA escribir clases Tailwind sin el prefijo.
3. **No mezclar 2 frameworks en el MISMO elemento** (ok tener en un mismo template `<div class="row g-4">` Bootstrap + `<div class="tw-flex tw-gap-2">` en un child, pero no `class="row tw-grid"` en mismo nodo — ambigüedad).
4. **Tokens via `theme.extend`**: no hardcodear `#4b41e1` en archivos .vue → siempre `tw-bg-primary` (que mapea a `var(--app-primary)`).
5. **Bootstrap Icons + Material Symbols**: se mantienen. `bootstrap-icons` no tiene que ver con Bootstrap CSS, es fuente de íconos independiente.

---

## 8. Seguimiento (Checklist Ejecutivo)

| Bloque | Descripción | Fecha Inicio | Fecha Fin | Estado | QA Pass |
|---|---|---|---|---|---|
| 0 | Setup Tailwind + Config + docs | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
| 1 | Dashboard Completo (9 files) | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
| 2 | Auth (Login/Register) | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
| 3 | Layout + HomeView | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
| 4 | User Module | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
| 5 | Calls + AppDropdown Reactive | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
| 6 | Placeholder Modules + Limpieza Residual | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
| 7 | Purga Final Bootstrap | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
| 8 | Refactor Estético + Shared Components | 2026-08-05 | 2026-08-05 | ✅ Completado | ✅ |
