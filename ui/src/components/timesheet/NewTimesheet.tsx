import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  FormControl,
  InputLabel,
  OutlinedInput,
  MenuItem,
  Select,
  Typography,
  Stack,
  Chip
} from '@mui/material';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { useNavigate } from 'react-router-dom';
import { createTimesheet } from '../../services/timesheetService';
import { medicationService } from '../../services/medicationService';
import dayjs from 'dayjs'

const NewTimesheet: React.FC = () => {
  const [medications, setMedications] = useState([]);
  const [selectedMedications, setSelectedMedications] = useState<any[]>([]);
  const [startDate, setStartDate] = useState(dayjs(new Date()));
  const [endDate, setEndDate] = useState(dayjs(new Date()));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const loadMedications = async () => {
      try {
        const meds = await medicationService.fetchUserMedications(); // Use the new getMedications function
        setMedications(meds);
      } catch (err) {
        setError('Failed to load medications');
      }
    };

    loadMedications();
  }, []);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      await createTimesheet({ medication_ids: selectedMedications.map(medication => medication.id), start_date: dayjs(startDate).format('YYYY-MM-DD'), end_date: dayjs(endDate).format('YYYY-MM-DD') });
      navigate('/timesheets');
    } catch (err) {
      setError('Failed to create timesheet');
    } finally {
      setLoading(false);
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Typography variant="h4" gutterBottom>
        New Timesheet
      </Typography>
      <Box sx={{ maxWidth: 600, margin: 'auto', padding: 2 }}>
        <form onSubmit={handleSubmit}>
          <FormControl fullWidth margin="normal">
            <InputLabel>Medications</InputLabel>
            <Select
              multiple
              value={selectedMedications}
              onChange={(e) => setSelectedMedications(e.target.value as any[])}
              input={<OutlinedInput label="Multiple Select" />}
              renderValue={(selected) => (
                <Stack gap={1} direction="row" flexWrap="wrap">
                  {selected.map((value) => (
                    <Chip key={value.id} label={value.name} />
                  ))}
                </Stack>
              )}
            >
              {medications.map((med) => (
                <MenuItem key={med.id} value={med}>
                  {med.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
          <DatePicker
            sx={{width: '100%', mt: 1, mb: 1}}
            label="Start Date"
            value={startDate}
            onChange={(newValue) => setStartDate(newValue)}
          />
          <DatePicker
            sx={{width: '100%', mt: 1, mb: 1}}
            label="End Date"
            value={endDate}
            onChange={(newValue) => setEndDate(newValue)}
          />
          {error && (
            <Typography color="error" variant="body2">
              {error}
            </Typography>
          )}
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
            <Button variant="contained" color="primary" type="submit" disabled={loading}>
              {loading ? <CircularProgress size={24} /> : 'Create Timesheet'}
            </Button>
          </Box>
        </form>
      </Box>
    </LocalizationProvider>
  );
};

export default NewTimesheet;