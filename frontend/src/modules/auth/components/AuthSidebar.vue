<template>
  <div class="col-span-1 md:col-span-1 hidden md:flex flex-col justify-between left-panel">
    <div class="left-panel-bg"></div>

    <div class="relative" style="z-index:1;">
      <div class="flex items-center gap-2 mb-5">
        <span class="brand-name">
          ProjectHub
        </span>
      </div>
      <h1 class="headline mb-2">
        Garantizando la excelencia académica.
      </h1>
      <p class="subhead">
        La plataforma de gestión de proyectos diseñada para investigadores y académicos de alto nivel.
      </p>
    </div>

    <div class="relative mt-auto" style="z-index:1;">
      <div class="avatar-stack flex mb-3">
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
      <p class="caption-text mb-0">
        Únete a más de 5,000 investigadores hoy.
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Left panel */
.left-panel {
  background-color: var(--primary-container, #131b2e);
    padding: 64px;
    position: relative;
    overflow: hidden;
    min-height: 100%;
}

.left-panel-bg {
  position: absolute;
  inset: 0;
  opacity: 0.20;
  background-image: url('https://lh3.googleusercontent.com/aida-public/AB6AXuCH4uqecPcMA5KQArhVFrLB38slunRmcO372Ot3ruLesQFNdTmzhyifrVeUtz_SNt1BQCYyaRDmm14cQVPRB6bUEah7GMyCcQ5lHmVPiO3fCGo2DlG2ePA9-Joc3fOejmH060ryxUlGYz2sxpA1u_bfWrIcEi4qJRV4xz0h-EJ5QiBn_t_WwmymbAwkj7QvtgtOd2Qn1mLAbKkwNvezqfokmFLQK5ijFltQ9jsEeI-q_ThCLHF5I6WCSw');
   background-size: cover;
  background-position: center;
}

.brand-name {
  color: var(--secondary-fixed, #e2dfff);
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
}

.headline {
  color: #fff;
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -0.015em;
  line-height: 1.2;
}

.subhead {
  color: var(--on-primary-container, #7c839b);
  font-size: 16px;
  line-height: 1.6;
  max-width: 24rem;
}

.avatar-stack img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid var(--primary-container, #131b2e);
  object-fit: cover;
  margin-left: -12px;
}

.avatar-stack img:first-child {
  margin-left: 0;
}

.caption-text {
  color: var(--on-primary-container, #7c839b);
  font-size: 12px;
  letter-spacing: 0.03em;
}
</style>