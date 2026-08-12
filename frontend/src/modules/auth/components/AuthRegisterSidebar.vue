<template>
  <div class="tw-col-span-1 lg:tw-col-span-5 tw-hidden lg:tw-flex tw-flex-col tw-justify-between sidebar-branding">
    <svg class="graph-bg" viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <!-- La red nace en la tarjeta y sube hacia la esquina vacía,
           en vez de puntos sueltos sin relación con el resto. -->
      <g stroke="rgba(247,244,236,0.16)" stroke-width="0.18" vector-effect="non-scaling-stroke">
        <line x1="14" y1="66" x2="31" y2="53" />
        <line x1="31" y1="53" x2="50" y2="40" />
        <line x1="31" y1="53" x2="23" y2="37" />
        <line x1="50" y1="40" x2="67" y2="21" />
        <line x1="23" y1="37" x2="30" y2="18" />
        <line x1="14" y1="66" x2="37" y2="80" />
        <line x1="37" y1="80" x2="57" y2="88" />
      </g>
      <g fill="var(--app-accent-brass, #B8863B)">
        <circle cx="31" cy="53" r="0.55" opacity="0.6" />
        <circle cx="50" cy="40" r="0.45" opacity="0.55" />
        <circle cx="23" cy="37" r="0.45" opacity="0.55" />
        <circle cx="67" cy="21" r="0.55" opacity="0.6" />
        <circle cx="30" cy="18" r="0.4" opacity="0.5" />
        <circle cx="37" cy="80" r="0.45" opacity="0.55" />
        <circle cx="57" cy="88" r="0.4" opacity="0.5" />
      </g>
    </svg>

    <div class="sidebar-content">
      <div class="tw-flex tw-items-center tw-gap-3 tw-mb-16">
        <div class="logo-badge">
          <span class="material-symbols-outlined notranslate" style="font-variation-settings: 'FILL' 1;">account_tree</span>
        </div>
        <span class="sidebar-brand-name">ProjectHub</span>
      </div>

      <p class="sidebar-eyebrow">Red de investigación &mdash; N.&ordm; 04</p>
      <h1 class="sidebar-title tw-mb-0">Eleva tu gestión académica al siguiente nivel.</h1>
      <p class="sidebar-desc tw-mt-4">Únete a la plataforma líder para la colaboración en investigación y proyectos
        universitarios de alto impacto.</p>
    </div>

    <div class="citation-card">
      <span class="citation-quote-mark">&ldquo;</span>
      <p class="testimonial-quote">
        ProjectHub transformó nuestra metodología de trabajo en red, permitiéndonos centralizar recursos de forma
        impecable.
      </p>
      <div class="tw-flex tw-items-center tw-gap-3">
        <div class="testimonial-avatar">
          <img
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3-e9ihrzVn3ULohcOKL4KvEz7DZLqzD601WzuRXHMYoJqHouMp1vqA5MN_mxQWM0Y9YX4675KEyKZnzqjM27sodKERztvnQLOROz1pSArKpGYP3atvmbAPwHfdA195IiftfjBRaOsCugE4F1kcsWHs8I4IzwKWibaBNg_G7vjeOY-ssa0m7LYR8JKPj22S9P2w_hox9gzcQhLBGvX3ONIU-P2coSImkcK00mR28RLOnBCBfk8wYKT7Q"
            alt="Dra. Elena Martínez">
        </div>
        <div>
          <p class="testimonial-name">Dra. Elena Martínez</p>
          <p class="testimonial-role">Investigadora Principal &middot; CSIC</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Sidebar: panel de tinta oscura en vez de blanco plano — el fondo
   pasa a formar parte del mensaje ("red de investigación"). */
.sidebar-branding {
  position: relative;
  background-color: var(--app-ink-900, #14243A);
  padding: 56px;
  overflow: hidden;
  height: 100%;
}

.graph-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.5;
  pointer-events: none;
}

.sidebar-content,
.citation-card {
  position: relative;
  z-index: 2;
}

.logo-badge {
  width: 40px;
  height: 40px;
  background-color: var(--app-accent-brass, #B8863B);
  border-radius: 0.625rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--app-ink-900, #14243A);
  box-shadow: 0 10px 20px -6px rgba(184, 134, 59, 0.5);
}

.sidebar-brand-name {
  font-family: var(--app-font-mono, 'IBM Plex Mono', monospace);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--app-paper, #F7F4EC);
}

.sidebar-eyebrow {
  font-family: var(--app-font-mono, 'IBM Plex Mono', monospace);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--app-accent-brass-light, #E8D2A6);
  margin: 0 0 18px 0;
}

/* Título: Fraunces sobre tinta, no azul saturado sobre blanco —
   el contraste ahora viene del panel oscuro, no del color de letra. */
.sidebar-title {
  font-family: var(--app-font-display, 'Fraunces', serif);
  font-size: 44px;
  font-weight: 500;
  letter-spacing: -0.01em;
  line-height: 1.14;
  color: var(--app-paper, #F7F4EC);
  max-width: 9.5em;
}

.sidebar-desc {
  font-family: var(--app-font-family, 'IBM Plex Sans', sans-serif);
  color: rgba(247, 244, 236, 0.68);
  max-width: 26em;
  line-height: 1.65;
  font-size: 15.5px;
}

/* Testimonio: ficha de cita "anclada" sobre el panel oscuro,
   con un clip de latón — el único acento cálido de la vista. */
.citation-card {
  background: var(--app-surface-container-lowest, #ffffff);
  border-radius: 4px;
  padding: 22px 22px 20px 26px;
  max-width: 23em;
  box-shadow: 0 20px 40px -18px rgba(0, 0, 0, 0.5);
}

.citation-card::before {
  content: "";
  position: absolute;
  top: -11px;
  left: 28px;
  width: 26px;
  height: 22px;
  background: var(--app-accent-brass, #B8863B);
  clip-path: polygon(0 0, 100% 0, 100% 100%, 50% 78%, 0 100%);
  transform: rotate(-3deg);
}

.testimonial-quote {
  font-family: var(--app-font-display, 'Fraunces', serif);
  font-style: italic;
  font-size: 15px;
  line-height: 1.55;
  color: var(--app-on-surface, #16232F);
  margin: 0 0 14px 0;
}

.testimonial-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
}

.testimonial-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.testimonial-name {
  font-family: var(--app-font-family, 'IBM Plex Sans', sans-serif);
  font-size: 13px;
  font-weight: 600;
  color: var(--app-on-surface, #16232F);
  margin-bottom: 0;
}

.testimonial-role {
  font-family: var(--app-font-mono, 'IBM Plex Mono', monospace);
  font-size: 10.5px;
  letter-spacing: 0.03em;
  color: var(--app-accent-brass, #B8863B);
  margin-bottom: 0;
}
</style>
