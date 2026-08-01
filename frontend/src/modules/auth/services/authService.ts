// src/modules/auth/services/authService.ts
import api from '@/api/axios';

export interface RegisterDTO {
  username: string;
  email: string;
  password: string; // O simplemente password
}

export interface LoginDTO {
  email: string;
  password: string;
}

export const authService = {
  async register(data: RegisterDTO) {
    const response = await api.post('/register', data);
    return response.data;
  },

  async login(data: LoginDTO) {
    const response = await api.post('/login', data);
    return response.data; // Retorna { token, user }
  },

  async getProfile() {
    const response = await api.get('/me');
    return response.data;
  }
};