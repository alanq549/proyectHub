<template>
  <div class="col-span-1 lg:col-span-5 hidden lg:flex flex-col justify-between sidebar-branding">
    <div>
      <div class="flex items-center gap-3 mb-5">
        <div class="logo-badge">
          <span class="material-symbols-outlined notranslate" style="font-variation-settings: 'FILL' 1;">account_tree</span>
        </div>
        <span class="sidebar-brand-name">ProjectHub</span>
      </div>
      <h1 class="sidebar-title mb-0">Eleva tu gestión académica al siguiente nivel.</h1>
      <p class="sidebar-desc mt-4">Únete a la plataforma líder para la colaboración en investigación y proyectos
        universitarios de alto impacto.</p>
    </div>

    <div class="flex flex-col gap-4">
      <div class="flex items-center gap-3">
        <div class="testimonial-avatar">
          <img
            src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3-e9ihrzVn3ULohcOKL4KvEz7DZLqzD601WzuRXHMYoJqHouMp1vqA5MN_mxQWM0Y9YX4675KEyKZnzqjM27sodKERztvnQLOROz1pSArKpGYP3atvmbAPwHfdA195IiftfjBRaOsCugE4F1kcsWHs8I4IzwKWibaBNg_G7vjeOY-ssa0m7LYR8JKPj22S9P2w_hox9gzcQhLBGvX3ONIU-P2coSImkcK00mR28RLOnBCBfk8wYKT7Q"
            alt="Dra. Elena Martínez">

        </div>
        <div>

          <p class="testimonial-name">Dra. Elena Martínez</p>
          <p class="testimonial-role">Investigadora Principal, CSIC</p>
        </div>
      </div>
      <div class="glass-card testimonial-quote">
        "ProjectHub transformó nuestra metodología de trabajo en red, permitiéndonos centralizar recursos de forma
        impecable."
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Sidebar */
.sidebar-branding {
  background-color: var(--surface-container-lowest, #ffffff);
  padding: 48px;
  border-right: 1px solid rgba(198, 198, 205, 0.3);
  height: 100%;
}

.logo-badge {
  width: 40px;
  height: 40px;
  background-color: var(--primary, #000000);
  border-radius: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.sidebar-brand-name {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--primary, #000000);
}

.sidebar-title {
  font-size: 48px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  color: var(--primary, #000000);
  max-width: 28rem;
}

.sidebar-desc {
  color: var(--on-surface-variant, #45464d);
  max-width: 24rem;
  line-height: 1.6;
}

.testimonial-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.testimonial-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.testimonial-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--on-surface, #191c1e);
  margin-bottom: 0;
}

.testimonial-role {
  font-size: 12px;
  color: var(--on-surface-variant, #45464d);
  margin-bottom: 0;
}

.testimonial-quote {
  padding: 12px;
  border-radius: 0.75rem;
  font-size: 12px;
  color: var(--on-surface-variant, #45464d);
  font-style: italic;
}
</style>