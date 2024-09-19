import axios from 'axios';
import { MedicationFormData } from '../components/medication/Medication';

const API_BASE_URL = '/api/medications';

export const medicationService = {
  async fetchMedication(id: string) {
    const response = await axios.get(`${API_BASE_URL}/medication/${id}`);
    return response.data;
  },

  async fetchMedications(params: {
    page: number;
    per_page: number;
    sort_field: string;
    sort_direction: string;
    [key: string]: any;
  }) {
    const response = await axios.get(API_BASE_URL, { params });
    return response.data;
  },

  async createMedication(data: MedicationFormData) {
    const response = await axios.post(API_BASE_URL, data);
    return response.data;
  },

  async updateMedication(id: string, data: MedicationFormData) {
    const response = await axios.put(`${API_BASE_URL}/medication/${id}`, data);
    return response.data;
  },

  async deleteMedication(id: string) {
    const response = await axios.delete(`${API_BASE_URL}/medication/${id}`);
    return response.data;
  },
};