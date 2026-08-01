<template>
  <div class="registration-wrapper">

    <div class="bg-blobs">
      <div class="blob-a"></div>
      <div class="blob-b"></div>
    </div>


    <main class="main-wrap">

      <div class="row g-0 min-vh-100">


        <!-- Sidebar -->
        <div class="col-lg-5 d-none d-lg-flex flex-column justify-content-between sidebar-branding">

          <div>

            <div class="d-flex align-items-center gap-3 mb-5">

              <div class="logo-badge">

                <span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;">
                  account_tree
                </span>

              </div>


              <span class="sidebar-brand-name">
                ProjectHub
              </span>

            </div>



            <h1 class="sidebar-title mb-0">
              Eleva tu gestión académica al siguiente nivel.
            </h1>


            <p class="sidebar-desc mt-4">
              Únete a la plataforma líder para la colaboración en investigación
              y proyectos universitarios de alto impacto.
            </p>


          </div>




          <div class="d-flex flex-column gap-4">


            <div class="d-flex align-items-center gap-3">


              <div class="testimonial-avatar">

                <img
                  src="https://lh3.googleusercontent.com/aida-public/AB6AXuB3-e9ihrzVn3ULohcOKL4KvEz7DZLqzD601WzuRXHMYoJqHouMp1vqA5MN_mxQWM0Y9YX4675KEyKZnzqjM27sodKERztvnQLOROz1pSArKpGYP3atvmbAPwHfdA195IiftfjBRaOsCugE4F1kcsWHs8I4IzwKWibaBNg_G7vjeOY-ssa0m7LYR8JKPj22S9P2w_hox9gzcQ-LBGvX3ONIU-P2coSImkcK00mR28RLOnBCBfk8wYKT7Q"
                  alt="Dra. Elena Martínez" />

              </div>



              <div>

                <p class="testimonial-name">
                  Dra. Elena Martínez
                </p>


                <p class="testimonial-role">
                  Investigadora Principal, CSIC
                </p>


              </div>


            </div>




            <div class="glass-card testimonial-quote">

              "ProjectHub transformó nuestra metodología de trabajo en red,
              permitiéndonos centralizar recursos de forma impecable."

            </div>


          </div>


        </div>







        <!-- Registration Section -->
        <div class="col-12 col-lg-7 form-section">


          <div class="w-100" style="max-width:480px;">



            <!-- Mobile Branding -->

            <div class="d-lg-none mobile-brand">


              <div class="mobile-logo-badge">

                <span class="material-symbols-outlined" style="font-size:18px;">
                  account_tree
                </span>


              </div>


              <span class="sidebar-brand-name">
                ProjectHub
              </span>


            </div>







            <!-- Register Form -->

            <div v-if="!registrationSuccess">


              <header class="mb-4">


                <h2 class="reg-title mb-2">
                  Crear una cuenta
                </h2>


                <p class="reg-subtitle mb-0">
                  Ingresa tus datos para comenzar tu trayecto académico.
                </p>


              </header>






              <form @submit.prevent="handleRegistration">





                <!-- Username -->

                <div class="mb-3">


                  <label class="form-label-custom">
                    Nombre de usuario
                  </label>


                  <div class="input-icon-wrap">


                    <span class="material-symbols-outlined icon-left">
                      person
                    </span>



                    <input v-model="username" type="text" class="form-control form-control-custom"
                      placeholder="ej. jdoe_research" required />


                  </div>


                </div>








                <!-- Email -->

                <div class="mb-3">


                  <label class="form-label-custom">
                    Correo electrónico
                  </label>



                  <div class="input-icon-wrap">


                    <span class="material-symbols-outlined icon-left">
                      mail
                    </span>



                    <input v-model="email" type="email" class="form-control form-control-custom"
                      placeholder="correo@universidad.edu" required />


                  </div>


                </div>








                <!-- Password -->

                <div class="mb-3">


                  <label class="form-label-custom">
                    Contraseña
                  </label>



                  <div class="input-icon-wrap">


                    <span class="material-symbols-outlined icon-left">
                      lock
                    </span>




                    <input v-model="password" :type="showPassword ? 'text' : 'password'"
                      class="form-control form-control-custom has-toggle" placeholder="••••••••" required
                      @input="checkStrength(password)" />




                    <button type="button" class="toggle-icon" @click="togglePassword">

                      <span class="material-symbols-outlined">
                        {{ showPassword ? 'visibility_off' : 'visibility' }}
                      </span>

                    </button>


                  </div>






                  <div class="pt-1">


                    <div class="strength-row">


                      <span class="strength-text">
                        Seguridad de la contraseña
                      </span>



                      <span class="strength-label" :style="{ color: strengthColor }">
                        {{ strengthText }}
                      </span>


                    </div>





                    <div class="strength-track">


                      <div class="password-strength-bar" :style="{
                        width: strength + '%',
                        backgroundColor: strengthColor
                      }"></div>



                    </div>



                  </div>



                </div>







                <!-- Confirm Password -->

                <div class="mb-3">


                  <label class="form-label-custom">
                    Confirmar contraseña
                  </label>



                  <div class="input-icon-wrap">


                    <span class="material-symbols-outlined icon-left">
                      verified_user
                    </span>




                    <input v-model="confirmPassword" :type="showConfirmPassword ? 'text' : 'password'"
                      class="form-control form-control-custom has-toggle" placeholder="••••••••" required />




                    <button type="button" class="toggle-icon" @click="toggleConfirmPassword">


                      <span class="material-symbols-outlined">
                        {{ showConfirmPassword ? 'visibility_off' : 'visibility' }}
                      </span>


                    </button>



                  </div>



                </div>







                <!-- Button -->

                <div class="pt-2">


                  <button class="btn-register" type="submit" :disabled="isLoading">


                    <span>
                      {{ isLoading ? 'Creando cuenta...' : 'Registrarse' }}
                    </span>




                    <span v-if="isLoading" class="spinner-border spinner-border-sm"></span>



                    <span v-else class="material-symbols-outlined" style="font-size:18px;">
                      arrow_forward
                    </span>



                  </button>



                </div>




              </form>







              <footer class="form-footer">


                <p class="reg-subtitle mb-0">


                  ¿Ya tienes cuenta?


                  <a href="#" @click.prevent="router.push({ name: 'login' })">
                    Inicia sesión
                  </a>


                </p>



              </footer>





            </div>









            <!-- Success State -->

            <div v-else id="success-state" class="show">



              <div class="success-icon-wrap">


                <span class="material-symbols-outlined" style="font-size:48px;font-variation-settings:'FILL' 1;">
                  check_circle
                </span>



              </div>





              <h2 class="reg-title">
                ¡Registro Exitoso!
              </h2>





              <p class="reg-subtitle mx-auto" style="max-width:20rem;">
                Hemos enviado un enlace de verificación a tu correo electrónico.
                Por favor, revisa tu bandeja de entrada para activar tu cuenta.
              </p>






              <button class="btn-back-home" @click="router.push({ name: 'home' })">

                Volver al inicio

              </button>





            </div>




          </div>



        </div>



      </div>



    </main>
  </div>
</template>

<script setup lang="ts">

import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// Form data

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');

// UI states

const showPassword = ref(false);
const showConfirmPassword = ref(false);

const isLoading = ref(false);
const registrationSuccess = ref(false);



// Password strength

const strength = ref(0);

const strengthText = ref('Baja');

const strengthColor = ref('var(--outline-variant)');


// Toggle password visibility

const togglePassword = () => {

  showPassword.value = !showPassword.value;

};

const toggleConfirmPassword = () => {

  showConfirmPassword.value = !showConfirmPassword.value;

};

// Password security checker

const checkStrength = (pwd: string) => {

  // Reset when empty

  if (!pwd.length) {

    strength.value = 0;
    strengthText.value = 'Baja';
    strengthColor.value = 'var(--outline-variant)';

    return;

  }

  let newStrength = 0;

  if (pwd.length > 5) {

    newStrength += 25;

  }

  if (pwd.length > 10) {

    newStrength += 25;

  }

  if (/[A-Z]/.test(pwd)) {

    newStrength += 25;

  }


  if (/[0-9]/.test(pwd)) {

    newStrength += 25;

  }

  if (newStrength <= 25) {


    strengthText.value = 'Débil';

    strengthColor.value = 'var(--error)';


  } else if (newStrength <= 75) {


    strengthText.value = 'Media';

    strengthColor.value = 'var(--secondary)';


  } else {

    strengthText.value = 'Fuerte';

    strengthColor.value = '#22c55e';
  }

  strength.value = newStrength;

};

// Register simulation

const handleRegistration = () => {

  if (password.value !== confirmPassword.value) {

    alert('Las contraseñas no coinciden');

    return;
  }

  isLoading.value = true;

  // Simulación de llamada API

  setTimeout(() => {
    isLoading.value = false;
    registrationSuccess.value = true;
  }, 1500);

};
</script>

<style scoped>

:global(:root){

  --outline: #76777d;
  --surface-container: #eceef0;
  --on-surface: #191c1e;
  --secondary-container: #645efb;
  --surface-container-low: #f2f4f6;
  --background: #f7f9fb;
  --outline-variant: #c6c6cd;
  --surface-container-lowest: #ffffff;
  --secondary: #4b41e1;
  --error: #ba1a1a;
  --on-surface-variant: #45464d;
  --surface-container-highest: #e0e3e5;
  --surface-dim: #d8dadc;
  --primary: #000000;
  --on-primary: #ffffff;

}



:global(body){

  font-family:'Inter', sans-serif;
  background-color:var(--background);
  color:var(--on-surface);
  min-height:100vh;
  overflow-x:hidden;

}




.material-symbols-outlined{

  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24;

}







/* Background */

.bg-blobs{

  position:fixed;
  inset:0;
  z-index:0;
  overflow:hidden;
  pointer-events:none;

}



.blob-a{

  position:absolute;

  top:-20%;
  left:-10%;

  width:60%;
  height:60%;

  border-radius:50%;

  background:rgba(0,0,0,.05);

  filter:blur(120px);

}



.blob-b{

  position:absolute;

  bottom:-20%;
  right:-10%;

  width:50%;
  height:50%;

  border-radius:50%;

  background:rgba(75,65,225,.05);

  filter:blur(120px);

}





.main-wrap{

  position:relative;

  z-index:10;

  min-height:100vh;

}





.glass-card{

  background:rgba(255,255,255,.85);

  backdrop-filter:blur(16px);

  -webkit-backdrop-filter:blur(16px);

  border:1px solid rgba(226,232,240,.8);

}









/* Sidebar */

.sidebar-branding{

  background-color:var(--surface-container-lowest);

  padding:48px;

  border-right:1px solid rgba(198,198,205,.3);

  height:100%;

}



.logo-badge{

  width:40px;
  height:40px;

  background-color:var(--primary);

  border-radius:.75rem;

  display:flex;

  align-items:center;

  justify-content:center;

  color:white;

  box-shadow:0 10px 15px -3px rgba(0,0,0,.1);

}





.sidebar-brand-name{

  font-size:20px;

  font-weight:700;

  letter-spacing:-.01em;

  color:var(--primary);

}





.sidebar-title{

  font-size:48px;

  font-weight:700;

  letter-spacing:-.02em;

  line-height:1.1;

  color:var(--primary);

  max-width:28rem;

}





.sidebar-desc{

  color:var(--on-surface-variant);

  max-width:24rem;

  line-height:1.6;

}





.testimonial-avatar{

  width:48px;

  height:48px;

  border-radius:50%;

  overflow:hidden;

  border:2px solid white;

}



.testimonial-avatar img{

  width:100%;

  height:100%;

  object-fit:cover;

}



.testimonial-name{

  font-size:14px;

  font-weight:500;

  color:var(--on-surface);

  margin-bottom:0;

}



.testimonial-role{

  font-size:12px;

  color:var(--on-surface-variant);

  margin-bottom:0;

}



.testimonial-quote{

  padding:12px;

  border-radius:.75rem;
  font-size:12px;
  color:var(--on-surface-variant);
  font-style:italic;
}

/* Form */

.form-section{
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  padding:24px;
  min-height:100vh;
}



@media(min-width:768px){
  .form-section{
    padding:48px;
  }
}

@media(min-width:992px){
  .form-section{
    padding:96px;
  }
}

.mobile-brand{
  display:flex;
  align-items:center;
  gap:.5rem;
  margin-bottom:3rem;
}



.mobile-logo-badge{
  width:32px;
  height:32px;
  background-color:var(--primary);
  border-radius:.5rem;
  display:flex;
  align-items:center;
  justify-content:center;
  color:white;
}

.reg-title{
  font-size:24px;
  font-weight:600;
  letter-spacing:-.01em;
  color:var(--primary);
}



@media(min-width:768px){
  .reg-title{
    font-size:32px;
    letter-spacing:-.015em;
  }
}


.reg-subtitle{
  color:var(--on-surface-variant);
}


.form-label-custom{
  font-size:14px;
  font-weight:500;
  color:var(--on-surface);
}

.input-icon-wrap{
  position:relative;
}

.icon-left{
  position:absolute;
  left:16px;
  top:50%;
  transform:translateY(-50%);
  color:var(--outline-variant);
  pointer-events:none;
}




.toggle-icon{
  position:absolute;
  right:16px;
  top:50%;
  transform:translateY(-50%);
  background:none;
  border:none;
  color:var(--outline-variant);
  cursor:pointer;
}



.toggle-icon:hover{
  color:var(--primary);
}







.form-control-custom{
  height:48px;
  padding-left:48px;
  padding-right:16px;
  background-color:var(--surface-container-lowest);
  border:1px solid var(--outline-variant);
  border-radius:.75rem;
  font-size:16px;
}



.form-control-custom.has-toggle{
  padding-right:48px;
}



.form-control-custom:focus{
  outline:none;
  border-color:var(--secondary);
  box-shadow:0 0 0 4px rgba(75,65,225,.10);
}

/* Strength */
.strength-row{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:.25rem;
}



.strength-text{
  font-size:12px;
  color:var(--on-surface-variant);
}



.strength-label{
  font-size:10px;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.05em;
}

.strength-track{
  width:100%;
  height:4px;
  background-color:var(--surface-container-highest);
  border-radius:9999px;
  overflow:hidden;
}



.password-strength-bar{
  height:4px;
  border-radius:9999px;
  transition:.3s ease;
}


/* Button */

.btn-register{
  width:100%;
  height:48px;
  background-color:var(--primary);
  color:var(--on-primary);
  font-size:14px;
  font-weight:700;
  border-radius:.75rem;
  border:none;
  display:flex;
  justify-content:center;
  align-items:center;
  gap:.5rem;
  box-shadow:0 10px 15px -3px rgba(0,0,0,.12);
}

.btn-register:hover{
  opacity:.9;
}

.btn-register:active{
  transform:scale(.98);
}

/* Footer */
.form-footer{
  padding-top:2rem;
  text-align:center;
  border-top:1px solid rgba(198,198,205,.3);
}

.form-footer a{
  color:var(--primary);
  font-weight:600;
  text-decoration:none;
}



.form-footer a:hover{
  text-decoration:underline;

}

/* Success */

#success-state.show{
  display:flex;
  flex-direction:column;
  align-items:center;
  text-align:center;
  gap:24px;
  animation:fadeIn .5s ease forwards;
}

@keyframes fadeIn{
  from{
    opacity:0;
    transform:translateY(10px);
  }

  to{
    opacity:1;
    transform:translateY(0);
  }

}

.success-icon-wrap{
  width:80px;
  height:80px;
  background-color:rgba(75,65,225,.10);
  color:var(--secondary);
  border-radius:50%;
  display:flex;
  align-items:center;
  justify-content:center;
}





.btn-back-home{
  padding:0 2rem;
  height:48px;
  background-color:var(--surface-container-highest);
  color:var(--primary);
  font-size:14px;
  font-weight:700;
  border:none;
  border-radius:.75rem;

}

.btn-back-home:hover{
  background-color:var(--surface-dim);
}

</style>