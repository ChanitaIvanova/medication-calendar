import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Typography,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { createTimesheet } from '../../services/timesheetService';
import { medicationService } from '../../services/medicationService';

const NewTimesheet: React.FC = () => {
  const [medications, setMedications] = useState([]);
  const [selectedMedications, setSelectedMedications] = useState<string[]>([]);
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
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
      await createTimesheet({ medication_ids: selectedMedications, start_date: startDate, end_date: endDate });
      navigate('/timesheets');
    } catch (err) {
      setError('Failed to create timesheet');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto', padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        New Timesheet
      </Typography>
      <form onSubmit={handleSubmit}>
        <FormControl fullWidth margin="normal">
          <InputLabel id="medications-label">Medications</InputLabel>
          <Select
            labelId="medications-label"
            multiple
            value={selectedMedications}
            onChange={(e) => setSelectedMedications(e.target.value as string[])}
          >
            {medications.map((med) => (
              <MenuItem key={med.id} value={med.id}>
                {med.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField
          fullWidth
          margin="normal"
          label="Start Date"
          type="date"
          InputLabelProps={{ shrink: true }}
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          required
        />
        <TextField
          fullWidth
          margin="normal"
          label="End Date"
          type="date"
          InputLabelProps={{ shrink: true }}
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          required
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
  );
};

export default NewTimesheet;