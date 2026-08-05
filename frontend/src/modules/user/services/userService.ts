// src/modules/user/services/userService.ts
import api from '@/api/axios';

export interface User {
  id?: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  role?: 'admin' | 'user';
  is_active?: boolean;
  profile_picture_url?: string;
  created_at?: string;
}

export interface PasswordChangeData {
  current_password: string;
  new_password: string;
}

// Payload genérico para soportar objetos JSON o FormData
export type UserPayload = FormData | (Omit<User, 'id'> & { password?: string });

export const userService = {
  async getUsers(): Promise<User[]> {
    const response = await api.get('/users');
    return response.data;
  },

  async getUserById(id: number): Promise<User> {
    const response = await api.get(`/users/${id}`);
    return response.data;
  },

  async createUser(data: UserPayload): Promise<User> {
    const isFormData = data instanceof FormData;
    const response = await api.post('/users', data, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : undefined
    });
    return response.data;
  },

  async updateUser(id: number, data: UserPayload | Partial<User>): Promise<User> {
    const isFormData = data instanceof FormData;
    const response = await api.put(`/users/${id}`, data, {
      headers: isFormData ? { 'Content-Type': 'multipart/form-data' } : undefined
    });
    return response.data;
  },

  async changePassword(data: PasswordChangeData): Promise<void> {
    const response = await api.put('/users/me/password', data);
    return response.data;
  },

  async deleteUser(id: number): Promise<void> {
    const response = await api.delete(`/users/${id}`);
    return response.data;
  }
};