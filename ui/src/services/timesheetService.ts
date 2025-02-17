import axios from 'axios';
import {TimeSheet, TimesheetBe} from '../models/timesheet_model'

export const fetchTimesheets = async () => {
  const response = await axios.get('/api/timesheets/timesheets', { withCredentials: true });
  return response.data.map((timesheet: TimesheetBe) => new TimeSheet(timesheet));
};

export const fetchTimesheet = async () => {
  const response = await axios.get('/api/timesheets/timesheet', { withCredentials: true });
  return new TimeSheet(response.data);
};

export const createTimesheet = async (data: { medication_ids: string[], start_date: string, end_date: string }) => {
  const response = await axios.post('/api/timesheets/timesheet', data, {
    withCredentials: true, // Include credentials for CORS
  });
  return response.data;
};

export const deleteTimesheet = async (id: string) => {
  await axios.delete(`/api/timesheets/timesheet/${id}`, { withCredentials: true });
};

export const updateTimesheet = async (data: { medication_ids: string[], start_date: string, end_date: string }) => {
  const response = await axios.put('/api/timesheets/timesheet', data, {
    withCredentials: true,
  });
  return new TimeSheet(response.data);
};

export const fetchActiveTimesheet = async () => {
    const response = await axios.get('/api/timesheets/timesheet/active', { withCredentials: true });
    return new TimeSheet(response.data);
};
