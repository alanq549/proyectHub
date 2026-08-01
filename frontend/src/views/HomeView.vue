<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-md navbar-custom">
      <div class="container-max d-flex justify-content-between align-items-center w-100">
        <div class="d-flex align-items-center gap-5">
          <span class="brand-text">ProjectHub</span>
          <div class="d-none d-md-flex gap-4">
            <a class="nav-link-custom" href="#">Proyectos</a>
            <a class="nav-link-custom" href="#">Investigación</a>
            <a class="nav-link-custom" href="#">Recursos</a>
          </div>
        </div>
        <div class="d-flex align-items-center gap-3">
          <button class="btn-login" @click="router.push({ name: 'login' })">Iniciar Sesión</button>
          <button class="btn-signup" @click="router.push({ name: 'register' })">Registrarse</button>
        </div>
      </div>
    </nav>

    <main>
      <!-- Hero -->
      <section class="hero-section hero-gradient" :style="heroGradientStyle">
        <div class="container-max d-flex flex-column align-items-center text-center">
          <div class="badge-pill mb-3">
            <span class="material-symbols-outlined" style="font-size:18px;">verified</span>
            <span>Nueva versión académica 2.0</span>
          </div>
          <h1 class="display-title mb-3">Gestión académica de alto nivel</h1>
          <p class="hero-desc mb-4">Optimiza la administración de proyectos de investigación, convocatorias y documentación con una plataforma diseñada para el rigor académico y la eficiencia operativa.</p>

          <div class="d-flex flex-wrap justify-content-center gap-3">
            <button class="btn-hero-primary" @click="router.push({ name: 'register' })">
              Comenzar ahora
            </button>
            <button class="btn-hero-secondary">Ver demo</button>
          </div>

          <!-- Hero Image -->
          <div class="hero-image-wrap w-100">
            <div class="hero-image-glow"></div>
            <div class="hero-image-frame glass-card">
              <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuCVhzXjOgaz6erhGe0mhEzs1bXxiig37koEP9MFiH9Og8Ua9CkaM_ryHPe37Ma-aZOFH3x9o4C2SPO9_mCJ4tiJBmE8OU_6Nz972KRUvsYbOer5ReMZl_sO1OgSzEAVUBJMrkz0BaJyiwvqkVK8JZN2XC97yHD7MbN8NTNGQ4y1WVc8Ik-Q8DjW9wG_jw2RMYohLOcMp7Lm6IyVvFS1FsIUzQZZhSgAO64JRovP_zR3hV1UZT4qHRbOYg" alt="Dashboard académico ProjectHub">
            </div>
          </div>
        </div>
      </section>

      <!-- Features -->
      <section class="section-padded" style="background-color: var(--surface);">
        <div class="container-max">
          <div class="text-center mb-5">
            <h2 class="section-title mb-2">Herramientas diseñadas para la excelencia</h2>
            <p class="text-on-surface-variant" style="color: var(--on-surface-variant);">Tecnología de vanguardia para instituciones que no comprometen la calidad.</p>
          </div>

          <div class="row g-4">
            <div class="col-12 col-md-6 col-lg-3">
              <div class="glass-card feature-card">
                <div class="feature-icon"><span class="material-symbols-outlined">account_tree</span></div>
                <h3 class="feature-title">Gestión de Proyectos</h3>
                <p class="feature-desc">Organiza flujos de trabajo complejos con cronogramas dinámicos y asignación de hitos.</p>
              </div>
            </div>
            <div class="col-12 col-md-6 col-lg-3">
              <div class="glass-card feature-card">
                <div class="feature-icon"><span class="material-symbols-outlined">campaign</span></div>
                <h3 class="feature-title">Convocatorias</h3>
                <p class="feature-desc">Publica y gestiona convocatorias de investigación con procesos de evaluación automatizados.</p>
              </div>
            </div>
            <div class="col-12 col-md-6 col-lg-3">
              <div class="glass-card feature-card">
                <div class="feature-icon"><span class="material-symbols-outlined">encrypted</span></div>
                <h3 class="feature-title">Documentación Segura</h3>
                <p class="feature-desc">Repositorio cifrado para archivos sensibles con control de versiones y firmas digitales.</p>
              </div>
            </div>
            <div class="col-12 col-md-6 col-lg-3">
              <div class="glass-card feature-card">
                <div class="feature-icon"><span class="material-symbols-outlined">monitoring</span></div>
                <h3 class="feature-title">Métricas en Tiempo Real</h3>
                <p class="feature-desc">Analítica avanzada para monitorizar el impacto y progreso de cada iniciativa académica.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Process -->
      <section class="section-padded">
        <div class="container-max">
          <div class="row align-items-center g-5">
            <div class="col-12 col-lg-6">
              <h2 class="section-title mb-3">Metodología simplificada</h2>
              <p class="mb-4" style="color: var(--on-surface-variant);">Nuestra plataforma elimina la fricción administrativa para que los investigadores puedan centrarse en lo que realmente importa: generar conocimiento.</p>

              <div class="d-flex flex-column gap-4">
                <div class="d-flex gap-3">
                  <div class="step-number">1</div>
                  <div>
                    <h4 class="step-title">Registro</h4>
                    <p class="step-desc mb-0">Inicia tu perfil institucional con validación de credenciales académicas en minutos.</p>
                  </div>
                </div>
                <div class="d-flex gap-3">
                  <div class="step-number">2</div>
                  <div>
                    <h4 class="step-title">Creación</h4>
                    <p class="step-desc mb-0">Configura proyectos, establece metas y carga los recursos necesarios de forma estructurada.</p>
                  </div>
                </div>
                <div class="d-flex gap-3">
                  <div class="step-number">3</div>
                  <div>
                    <h4 class="step-title">Gestión</h4>
                    <p class="step-desc mb-0">Monitorea cada fase, colabora con pares y genera reportes automáticos de cumplimiento.</p>
                  </div>
                </div>
              </div>
            </div>

            <div class="col-12 col-lg-6">
              <div class="process-image-wrap">
                <img src="https://lh3.googleusercontent.com/aida-public/AB6AXuBtMIMexHhRzdMmMuF3-0pEdUuPRN9swOxsz42JWJhOfqYMhJhQZ5726O9jQerBdS0_n_4-9lW_3igNxD-7S-jp78hEYDjBCgfDJ_VGybTtQm8fDm_IecIC3eVD9JDefbzGEkObTjLV4mhGmHJzwS58I2hNDje3Ixj7W-1NRwvfulGUv9703s8-uos_c_HMmOhTkR6AOH58FPJ6_8-OXlF8ZgIeXnVZGCegeO4vjWFGEtthWk9osgw9Tw" alt="Espacio de trabajo académico organizado">
                <div class="process-image-overlay"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- CTA -->
      <section class="section-padded">
        <div class="container-max">
          <div class="cta-box">
            <div class="cta-blob-1"></div>
            <div class="cta-blob-2"></div>
            <div class="position-relative" style="z-index:1;">
              <h2 class="cta-title mb-3">¿Listo para elevar tus estándares?</h2>
              <p class="cta-desc mb-4">Únete a cientos de instituciones que ya transformaron su gestión académica con ProjectHub.</p>
              <button class="btn-cta">Empezar gratuitamente</button>
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer class="footer-custom">
      <div class="container-max">
        <div class="row g-4">
          <div class="col-12 col-md-3">
            <span class="brand-text d-block mb-2">ProjectHub</span>
            <p class="footer-caption mb-0">© 2024 ProjectHub. Gestión académica de alto nivel.</p>
          </div>
          <div class="col-6 col-md-3">
            <h5 class="footer-heading">Producto</h5>
            <ul class="list-unstyled d-flex flex-column gap-2 mb-0">
              <li><a class="footer-link" href="#">Metodología</a></li>
              <li><a class="footer-link" href="#">Recursos</a></li>
              <li><a class="footer-link" href="#">Soporte</a></li>
            </ul>
          </div>
          <div class="col-6 col-md-3">
            <h5 class="footer-heading">Legal</h5>
            <ul class="list-unstyled d-flex flex-column gap-2 mb-0">
              <li><a class="footer-link" href="#">Privacidad</a></li>
              <li><a class="footer-link" href="#">Términos</a></li>
            </ul>
          </div>
          <div class="col-6 col-md-3">
            <h5 class="footer-heading">Contacto</h5>
            <ul class="list-unstyled d-flex flex-column gap-2 mb-0">
              <li><a class="footer-link" href="#">Contacto</a></li>
              <li><a class="footer-link" href="#">Ayuda</a></li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const heroGradientStyle = ref({});

const handleMouseMove = (e: MouseEvent) => {
  const x = e.clientX / window.innerWidth;
  const y = e.clientY / window.innerHeight;
  heroGradientStyle.value = {
    background: `radial-gradient(circle at ${80 - (x * 5)}% ${20 + (y * 5)}%, rgba(75, 65, 225, 0.08) 0%, transparent 40%),
                 radial-gradient(circle at ${20 + (x * 5)}% ${80 - (y * 5)}%, rgba(75, 65, 225, 0.05) 0%, transparent 40%)`,
  };
};

onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove);
});

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove);
});
</script>

<style scoped>
/* Variables will be handled by global CSS or a theme */

.container-max{
  max-width: 1280px;
  margin-left: auto;
  margin-right: auto;
  padding-left: 64px;
  padding-right: 64px;
}
@media (max-width: 767.98px){
  .container-max{ padding-left: 24px; padding-right: 24px; }
}

.material-symbols-outlined{
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(226, 232, 240, 0.5);
  transition: transform .3s ease, box-shadow .3s ease;
}

/* Navbar */
.navbar-custom{
  background-color: rgba(255,255,255,0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  position: sticky;
  top: 0;
  z-index: 1030;
  height: 80px;
  box-shadow: 0px 10px 30px rgba(79,70,229,0.04);
}
.brand-text{
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--primary, #000000);
}
.nav-link-custom{
  color: var(--on-surface-variant, #45464d);
  text-decoration: none;
  transition: color .15s ease;
  font-size: 16px;
}
.nav-link-custom:hover{ color: var(--primary, #000000); }

.btn-login{
  background: none;
  border: none;
  color: var(--primary, #000000);
  font-size: 14px;
  font-weight: 500;
  padding: 0.5rem 1.5rem;
}
.btn-signup{
  background-color: var(--primary, #000000);
  color: var(--on-primary, #ffffff);
  border-radius: 0.75rem;
  font-size: 14px;
  font-weight: 500;
  padding: 0.5rem 1.5rem;
  box-shadow: 0 10px 15px -3px rgba(0,0,0,0.08);
  border: none;
  transition: opacity .15s ease, transform .1s ease;
}
.btn-signup:hover{ opacity: 0.9; color: var(--on-primary, #ffffff); }
.btn-signup:active{ transform: scale(0.95); }

/* Hero */
.hero-section{
  position: relative;
  overflow: hidden;
  padding-top: 48px;
  padding-bottom: 64px;
}
.badge-pill{
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.35rem 1rem;
  border-radius: 9999px;
  background-color: rgba(226,223,255,0.3);
  color: var(--on-secondary-fixed-variant, #3323cc);
  font-size: 14px;
  font-weight: 500;
}
.display-title{
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.1;
  color: var(--primary, #000000);
  max-width: 800px;
}
@media (min-width: 768px){
  .display-title{ font-size: 48px; }
}
.hero-desc{
  color: var(--on-surface-variant, #45464d);
  font-size: 16px;
  max-width: 640px;
  line-height: 1.6;
}

.btn-hero-primary{
  padding: 1rem 2rem;
  background-color: var(--primary, #000000);
  color: var(--on-primary, #ffffff);
  border-radius: 0.75rem;
  font-size: 20px;
  font-weight: 600;
  border: none;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.15);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: opacity .15s ease, transform .1s ease;
}
.btn-hero-primary:hover{ opacity: 0.95; color: var(--on-primary, #ffffff); }
.btn-hero-primary:active{ transform: scale(0.95); }

.btn-hero-secondary{
  padding: 1rem 2rem;
  background-color: var(--surface-container-lowest, #ffffff);
  color: var(--primary, #000000);
  border-radius: 0.75rem;
  font-size: 20px;
  font-weight: 600;
  border: 1px solid var(--outline-variant, #c6c6cd);
  transition: background-color .15s ease, transform .1s ease;
}
.btn-hero-secondary:hover{ background-color: var(--surface-container, #eceef0); color: var(--primary, #000000); }
.btn-hero-secondary:active{ transform: scale(0.95); }

.hero-image-wrap{
  position: relative;
  max-width: 64rem;
  margin: 64px auto 0;
}
.hero-image-glow{
  position: absolute;
  inset: -4px;
  background: linear-gradient(to right, rgba(75,65,225,0.20), rgba(0,0,0,0.10));
  border-radius: 1rem;
  filter: blur(20px);
  opacity: 0.25;
}
.hero-image-frame{
  position: relative;
  border-radius: 1rem;
  overflow: hidden;
  border: 1px solid var(--outline-variant, #c6c6cd);
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
}
.hero-image-frame img{
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
}

/* Features */
.section-padded{ padding-top: 64px; padding-bottom: 64px; }
.section-title{
  font-size: 32px;
  font-weight: 600;
  letter-spacing: -0.015em;
  color: var(--primary, #000000);
}
.feature-card{
  padding: 24px;
  border-radius: 0.75rem;
  height: 100%;
}
.feature-card:hover{
  transform: translateY(-4px);
  box-shadow: 0 20px 25px -5px rgba(0,0,0,0.10);
}
.feature-icon{
  width: 48px; height: 48px;
  border-radius: 0.5rem;
  background-color: var(--primary-fixed, #dae2fd);
  color: var(--primary, #000000);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  transition: background-color .2s ease, color .2s ease;
}
.feature-card:hover .feature-icon{
  background-color: var(--primary, #000000);
  color: var(--on-primary, #ffffff);
}
.feature-title{
  font-size: 20px;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.feature-desc{
  color: var(--on-surface-variant, #45464d);
  font-size: 14px;
}

/* Process */
.step-number{
  flex-shrink: 0;
  width: 40px; height: 40px;
  border-radius: 50%;
  background-color: var(--primary, #000000);
  color: var(--on-primary, #ffffff);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}
.step-title{ font-size: 20px; font-weight: 600; }
.step-desc{ color: var(--on-surface-variant, #45464d); font-size: 14px; }

.process-image-wrap{
  position: relative;
  aspect-ratio: 1/1;
  border-radius: 1.5rem;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
}
.process-image-wrap img{
  width: 100%; height: 100%; object-fit: cover;
}
.process-image-overlay{
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(19,27,46,0.20), transparent);
}

/* CTA */
.cta-box{
  background-color: var(--primary-container, #131b2e);
  border-radius: 2rem;
  padding: 64px;
  text-align: center;
  position: relative;
  overflow: hidden;
}
.cta-blob-1{
  position: absolute; top: 0; right: 0;
  width: 16rem; height: 16rem;
  background: rgba(75,65,225,0.10);
  filter: blur(100px);
  margin-right: -8rem; margin-top: -8rem;
}
.cta-blob-2{
  position: absolute; bottom: 0; left: 0;
  width: 16rem; height: 16rem;
  background: rgba(218,226,253,0.05);
  filter: blur(100px);
  margin-left: -8rem; margin-bottom: -8rem;
}
.cta-title{
  color: #fff;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
}
@media (min-width: 768px){
  .cta-title{ font-size: 48px; }
}
.cta-desc{
  color: var(--on-primary-container, #7c839b);
  font-size: 16px;
  max-width: 36rem;
  margin: 0 auto;
}
.btn-cta{
  padding: 1.25rem 2.5rem;
  background-color: var(--secondary, #4b41e1);
  color: var(--on-secondary, #ffffff);
  border-radius: 1rem;
  font-size: 20px;
  font-weight: 600;
  border: none;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
  transition: transform .2s ease;
}
.btn-cta:hover{ transform: scale(1.05); color: var(--on-secondary, #ffffff); }

/* Footer */
.footer-custom{
  background-color: var(--surface-container, #eceef0);
  border-top: 1px solid var(--outline-variant, #c6c6cd);
  padding-top: 64px;
  padding-bottom: 64px;
  margin-top: 64px;
}
.footer-heading{
  font-size: 14px;
  color: var(--primary, #000000);
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.footer-link{
  color: var(--on-surface-variant, #45464d);
  text-decoration: none;
  font-size: 14px;
}
.footer-link:hover{ color: var(--primary, #000000); }
.footer-caption{
  color: var(--on-surface-variant, #45464d);
  font-size: 12px;
}
</style>