<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <!-- RouterView se encarga de renderizar LoginView, RegisterView, etc., según la ruta activa -->
  <RouterView />
</template>

<style>
/* Estilos globales para toda la aplicación si son necesarios */
#app {
  min-height: 100vh;
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
</style>