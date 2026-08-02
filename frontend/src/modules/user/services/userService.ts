import api from '@/api/axios';

export interface User {
  id?: number;
  username: string;
  email: string;
  role?: string;
  created_at?: string;
}

export const userService = {
  async getUsers() {
    const response = await api.get('/users');
    return response.data;
  },

  async createUser(user: Omit<User, 'id'> & { password?: string }) {
    const response = await api.post('/users', user);
    return response.data;
  },

  async updateUser(id: number, user: Partial<User>) {
    const response = await api.put(`/users/${id}`, user);
    return response.data;
  },

  async deleteUser(id: number) {
    const response = await api.delete(`/users/${id}`);
    return response.data;
  }
};