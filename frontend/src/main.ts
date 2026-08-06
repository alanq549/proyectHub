import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'material-symbols';


// Importante: Si utilizas iconos de Material Symbols / Bootstrap Icons
import 'bootstrap-icons/font/bootstrap-icons.css' 
// En main.ts
import 'material-symbols/outlined.css' // Importa los estilos de la versión Outlined

// Tus estilos globales personalizados
import './assets/main.css'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')