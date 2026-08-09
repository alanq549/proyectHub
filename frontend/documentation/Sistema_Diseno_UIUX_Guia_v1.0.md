# ProjectHub — Guía de Sistema de Diseño UI/UX (Frontend)
**Versión 1.0 | Fecha: 2026-08-08 | Ámbito: `frontend/`**

---

## 1. Propósito y Alcance

Este documento define:

1. **Paleta de colores oficial**: tokens `--app-*` canónicos, mapeo Tailwind y prohibición de valores hardcodeados.
2. **Jerarquía UI/UX**: tipografía, superficies, elevaciones, espaciados y radii estandarizados.
3. **Correcciones obligatorias** sobre vistas ya implementadas (Home, Auth, Dashboard, Layout, Profile, Calls).
4. **Normativas de implementación** para vistas nuevas.

Fuentes canónicas de la verdad:

- [main.css](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/assets/main.css) — tokens globales `--app-*`.
- [tailwind.config.ts](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/tailwind.config.ts) — mapeo Tailwind 1:1 sobre `var(--app-*, fallback)`.
- [AppButton.vue](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/shared/components/AppButton.vue) / [AppCard.vue](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/shared/components/AppCard.vue) / [AppInput.vue](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/shared/components/AppInput.vue) — componentes base compartidos.

---

## 2. Auditoría de Paleta — Inconsistencias Detectadas

> **Severidad ALTA**: existe una dualidad de "color primario" en toda la base de código que rompe la semántica.

| Hallazgo | Ubicaciones detectadas | Corrección |
|---|---|---|
| `--app-primary` declarado `#0f172a` (Slate 900 / "negro") pero múltiples componentes usan `#4b41e1` (índigo/morado) como primario efectivo. | [AppLayout.vue#L452-L453](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L452-L453), [AppLayout.vue#L524](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L524), [DashboardHeroCard.vue#L144-L146](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/dashboard/components/DashboardHeroCard.vue#L144-L146), [DashboardHeroCard.vue#L170-L171](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/dashboard/components/DashboardHeroCard.vue#L170-L171), [LoginView.vue#L368-L369](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/auth/views/LoginView.vue#L368-L369), [HomeView.vue pasim](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/views/HomeView.vue). | **Decisión**: Slate 900 `#0f172a` = color primario tipográfico / de marca. El índigo `#4b41e1` se convierte en `--app-accent` (color de acento para CTA, fáb, focus-ring, badges de rol). (Ver §3.2) |
| Valores RGB/RGBA/Hex **hardcodeados** inline o en `<style scoped>` en lugar de usar tokens. | [HomeView.vue#L232](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/views/HomeView.vue#L232), [HomeView.vue#L241](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/views/HomeView.vue#L241), [UserAvatar.vue#L34](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/components/UserAvatar.vue#L34), [RegisterView.vue#L392](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/auth/views/RegisterView.vue#L392) (usa `#22c55e` != `--app-success #15803d`), [DashboardView.vue pasim](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/dashboard/views/DashboardView.vue) (`iconBg`, `iconColor` con hex crudos). | Todo color debe pasar por `var(--app-*)` o su clase Tailwind equivalente. Ningún hex/rgba crudo permitido fuera de `:root` en `main.css`. |
| Desalineación de fallbacks entre `main.css` y `tailwind.config.ts` en tokens de surface. | `surface-container`: main.css `#eceef0` vs tailwind fallback `#e8eaed`; `surface-container-high`: `#e6e8ea` vs `#dcdfe2`; `surface-container-highest`: `#e0e3e5` vs `#d0d3d6`. | Los fallbacks de Tailwind deben coincidir **exactamente** con los valores de `main.css` (single source of truth). |
| `--app-outline` (`#76777d`) y `--app-on-surface-variant` (`#475569`) usados de forma indistinta para texto secundario. | CallsListView KPI labels (`tw-text-outline`), LoginView form-label-custom (`--on-surface-variant`), etc. | Regla semántica: **texto** → `--app-on-surface-variant`; **bordes / divisores** → `--app-outline` / `--app-outline-variant`. |
| Contraseña fuerte en RegisterView usa códigos Bootstrap (`#dc3545`, `#ffc107`, `#22c55e`) en lugar de los tokens de estado canónicos. | [RegisterView.vue#L386-L392](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/auth/views/RegisterView.vue#L386-L392). | Mapear: `--app-error`, `--app-warning`, `--app-success` con sus `*-bg` y opacidad adecuada. |

---

## 3. Paleta de Colores Oficial (Corregida)

### 3.1 Taxonomía de Tokens

Regla de naming: `--app-{rol}[{-variante}]`. **No usar tokens sin prefijo `--app-` en componentes nuevos** (los existentes como `--primary`, `--surface-container`, etc. son alias de compatibilidad que se eliminarán en el Bloque 7).

### 3.2 Paleta Semántica Definitiva

| Token | Valor Hex/RGBA | Tailwind Key | Propósito / Cuándo usar |
|---|---|---|---|
| **`--app-primary`** | `#0f172a` (Slate 900) | `tw-bg-primary` / `tw-text-primary` | Color de marca principal. Títulos, brand name, borde focus default, botón primario sólido. |
| `--app-primary-dark` | `#000000` | `tw-bg-primary-dark` | Hover botón primario, bordes oscuros. |
| `--app-primary-light` | `#334155` (Slate 700) | `tw-bg-primary-light` | Variant más suave. |
| **`--app-accent`** ⭐ (nuevo) | `#4b41e1` (Índigo 600) | `tw-bg-accent` / `tw-text-accent` | Acento visual. FAB, badges de rol, CTA especiales, focus-ring de inputs. |
| `--app-accent-hover` (nuevo) | `#4338ca` (Índigo 700) | `hover:tw-bg-accent-hover` | Hover de elementos accent. |
| `--app-accent-bg` (nuevo) | `rgba(75, 65, 225, 0.08)` | `tw-bg-accent/8` | Fondo sutil para badges/estados activos accent. |
| `--app-secondary` | `#475569` (Slate 600) | `tw-text-secondary` | Subtítulos / elementos menos relevantes que primary. |
| `--app-secondary-light` | `#f1f5f9` (Slate 100) | `tw-bg-secondary-light` | Fondos neutros suaves. |
| **On-colors (texto sobre superficies)** | | | |
| `--app-on-primary` | `#ffffff` | `tw-text-on-primary` | Texto blanco sobre botones primarios / accent oscuros. |
| `--app-on-surface` | `#0f172a` | `tw-text-on-surface` | Texto body principal (párrafos, títulos). |
| `--app-on-surface-variant` | `#475569` (Slate 600) | `tw-text-on-surface-variant` | **Texto secundario**: labels, descripciones, placeholders, metadatos. |
| **Grises escala Slate (solo para variantes visuales, NO para semántica)** | | | |
| `--app-slate-50..900` | Ver `main.css` [L28-L37](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/assets/main.css#L28-L37) | `tw-slate-*` | Únicamente cuando se necesita un matiz de gris específico (ej: borde sutil `slate-200`). Preferir siempre tokens semánticos antes. |
| `--app-black` | `#000000` | `tw-bg-black` | Excepciones (nunca como reemplazo de `--app-primary`). |
| **Bordes / Outline** | | | |
| `--app-outline` | `#76777d` | `tw-border-outline` | Divisores secundarios, borde inactivo. |
| `--app-outline-variant` | `#c6c6cd` | `tw-border-outline-variant` | Borde de inputs inactivos, bordes de cards outlined. |
| **Estados de Feedback** | | | |
| `--app-success` | `#15803d` (Green 700) | `tw-text-success` | Estado OK, aprobado, tendencia positiva. |
| `--app-success-bg` | `rgba(220, 252, 231, 0.8)` | `tw-bg-success-bg` | Fondo chip/badge de éxito. |
| `--app-warning` | `#b45309` (Amber 700) | `tw-text-warning` | Advertencias, en revisión. |
| `--app-warning-bg` | `rgba(254, 243, 199, 0.8)` | `tw-bg-warning-bg` | Fondo chip warning. |
| `--app-error` | `#ba1a1a` (Red 700) | `tw-text-error` | Errores de formulario, alertas, notif-dot. |
| `--app-error-bg` | `rgba(254, 226, 226, 0.8)` | `tw-bg-error-bg` | Fondo alerta/error. |

> **Acción inmediata 1**: Añadir `--app-accent`, `--app-accent-hover`, `--app-accent-bg` a `main.css :root` y su mapeo correspondiente a `tailwind.config.ts → theme.extend.colors.accent`.

### 3.3 Superficies (Material Design 3 Scale)

Escala de elevación por temperatura de fondo. **Orden de menor a mayor temperatura**:

| Token (main.css [L66-L71](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/assets/main.css#L66-L71)) | Valor | Tailwind Key | Cuándo usar |
|---|---|---|---|
| `--app-surface-container-lowest` | `#ffffff` | `tw-bg-surface-container-lowest` | Inputs, campos rellenables, chips individuales. |
| `--app-surface-container-low` | `#f2f4f6` | `tw-bg-surface-container-low` | Tarjetas flat, fondo de botón secondary, rail nav. |
| `--app-surface-container` | `#eceef0` | `tw-bg-surface-container` | Área de carga avatar dashed, fondo iconos, footer. |
| `--app-surface-container-high` | `#e6e8ea` | `tw-bg-surface-container-high` | Hover de rail-link / icon-btn, estado pressed. |
| `--app-surface-container-highest` | `#e0e3e5` | `tw-bg-surface-container-highest` | Dropdowns abiertos, menús, avatares fallback. |
| `--app-surface` | `#f7f9fb` | — (no Tailwind key aún) | Fondo de secciones HomeView. |

> **Acción inmediata 2**: Corregir fallbacks en tailwind.config.ts surface-container / high / highest para que coincidan con `main.css`. Añadir `surface` a Tailwind keys.

---

## 4. Jerarquía Tipográfica

### 4.1 Escala Oficial

Los tokens ya están declarados en Tailwind pero **no se usan sistemáticamente**. Obligatorio para vistas nuevas:

| Token / Tailwind Key | Size | Line-height | Weight | Uso |
|---|---|---|---|---|
| `fontSize.hero-title` | `3rem` (48px) | `1.05` | 900 | Título Hero de landing. Exclusivo HomeView hero. |
| `fontSize.hero-sub` | `1.05rem` (16.8px) | `1.55` | 400 | Subtítulo hero. |
| `fontSize.section-title` | `1.65rem` (26.4px) | `1.3` | 800 | Título de sección dentro de una vista. |
| **Nuevos tokens a añadir**: | | | |
| `page-title` | `1.5rem` (24px) | `1.25` | 700 | `h1` de vistas internas (Profile, Calls, Projects, Dashboard). Clase Tailwind: `tw-text-page-title` o combinación `tw-text-2xl tw-font-bold` **con consistencia**. |
| `card-title` | `1.125rem` (18px) | `1.35` | 600 | `h2/h3` dentro de AppCard. |
| `label` | `0.75rem` (12px) | `1.2` | 500 | Labels de inputs, KPI label. **NO 0.75rem con 11px mezclados**. |
| `caption` | `0.6875rem` (11px) | `1.2` | 500 | Exclusivo para KPI footnotes, chip contents. |
| `body-base` | `1rem` (16px) | `1.6` | 400 | Párrafos, descripciones. |
| `body-small` | `0.875rem` (14px) | `1.5` | 400 | Textos de card description. |

> **Regla de corrección**: En vistas existentes, unificar `h1` de página a **24px / 700 / #0f172a**. Actualmente:
> - [ProfileView.vue#L126](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/user/views/ProfileView.vue#L126) → `tw-text-2xl tw-font-bold` ✅ (24px, 700).
> - [CallsListView.vue#L6](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/calls/views/CallsListView.vue#L6) → `tw-text-2xl tw-font-bold` ✅.
> - [DashboardHeroCard.vue#L135](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/dashboard/components/DashboardHeroCard.vue#L135) → 26px / 800. ⚠️ Es un hero de dashboard, mantener como excepción o tokenizar como `dashboard-hero-title`.
> - [LoginView.vue#L284-L296](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/auth/views/LoginView.vue#L284-L296) → 24/32px / 600. ✅ Correcto para auth.

### 4.2 Color de Texto (Obligatorio)

| Elemento | Color Token | Tailwind |
|---|---|---|
| Título (H1..H3), brand name, body destacado | `--app-on-surface` → `#0f172a` | `tw-text-on-surface` |
| Subtítulo, label, placeholder, descripción, metadata | `--app-on-surface-variant` → `#475569` | `tw-text-on-surface-variant` |
| Texto sobre botón primario/accent sólido | `--app-on-primary` → `#ffffff` | `tw-text-on-primary` |
| KPI value, número destacado | `--app-slate-900` (igual a on-surface pero peso 800) | `tw-text-slate-900` |
| KPI label (solo este caso) | `--app-slate-500` → `#64748b` | `tw-text-slate-500` |

---

## 5. Sistema de Layout — Grid, Espaciados y Radii

### 5.1 Grid de 12 Columnas (Tailwind)

Usar siempre `tw-grid` (no `row`/`col-*` de Bootstrap en código nuevo):

| Breakpoint | Tailwind Key | Ancho mínimo | Columnas base | Gutters (gap) |
|---|---|---|---|---|
| Mobile | default | < 576px | 1 | `tw-gap-4` (16px) |
| Tablet | `sm:` | ≥ 576px | 2 | `tw-gap-4` |
| Laptop | `md:` / `lg:` | ≥ 768px / ≥ 992px | 8 + 4 (dashboard) o 3 | `tw-gap-4` o `tw-gap-6` |
| Desktop | `xl:` / `2xl:` | ≥ 1200px | 4 | `tw-gap-4` o `tw-gap-6` |

### 5.2 Padding de AppLayout (Obligatorio)

Actualmente correcto en [AppLayout.vue#L460-L464](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue#L460-L464):
- Top: `80px`
- Left: `calc(64px + 16px)` (rail + gap) / mobile `16px`
- Right: `16px`
- Bottom: `96px` (bottom nav)
- Min-height: `100vh`

### 5.3 Padding de Contenedores HomeView

- `.container-max`: Desktop `padding-x: 64px`, Mobile `24px`, max-width `1280px`. Correcto.

### 5.4 Border Radius Estandarizados

**Prohibición**: ningún `border-radius` hardcodeado fuera de estos tokens.

| Token / Tailwind | Valor | Casos de uso |
|---|---|---|
| `--app-radius-pill` / `tw-rounded-pill` | `9999px` | Badges, chips, FAB, avatar. |
| `--app-input-radius` / `tw-rounded-input` | `0.5rem` (8px) | ⚠️ **Corregir LoginView**: inputs/auth actualmente usan `0.75rem`. Unificar: inputs → 0.5rem, botones → 0.75rem. |
| `--app-glass-radius-sm` / `tw-rounded-glass-sm` | `0.75rem` (12px) | Cards light, KPI icon box, botones. |
| `--app-btn-radius-md` (implícito) | `0.75rem` | Botones md/lg. |
| `--app-glass-radius-md` / `tw-rounded-glass-md` | `1.1rem` | AppCard glass default. |
| `--app-glass-radius-lg` / `tw-rounded-glass-lg` | `1.25rem` | AppCard glass-table. |
| `--app-glass-radius-xl` / `tw-rounded-glass-xl` | `1.5rem` | AppCard glass-xl (Hero). |
| `--app-flat-radius` / `tw-rounded-2xl` | `1rem` | AppCard flat. |
| — / `tw-rounded-3xl` | `1.5rem` | Process image (HomeView). OK. |
| — / `tw-rounded-[2rem]` | `2rem` | CTA box (HomeView) y Auth card wrapper. OK como excepción. |

> **Acción inmediata 3**: Unificar `border-radius` de inputs a **0.5rem** (`--app-input-radius`) en LoginView/RegisterView. Actualmente está a `0.75rem` en `LoginView.vue#L357`.

---

## 6. Sistema de Elevaciones — Sombras y Glassmorphism

### 6.1 Cuatro Variantes de Tarjetas (Usar AppCard, NO clases locales)

| Variant de AppCard | Fondo | Blur | Borde | Shadow | Caso |
|---|---|---|---|---|---|
| `glass` (default) | `rgba(255,255,255,0.72)` | `blur(20px)` | 1px white/90 + bottom black/6 | `--app-glass-shadow` | KPI, Upload, SystemHealth, Profile sections. |
| `glass-xl` | `rgba(255,255,255,0.75)` | `blur(20px)` | 1px white/90 + bottom primary/10 | `--app-glass-shadow` versión grande | Dashboard Hero Card. |
| `glass-light` | `rgba(255,255,255,0.55)` | `blur(12px)` | 1px white/50 + shadow-sm | Shadow small | CallCard / convocatorias. |
| `flat` | `#ffffff` | — | 1px slate-200 | `--app-flat-shadow` | Tabla Users, tablas densas. |
| `outlined` | transparent | — | 1px slate-200 | — | Chip container, badge wrapper. |

> **Corrección**: En [HomeView.vue#L231-L237](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/views/HomeView.vue#L231-L237) la clase local `.glass-card` tiene valores diferentes del estándar. Sustituir por `<AppCard variant="glass">` o la clase utilidad global `.app-card-glass` de main.css. Eliminar la definición scoped duplicada.

### 6.2 Sombras de Botones (AppButton Estandarizado)

| Variant | Shadow |
|---|---|
| `primary` | `--app-btn-primary-shadow` (hover + versión hover) |
| `secondary` / `outline` / `ghost` | `shadow-sm` o ninguno. |
| `danger` | `shadow-sm`. |

> **Corrección grave**: [DashboardHeroCard.vue#L169-L238](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/dashboard/components/DashboardHeroCard.vue#L169-L238) define sus propios botones `af-btn-primary`, `af-btn-black`, `af-btn-outline` **en lugar de usar AppButton**. Además:
> - `af-btn-primary` usa **accent índigo** como "primario", inconsistente con `AppButton variant=primary` (slate).
> - `af-btn-black` = slate 900, que sí coincide con primario.
> 
> **Resolución**: Sustituir los 3 botones del Hero Card por `<AppButton>`:
> - `Gestionar Usuarios` → AppButton `variant="accent"` (una vez añadida la variante accent a AppButton).
> - `Descargar Reporte` → AppButton `variant="outline"`.
> - `Nueva Auditoría` → AppButton `variant="primary"` (slate 900).
>
> Añadir previamente la variante `accent` a `AppButton.vue` (mapeo de colores `--app-accent`, `--app-accent-hover`, `--app-on-primary`).

### 6.3 Focus Rings (Accesibilidad)

Única especificación para todos los elementos interactivos:

| Elemento | Focus |
|---|---|
| Input de formulario | `border-color: var(--app-accent)` + `box-shadow: 0 0 0 4px var(--app-accent-bg)` (4px, no 3px). Unificar el grosor. |
| Botones | `ring-2 ring-accent/20` (AppButton ya lo tiene). |
| Enlaces focus | Subrayado + `outline-accent`. |

> **Corrección**: LoginView tiene `box-shadow: 0 0 0 4px rgba(75, 65, 225, 0.10)` que casualmente coincide; pero debe sustituirse por `var(--app-accent-bg)` con opacidad aumentada a 0.12 (hacer token nuevo `--app-accent-focus-ring`). El token `--app-input-focus-ring` actual es slate 0.12; renombrarlo/redirigirlo a accent.

---

## 7. Sistema de Botones

Variante canónica única — **usar siempre `<AppButton>`**. 3 variantes + 1 accent + 1 danger = 5. Ninguna clase de botón local scoped permitida en nuevos componentes.

| Variant | Fondo | Borde | Texto | Sombra | Cuándo |
|---|---|---|---|---|---|
| `primary` | `--app-primary` (#0f172a) → hover `--app-primary-dark` | 1px `--app-primary-dark` | `--app-on-primary` | `--app-btn-primary-shadow` | Acción principal de página (Guardar, Enviar, Nueva auditoría). |
| **`accent`** ⭐ (nueva) | `--app-accent` (#4b41e1) → hover `--app-accent-hover` | 1px `--app-accent-hover` | `--app-on-primary` | `--app-btn-primary-shadow` versión accent | FAB, CTA único en página, Gestionar Usuarios (rol admin), botón con peso emocional alto. |
| `secondary` | `--app-surface-container-low` → hover `--app-surface-container` | 1px `--app-outline-variant` | `--app-on-surface` | `shadow-sm` | Acción secundaria (Cancelar, Reset, Ver demo). |
| `outline` | transparent → hover `--app-surface-container-low` | 1px `--app-outline-variant` → hover `--app-outline` | `--app-on-surface-variant` → hover `--app-on-surface` | — | Acción terciaria (Descargar reporte). |
| `ghost` | transparent → hover `--app-surface-container-low` | — | `--app-on-surface-variant` → hover `--app-on-surface` | — | Botones en barra de navegación, icon-only sin fondo. |
| `danger` | `--app-error` → hover `--app-error`/90% | 1px `--app-error` | `--app-on-primary` | `shadow-sm` | Eliminar, Borrar, Cerrar sesión en color rojo. |

**Tamaños**:

| Size | Padding | Font-size | Icon gap |
|---|---|---|---|
| `sm` | px-3 (12px) / py-1.5 (6px) | 12px (xs) | 6px |
| `md` (default) | px-4 (16px) / py-2 (8px) | 14px (sm) | 8px |
| `lg` | px-6 (24px) / py-3 (12px) | 16px (base) | 10px |

**Altura de botones en Auth (Login/Register)**: Actualmente 52px; no corresponde a ningún size de AppButton. Para botón full-width de auth, usar size `lg` + posiblemente altura extra por prop CSS. Tokenizar `--app-btn-auth-height: 52px` si se desea mantener.

---

## 8. Correcciones Puntuales por Vista (Checklist de Implementación)

### 8.1 Main CSS + Tailwind Config
| Tarea | Estado inicial | Acción | Prioridad |
|---|---|---|---|
| Añadir tokens `--app-accent`, `--app-accent-hover`, `--app-accent-bg`, `--app-accent-focus-ring` a `:root`. | No existen | Añadir en main.css bloque [L18-L50](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/assets/main.css#L18-L50). | 🔴 Alta |
| Añadir `colors.accent` a tailwind.config.ts | No existe | Mapeo `DEFAULT: var(--app-accent, #4b41e1)`, `hover: var(--app-accent-hover, #4338ca)`, `bg: var(--app-accent-bg, rgba(...))` | 🔴 Alta |
| Corregir fallbacks surface-container / high / highest en Tailwind. | Inconsistentes | Alinear con main.css valores. | 🟡 Media |
| Añadir tokens tipografía `page-title`, `card-title`, `label`, `caption` a Tailwind. | No existen | En `theme.extend.fontSize`. | 🟡 Media |
| Re-mapear `--app-input-focus-ring` de slate a accent. | slate/0.12 | Cambiar valor o crear `--app-input-focus-ring` a accent. | 🟡 Media |

### 8.2 AppButton.vue
| Tarea | Prioridad |
|---|---|
| Añadir variante `accent` a `variantClasses`. | 🔴 Alta |
| Asegurar que todos los `af-btn-*` y `btn-*` locales de Dashboard/Login/Home puedan migrarse. | 🔴 Alta |

### 8.3 AppLayout.vue ([archivo](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/layouts/AppLayout.vue))
| Tarea | Línea | Acción | Prioridad |
|---|---|---|---|
| Color activo rail-link | L452-L453 | Cambiar `--app-primary` (#4b41e1 fallback) por `--app-accent` + `--app-accent-bg`. Ya usa colores correctos pero nombres de token equivocados. | 🔴 Alta |
| Color FAB bottom-nav | L524 | Cambiar `--app-primary` por `--app-accent` (FAB es accent por definición). | 🔴 Alta |
| Search close btn text | L416 | Cambiar `--app-primary` (#4b41e1 fallback) por `--app-accent` o `--app-on-surface-variant`. | 🟡 Media |
| Blob bg colors | L559, L570 | Asegurar uso de tokens `--app-bg-blob-primary/secondary`. Fallbacks inline con rgba crudos deben ser los mismos valores del token. | 🟡 Baja |

### 8.4 DashboardHeroCard.vue ([archivo](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/dashboard/components/DashboardHeroCard.vue))
| Tarea | Línea | Acción | Prioridad |
|---|---|---|---|
| **Eliminar** clases `af-btn-primary`, `af-btn-outline`, `af-btn-black`. | L169-L238 | Sustituir `<button>` por `<AppButton>`: Gestionar Usuarios → `variant="accent"`, Descargar Reporte → `variant="outline"`, Nueva Auditoría → `variant="primary"`. | 🔴 Alta |
| Badge rol af-role-badge color | L144-L146 | Eliminar color morado crudo, usar `--app-accent-bg` + `--app-accent` | 🟡 Media |
| Hero glow background | L92-L99 | Sustituir rgba crudo por `--app-accent-bg` con opacidad mayor (15%). | 🟡 Baja |
| Avatar wrapper gradient | L130 | Sustituir `rgba(75, 65, 225, 0.3)` por token accent. | 🟡 Baja |
| Override de fondo .af-hero-card | L82-L89 | Mantener, pero documentar como variante "hero-gradient" permitida (solo esta card). | 🟢 Baja |

### 8.5 DashboardView.vue — KPI Icon Colors / Bg
| Tarea | Línea | Acción | Prioridad |
|---|---|---|---|
| `kpis[].iconBg`, `kpis[].iconColor` pasados como hex crudo | L90-L124 | Cambiar tipado Kpi para aceptar tokens semánticos o mapear en el componente: por defecto `iconBg = var(--app-accent-bg)`, `iconColor = var(--app-primary)` o `var(--app-accent)` según tipo. | 🟡 Media |
| `recentProjects[].orgBg`, `orgColor`, `iconBg` | L150-L169 y L127-L149 | Sustituir `#fef2f2`, `#b91c1c`, `##FDFDFE` (typo doble #) por tokens `--app-error-bg`, `--app-error`, `--app-surface-container-lowest`. **Incluye arreglo de typo `##FDFDFE` → `#ffffff` vía token**. | 🟡 Media |

### 8.6 LoginView.vue ([archivo](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/auth/views/LoginView.vue))
| Tarea | Línea | Acción | Prioridad |
|---|---|---|---|
| `btn-primary-custom` clase local | L381-L408 | Sustituir por `<AppButton variant="primary" size="lg" block>`. Mantener altura 52px con prop si es necesario. | 🔴 Alta |
| Input border-radius 0.75rem | L357 | Cambiar a `--app-input-radius` (0.5rem) o unificar token. Consistencia con AppInput. | 🟡 Media |
| Focus ring slate/accent dual | L366-L370 | Usar `--app-accent` para border-color y `--app-accent-focus-ring` para shadow. | 🟡 Media |
| Blobs rgba crudos | L231-L255 | Usar `--app-accent-bg` con opacidad variada. | 🟢 Baja |

### 8.7 RegisterView.vue ([archivo](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/modules/auth/views/RegisterView.vue))
| Tarea | Línea | Acción | Prioridad |
|---|---|---|---|
| Estilos inline alerta error | L27 | Sustituir `style="background-color: rgba(255, 218, 214, 0.5); border: 1px solid rgba(186, 26, 26, 0.10); color: var(--on-error-container, #93000a)"` por ErrorAlert component o clases `tw-bg-error-bg tw-border-error/20 tw-text-error`. | 🔴 Alta |
| Password strength colors Bootstrap crudos | L386-L392 | `#dc3545` → `var(--app-error)`; `#ffc107` → `var(--app-warning)`; `#22c55e` → `var(--app-success)`. | 🟡 Media |
| `strength-track` bg color fallback | L150 | `var(--outline-variant, #e0e0e0)` fallback erróneo (outline-variant es #c6c6cd). Corregir fallback. | 🟢 Baja |

### 8.8 HomeView.vue ([archivo](file:///c:/Users/alanq/OneDrive/Documentos/universidad/noveno%20semestre/ProjectHub/frontend/src/views/HomeView.vue))
| Tarea | Línea(s) | Acción | Prioridad |
|---|---|---|---|
| **Eliminar** clase local `.glass-card` | L231-L237 | Usar `.app-card-glass` global o `<AppCard variant="glass">`. | 🔴 Alta |
| `btn-signup`, `btn-login` locales | L264-L284 | Sustituir por `<AppButton>`: `btn-signup` → `variant="primary" size="md"`; `btn-login` → `variant="ghost" size="md"`. | 🔴 Alta |
| `btn-hero-primary / secondary` | L322-L350 | `<AppButton variant="primary" size="lg">` y `<AppButton variant="outline" size="lg">`. | 🔴 Alta |
| `btn-cta` fondo `--secondary` = índigo | L489-L500 | Sustituir por `<AppButton variant="accent" size="lg">`. CTA es accent. | 🔴 Alta |
| `.badge-pill` bg `rgba(226,223,255,0.3)` y color `--on-secondary-fixed-variant` (no existe token) | L293-L303 | bg → `--app-accent-bg` (aumentar opacidad); texto → `--app-accent`. | 🟡 Media |
| `.feature-icon` bg `--primary-fixed` (#dae2fd) — token sin prefijo app | L395-L409 | Añadir token `--app-feature-icon-bg` o usar `--app-accent-bg`; hover: `--app-accent`. | 🟡 Media |
| `.hero-image-glow` gradient hardcodeado rgba(75,65,225) | L357-L364 | Usar tokens accent + slate opacity. | 🟢 Baja |
| `.cta-blob-1/2` rgba crudos | L460-L473 | Usar `--app-accent-bg` variantes. | 🟢 Baja |
| `.cta-title` color `#fff` hardcodeado | L474 | No hay token `--app-on-primary-container`. Documentar excepción (CTA es dark) o añadir token. | 🟢 Baja |
| `.cta-box` bg `--primary-container` (#131b2e) alias sin app | L452-L459 | Crear token `--app-primary-container` y vincular. | 🟡 Baja |
| `.process-image-overlay` rgba hardcodeado | L446-L449 | Convertir a token o mantener como excepción de imagen. | 🟢 Baja |
| `.navbar-custom` box-shadow con rgba crudo | L248 | Usar `--app-topbar-shadow` (declarar token si no existe). | 🟢 Baja |

### 8.9 UserAvatar.vue
| Tarea | Línea | Acción | Prioridad |
|---|---|---|---|
| `background: #fff` hardcodeado | L34 | `--app-surface-container-lowest`. | 🟡 Baja |
| Box-shadow + border rgba crudos | L60-L63 | Usar tokens. | 🟢 Baja |

### 8.10 CallsListView / Project Views (Archivos vacíos actualmente)
Cuando se implementen:
- Seguir patrón de CallsListView (que ya usa AppCard y AppButton correctamente).
- Headers de página = `tw-text-2xl tw-font-bold tw-text-on-surface`.
- Iconos en header = `tw-w-12 tw-h-12 tw-rounded-2xl tw-bg-surface-container tw-text-primary` (igual que ProfileView). **Consistente**.

---

## 9. Normativas para Vistas Nuevas

Checklist obligatorio antes de marcar una vista como "lista":

### 9.1 Paleta y Colores
- [ ] **Cero** hex/rgba crudos en `<style scoped>`, `:style=""` o props. Todo por `--app-*` o Tailwind keys.
- [ ] Botones primarios de acción = `<AppButton variant="primary">`.
- [ ] FAB, CTA destacado, badges de rol = `<AppButton variant="accent">` / `--app-accent`.
- [ ] Texto secundario = `tw-text-on-surface-variant` (nunca `tw-text-outline`).
- [ ] Bordes = `tw-border-outline-variant` / `tw-border-outline` según jerarquía.

### 9.2 Tipografía
- [ ] `h1` página = `24px / 700 / on-surface`.
- [ ] `h2` card = `18px / 600 / on-surface`.
- [ ] Labels inputs = `12px / 500 / on-surface-variant`.
- [ ] Ningún font-size hardcodeado; usar Tailwind o tokens.

### 9.3 Layout y Espaciado
- [ ] Wrapper: máximo `tw-max-w-{valor}` consistente con la sección (dashboard: sin max; perfil: `max-w-[860px]`; landing: `container-max 1280px`).
- [ ] Grid: `tw-grid` + `tw-grid-cols-N` + breakpoint prefixes `sm:/md:/lg:`.
- [ ] Gap entre cards: `tw-gap-4` (16px) o `tw-gap-6` (24px).

### 9.4 Cards y Superficies
- [ ] Toda tarjeta = `<AppCard variant="X">` con el variant correcto.
- [ ] Padding por defecto de AppCard (`md`: `p-5 sm:p-6`) respetado; no overrides a menos que sea caso KPI.
- [ ] Divisores header/footer de card = border `slate-200/60` (AppCard lo gestiona).

### 9.5 Accesibilidad
- [ ] Focus rings en inputs = accent (4px).
- [ ] Botones con ícono = `aria-label` si no tienen texto visible.
- [ ] Imágenes decorativas = `alt=""`; informativas = `alt` descriptivo.
- [ ] Contraste WCAG AA (4.5:1 texto normal, 3:1 large). **Verificar**:
  - `on-surface-variant (#475569)` sobre `surface-container-lowest (#ffffff)` → contraste alto ✅.
  - `success (#15803d)` sobre `success-bg` → ok ✅.
  - `accent (#4b41e1)` sobre blanco → ok ✅.
  - `warning (#b45309)` sobre blanco → ok ✅.
  - `error (#ba1a1a)` sobre blanco → ok ✅.
  - `outline (#76777d)` sobre blanco → **2.97:1 (solo large text ok)** ⚠️. Nunca usar `--app-outline` para texto de body. OK solo para bordes.

---

## 10. Resumen de Prioridades y Siguientes Pasos

### Prioridad 🔴 ALTA (Bloqueando nuevas features)
1. Añadir tokens `--app-accent*` a main.css + Tailwind config.
2. Añadir variant `accent` a AppButton.vue.
3. Sustituir **todos** los botones locales (`af-btn-*`, `btn-hero-*`, `btn-primary-custom`, `btn-signup`, `btn-cta`, `btn-login`) por `<AppButton>`.
4. Corregir doble-color-primary: rail-link.active y FAB en AppLayout → `--app-accent`.
5. Eliminar estilos inline de error en RegisterView y usar ErrorAlert/clases.
6. Arreglar typo `##FDFDFE` y colores crudos en DashboardView recentProjects/activeCalls KPI data.

### Prioridad 🟡 MEDIA (Refinamiento del sistema)
7. Unificar input radius a `--app-input-radius` en Auth views.
8. Corregir surface-container fallbacks en tailwind.config.ts.
9. Tokenizar y aplicar `--app-accent-focus-ring` a focus states.
10. Añadir tipografía tokens `page-title`, `card-title`, `label`, `caption`.
11. Password strength meter → tokens estado.
12. Badge pill y feature-icon backgrounds HomeView → tokens accent.
13. DashboardHeroCard badges → accent tokens.

### Prioridad 🟢 BAJA (Housekeeping)
14. Migrar todos los rgba crudos en blobs/gradientes a variantes de accent con opacidad.
15. Añadir `--app-topbar-shadow`, `--app-primary-container`, `--app-on-primary-container`.
16. Eliminar clase `.glass-card` duplicada en HomeView.
17. Unificar UserAvatar fondos y bordes a tokens.

---

**Fin del documento.** Cualquier nueva implementación debe pasar este checklist antes de ser integrada.
