<template>
  <div
    class="login-wrapper min-vh-100 d-flex align-items-center justify-content-center p-3 p-md-0 position-relative overflow-hidden">

    <div class="bg-layer">
      <div class="blob-1"></div>
      <div class="blob-2"></div>
    </div>

    <main class="auth-card">

      <div class="row g-0">

        <!-- LEFT PANEL -->
        <div class="col-md-6 d-none d-md-flex flex-column justify-content-between left-panel">

          <div class="left-panel-bg"></div>

          <div class="position-relative" style="z-index:1;">

            <div class="d-flex align-items-center gap-2 mb-5">
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


          <div class="position-relative mt-auto" style="z-index:1;">

            <div class="avatar-stack d-flex mb-3">

              <img
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3-e9ihrzVn3ULohcOKL4KvEz7DZLqzD601WzuRXHMYoJqHouMp1vqA5MN_mxQWM0Y9YX4675KEyKZnzqjM27sodKERztvnQLOROz1pSArKpGYP3atvmbAPwHfdA195IiftfjBRaOsCugE4F1kcsWHs8I4IzwKWibaBNg_G7vjeOY-ssa0m7LYR8JKPj22S9P2w_hox9gzcQhLBGvX3ONIU-P2coSImkcK00mR28RLOnBCBfk8wYKT7Q"
                alt="Investigadora">

              <img
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuCnjSF8TUpVqpHgmNcdbDV61rrrSaafWJRY9Y1nqj9rRibKxZi1Amco87hb8FOX0ND7cjan-i6GqL6UCXSKTTG5SOb5pcd3Et7e_AGkN3dAHsoi3pqLfMI8asMQ1FkBPgDXpM6hWRc5EYLFiEmUmUaDzH0T5WZouzeGIldX5wKeXnv0LGFR-MiQNwBu7V89q7nyEREH03R3mcHQWe9b4_Rab3cdCftNvwaSy4wZFy3x4vKe3x6oJMiJ5g"
                alt="Académico">

              <img
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3faTjVGZj6d3l8Ff-cp3IqLWD3avOw7p02pfbdELvnXHw1IJNMinwm-iTgPDvi9cEtnFfdCo8GvSwwztV66vPIPxfFgLTIWm_DkulZBfF-QLA8_SjLPBjam2RKv3ug-cXduOve63CKZdkC7voCnQ3WubJ7jVvDOYS7KIvQPW_nwQTWPpFszvkPTFepRz7tLwpGOstLvd-YfHH4WyqCQ5lT9sXgLUYRLJtvYzJ0MKQdwEeu3ueHsvT4w"
                alt="Investigador">

            </div>


            <p class="caption-text mb-0">
              Únete a más de 5,000 investigadores hoy.
            </p>

          </div>

        </div>




        <!-- RIGHT PANEL -->

        <div class="col-12 col-md-6 right-panel">


          <div class="mx-auto" style="max-width:24rem;">


            <!-- HEADER MOBILE -->
            <div class="d-md-none d-flex justify-content-between align-items-center mb-5">

              <span class="brand-name" style="color:var(--primary)">
                ProjectHub
              </span>


              <button class="btn-back-home" @click="router.push({ name: 'home' })">

                <span class="material-symbols-outlined">
                  arrow_back
                </span>

                Inicio

              </button>

            </div>



            <!-- DESKTOP BACK BUTTON -->

            <div class="d-none d-md-block mb-4">

              <button class="btn-back-home" @click="router.push({ name: 'home' })">
                Volver al inicio
              </button>
            </div>
            <div class="mb-5">
              <h2 class="form-title mb-2">
                Bienvenido de nuevo
              </h2>
              
              <p class="form-subtitle mb-0">
                Ingresa tus credenciales para acceder.
              </p>

            </div>





            <!-- ERROR -->

            <div v-if="errorMessage" class="error-alert">

              <span class="material-symbols-outlined">
                error
              </span>


              <p>
                Credenciales incorrectas. Por favor, intenta de nuevo.
              </p>


            </div>






            <form @submit.prevent="handleLogin" id="login-form">


              <!-- EMAIL -->

              <div class="mb-4">

                <label class="form-label form-label-custom">
                  Correo electrónico
                </label>


                <div class="input-icon-wrap">

                  <span class="material-symbols-outlined">
                    mail
                  </span>


                  <input type="email" class="form-control form-control-custom" v-model="email"
                    placeholder="nombre@institucion.edu" required>

                </div>


              </div>





              <!-- PASSWORD -->

              <div class="mb-4">


                <div class="d-flex justify-content-between align-items-center mb-2">


                  <label class="form-label form-label-custom mb-0">
                    Contraseña
                  </label>


                  <a href="#" class="link-secondary fw-semibold">
                    ¿Olvidaste tu contraseña?
                  </a>


                </div>



                <div class="input-icon-wrap">


                  <span class="material-symbols-outlined">
                    lock
                  </span>



                  <input :type="showPassword ? 'text' : 'password'" class="form-control form-control-custom has-toggle"
                    v-model="password" placeholder="••••••••" required>



                  <button type="button" class="toggle-icon" @click="togglePassword">

                    <span class="material-symbols-outlined">
                      {{ showPassword ? 'visibility_off' : 'visibility' }}
                    </span>

                  </button>



                </div>


              </div>






              <button class="btn-primary-custom" :disabled="isLoading">


                <span v-if="!isLoading">
                  Iniciar Sesión
                </span>


                <div v-else class="spinner-border spinner-border-sm" style="color:white"></div>


              </button>



            </form>





            <div class="text-center mt-4">


              <p class="form-subtitle mb-0">

                ¿No tienes una cuenta?


                <a href="#" class="link-secondary fw-semibold" @click.prevent="router.push({ name: 'register' })">
                  Crear cuenta
                </a>


              </p>


            </div>





            <!-- SOCIAL LOGIN -->

            <div class="d-flex align-items-center gap-3 my-4">

              <div class="divider-line"></div>

              <span class="divider-text">
                O CONTINUAR CON
              </span>

              <div class="divider-line"></div>

            </div>



            <div class="row g-3">

              <div class="col-6">
                <button class="sso-btn">
                  Google
                </button>
              </div>


              <div class="col-6">

                <button class="sso-btn">

                  <span class="material-symbols-outlined">
                    school
                  </span>

                  Institucional

                </button>

              </div>


            </div>



          </div>


        </div>


      </div>


    </main>



    <div class="secure-badge">

      <span class="material-symbols-outlined">
        verified_user
      </span>


      <span class="txt">
        Encriptación de nivel bancario
      </span>


    </div>


  </div>

</template>

<script setup lang="ts">

import { ref } from 'vue'
import { useRouter } from 'vue-router'


const router = useRouter()


const email = ref('')
const password = ref('')

const showPassword = ref(false)

const isLoading = ref(false)

const errorMessage = ref(false)



const togglePassword = () => {

  showPassword.value = !showPassword.value

}




const handleLogin = () => {


  isLoading.value = true

  errorMessage.value = false



  setTimeout(() => {


    isLoading.value = false


    // temporal mientras no existe backend
    errorMessage.value = true



    const form =
      document.getElementById('login-form')


    if (form) {

      form.classList.add('animate-shake')


      setTimeout(() => {

        form.classList.remove('animate-shake')

      }, 500)

    }



  }, 2000)


}


</script>

<style scoped>
/* Variables moved to global CSS or handled by a theme */
/* .login-wrapper background color */
.login-wrapper {
  background-color: var(--background, #f7f9fb);
}

/* Background atmospheric layer */
.bg-layer {
  position: fixed;
  inset: 0;
  z-index: 0;
  background-color: var(--surface-bright, #f7f9fb);
}

.bg-layer::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at top right, rgba(75, 65, 225, 0.05) 0%, transparent 40%),
    radial-gradient(circle at bottom left, rgba(172, 237, 255, 0.05) 0%, transparent 40%);
}

.blob-1 {
  position: absolute;
  top: -10%;
  right: -5%;
  width: 40%;
  height: 40%;
  background: rgba(75, 65, 225, 0.05);
  border-radius: 50%;
  filter: blur(120px);
}

.blob-2 {
  position: absolute;
  bottom: -10%;
  left: -5%;
  width: 30%;
  height: 30%;
  background: rgba(76, 215, 246, 0.10);
  border-radius: 50%;
  filter: blur(100px);
}

.auth-card {
  position: relative;
  z-index: 10;
  max-width: 1100px;
  width: 100%;
  border-radius: 2rem;
  overflow: hidden;
  box-shadow: 0px 40px 100px rgba(0, 0, 0, 0.06);
  background: #fff;
}

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

/* Right panel (form) */
.right-panel {
  background-color: var(--surface-container-lowest, #ffffff);
  padding: 64px;
}

.btn-back-home {
  border: none;
  background: transparent;
  color: var(--secondary, #4b41e1);
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: .35rem;
  padding: 0;
}

.btn-back-home:hover {
  text-decoration: underline;
}


@media (max-width: 767.98px) {
  .right-panel {
    padding: 2rem;
  }
}

.form-title {
  color: var(--on-surface, #191c1e);
  font-weight: 600;
  letter-spacing: -0.01em;
  font-size: 24px;
}

@media (min-width: 768px) {
  .form-title {
    font-size: 32px;
    letter-spacing: -0.015em;
  }
}

.form-subtitle {
  color: var(--on-surface-variant, #45464d);
  font-size: 16px;
}

.form-label-custom {
  color: var(--on-surface-variant, #45464d);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.02em;
}

.input-icon-wrap {
  position: relative;
}

.input-icon-wrap .material-symbols-outlined {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--outline, #76777d);
  pointer-events: none;
}

.input-icon-wrap .toggle-icon {
  position: absolute;
  right: 16px;
  left: auto;
  top: 50%;
  transform: translateY(-50%);
  color: var(--outline-variant, #c6c6cd);
  cursor: pointer;
  pointer-events: auto;
  background: none;
  border: none;
}

.form-control-custom {
  height: 48px;
  padding-left: 48px;
  padding-right: 16px;
  background-color: var(--surface, #f7f9fb);
  border: 1px solid var(--outline-variant, #c6c6cd);
  border-radius: 0.75rem;
  color: var(--on-surface, #191c1e);
  font-size: 16px;
}

.form-control-custom.has-toggle {
  padding-right: 48px;
}

.form-control-custom:focus {
  outline: none;
  box-shadow: 0 0 0 4px rgba(75, 65, 225, 0.10);
  border-color: var(--secondary, #4b41e1);
}

.link-secondary {
  color: var(--secondary, #4b41e1);
  font-size: 14px;
  text-decoration: none;
}

.link-secondary:hover {
  text-decoration: underline;
}

.btn-primary-custom {
  height: 52px;
  width: 100%;
  background-color: var(--primary, #000000);
  color: var(--on-primary, #ffffff);
  border-radius: 0.75rem;
  font-size: 14px;
  font-weight: 600;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: opacity .15s ease, transform .1s ease;
}

.btn-primary-custom:hover {
  opacity: 0.9;
  color: var(--on-primary, #ffffff);
}

.btn-primary-custom:active {
  transform: scale(0.98);
}

.btn-primary-custom:disabled {
  opacity: 0.9;
}

.error-alert {
  /* display: none; */
  /* Handled by Vue's :style binding */
  margin-bottom: 24px;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: rgba(255, 218, 214, 0.5);
  border: 1px solid rgba(186, 26, 26, 0.10);
  align-items: center;
  gap: 0.75rem;
}

.error-alert .material-symbols-outlined {
  color: var(--error, #ba1a1a);
}

.error-alert p {
  color: var(--on-error-container, #93000a);
  font-size: 14px;
  margin: 0;
}

.divider-text {
  color: var(--outline-variant, #c6c6cd);
  font-size: 12px;
  letter-spacing: 0.03em;
  white-space: nowrap;
}

.divider-line {
  height: 1px;
  flex: 1;
  background-color: var(--outline-variant, #c6c6cd);
}

.sso-btn {
  height: 48px;
  border: 1px solid var(--outline-variant, #c6c6cd);
  border-radius: 0.75rem;
  background-color: var(--surface, #f7f9fb);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  transition: background-color .15s ease;
  color: var(--on-surface, #191c1e);
  font-size: 14px;
  font-weight: 500;
}

.sso-btn:hover {
  background-color: var(--surface-container, #eceef0);
  color: var(--on-surface, #191c1e);
}

.sso-btn svg,
.sso-btn .material-symbols-outlined {
  transition: transform .15s ease;
}

.sso-btn:hover svg,
.sso-btn:hover .material-symbols-outlined {
  transform: scale(1.1);
}

.secure-badge {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  border: 1px solid #fff;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  z-index: 20;
}

.secure-badge .material-symbols-outlined {
  font-size: 16px;
  color: #16a34a;
  font-variation-settings: 'FILL' 1;
}

.secure-badge span.txt {
  color: var(--on-surface-variant, #45464d);
  font-size: 12px;
  font-weight: 500;
}

@keyframes shake {

  0%,
  100% {
    transform: translateX(0);
  }

  25% {
    transform: translateX(-4px);
  }

  75% {
    transform: translateX(4px);
  }
}

.animate-shake {
  animation: shake 0.2s cubic-bezier(.36, .07, .19, .97) both;
}
</style>