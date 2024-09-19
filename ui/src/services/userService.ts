import axios from 'axios';
import User from '../types/User';

const API_URL = 'http://127.0.0.1:9000/api/auth';

export const userService = {
  login: async (username: string, password: string): Promise<User> => {
    const response = await axios.post<User>(`${API_URL}/login`, { username, password });
    return response.data;
  },

  signUp: async (email: string, username: string, password: string): Promise<void> => {
    await axios.post<User>(`${API_URL}/sign-up`, { email, username, password });
  },
};