// src/api/axios.ts
import axios from 'axios';

const api = axios.create({
  // En desarrollo usará '/api' (aprovechando el proxy de Vite) o la variable de entorno si está definida
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor REQUEST: Adjunta el Token JWT si existe
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor RESPONSE: Manejo centralizado de errores (401, 403, 500, etc.)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;

    if (status === 401) {
      // Token expirado o inválido: limpiar sesión y redirigir
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    } else if (status === 403) {
      console.error('Acceso denegado: No tienes permisos para realizar esta acción.');
    } else if (status >= 500) {
      console.error('Error en el servidor. Por favor, intente más tarde.');
    }

    return Promise.reject(error);
  }
);

export default api;