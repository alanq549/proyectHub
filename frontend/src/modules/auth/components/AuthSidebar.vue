<template>
  <div class="tw-col-span-1 md:tw-col-span-1 tw-hidden md:tw-flex tw-flex-col tw-justify-between left-panel">
    <svg class="graph-bg" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
      <!-- La red termina en el grupo de avatares: los nodos son
           investigadores reales, no puntos decorativos sueltos. -->
      <g stroke="rgba(247,244,236,0.16)" stroke-width="0.18" vector-effect="non-scaling-stroke">
        <line x1="16" y1="82" x2="33" y2="68" />
        <line x1="33" y1="68" x2="52" y2="54" />
        <line x1="33" y1="68" x2="25" y2="50" />
        <line x1="52" y1="54" x2="70" y2="34" />
        <line x1="52" y1="54" x2="66" y2="66" />
        <line x1="70" y1="34" x2="62" y2="16" />
        <line x1="70" y1="34" x2="86" y2="24" />
      </g>
      <g fill="var(--app-accent-brass, #B8863B)">
        <circle cx="33" cy="68" r="0.5" opacity="0.55" />
        <circle cx="52" cy="54" r="0.45" opacity="0.5" />
        <circle cx="25" cy="50" r="0.4" opacity="0.5" />
        <circle cx="70" cy="34" r="0.55" opacity="0.6" />
        <circle cx="66" cy="66" r="0.4" opacity="0.45" />
        <circle cx="62" cy="16" r="0.45" opacity="0.5" />
        <circle cx="86" cy="24" r="0.4" opacity="0.45" />
      </g>
    </svg>

    <div class="tw-relative" style="z-index:1;">
      <div class="tw-flex tw-items-center tw-gap-3 tw-mb-16">
        <div class="logo-badge">
          <span class="material-symbols-outlined notranslate" style="font-variation-settings: 'FILL' 1;">account_tree</span>
        </div>
        <span class="brand-name">ProjectHub</span>
      </div>

      <p class="eyebrow-text">Acceso seguro &mdash; N.&ordm; 01</p>
      <h1 class="headline tw-mb-2">
        Garantizando la excelencia académica.
      </h1>
      <p class="subhead">
        La plataforma de gestión de proyectos diseñada para investigadores y académicos de alto nivel.
      </p>
    </div>

    <div class="tw-relative tw-mt-auto" style="z-index:1;">
      <div class="avatar-stack tw-flex tw-mb-3">
        <img
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuBAXfhEfWfTaKVGvIHAs7_UDZPt_wA6IPGlRBO7NrRs4koBf_dJE6JtECZ7tKnjBM9sNwMrcfOaemF3p03L4hipB9meE5AYCGbOOCNWmU5oSI82Y2O23hVfazOjjNN3LQeIanmR-tDfWIrhGNdCxdpiQ8Z39L-RzCG4nBHlu_FBSdwMSo5wl4mZJZKDCf0hXBSTDfWRagOJ1rc_KuogekkJnjuW20F-FhDnCC0y4TeXAcNvc00_B3rMKw"
          alt="Investigadora">
        <img
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuCnjSF8TUpVqpHgmNcdbDV61rrrSaafWJRY9Y1nqj9rRibKxZi1Amco87hb8FOX0ND7cjan-i6GqL6UCXSKTTG5SOb5pcd3Et7e_AGkN3dAHsoi3pqLfMI8asMQ1FkBPgDXpM6hWRc5EYLFiEmUmUaDzH0T5WZouzeGIldX5wKeXnv0LGFR-MiQNwBu7V89q7nyEREH03R3mcHQWe9b4_Rab3cdCftNvwaSy4wZFy3x4vKe3x6oJMiJ5g"
          alt="Académico">
        <img
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3faTjVGZj6d3l8Ff-cp3IqLWD3avOw7p02pfbdELvnXHw1IJNMinwm-iTgPDvi9cEtnFfdCo8GvSwwztV66vPIPxfFgLTIWm_DkulZBfF-QLA8_SjLPBjam2RKv3ug-cXduOve63CKZdkC7voCnQ3WubJ7jVvDOYS7KIvQPW_nwQTWPpFszvkPTFepRz7tLwpGOstLvd-YfHH4WyqCQ5lT9sXgLUYRLJtvYzJ0MKQdwEeu3ueHsvT4w"
          alt="Investigador en presentación">
      </div>
      <p class="caption-text tw-mb-0">
        Únete a más de 5,000 investigadores hoy.
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Left panel — mismo lenguaje visual que el registro: tinta oscura,
   red de nodos y acento latón, en vez del teal + captura de pantalla. */
.left-panel {
  background-color: var(--app-ink-900, #14243A);
  padding: 64px;
  position: relative;
  overflow: hidden;
  min-height: 100%;
}

.graph-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  opacity: 0.5;
  pointer-events: none;
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

.brand-name {
  font-family: var(--app-font-mono, 'IBM Plex Mono', monospace);
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--app-paper, #F7F4EC);
}

.eyebrow-text {
  font-family: var(--app-font-mono, 'IBM Plex Mono', monospace);
  font-size: 12px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--app-accent-brass-light, #E8D2A6);
  margin: 0 0 18px 0;
}

.headline {
  font-family: var(--app-font-display, 'Fraunces', serif);
  color: var(--app-paper, #F7F4EC);
  font-size: 36px;
  font-weight: 500;
  letter-spacing: -0.01em;
  line-height: 1.16;
  max-width: 11em;
}

.subhead {
  font-family: var(--app-font-family, 'IBM Plex Sans', sans-serif);
  color: rgba(247, 244, 236, 0.68);
  font-size: 15.5px;
  line-height: 1.65;
  max-width: 24rem;
}

.avatar-stack img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--app-ink-900, #14243A);
  object-fit: cover;
  margin-left: -12px;
}

.avatar-stack img:first-child {
  margin-left: 0;
}

.caption-text {
  font-family: var(--app-font-mono, 'IBM Plex Mono', monospace);
  color: var(--app-accent-brass-light, #E8D2A6);
  font-size: 11.5px;
  letter-spacing: 0.05em;
}
</style>
