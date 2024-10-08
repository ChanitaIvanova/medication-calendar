import axios from 'axios';

export const createTimesheet = async (data: { medication_ids: string[], start_date: string, end_date: string }) => {
  const response = await axios.post('/api/timesheets/timesheet', data, {
    withCredentials: true, // Include credentials for CORS
  });
  return response.data;
};