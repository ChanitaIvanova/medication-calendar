import React, { useState, useEffect } from 'react';
import { Box, Typography, CircularProgress } from '@mui/material';
import { fetchTimesheet } from '../../services/timesheetService';
import TimesheetCalendar from './TimesheetCalendar';

const Timesheet: React.FC = () => {
  const [timesheet, setTimesheet] = useState<TimeSheet | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadData = async () => {
      try {
        const ts = await fetchTimesheet();
        setTimesheet(ts);
      } catch (err) {
        if (err.response?.status === 404) {
          setTimesheet(null);
        } else {
          setError('Failed to load timesheet');
        }
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return (
      <Typography color="error" variant="body1">
        {error}
      </Typography>
    );
  }

  return (
    <Box sx={{ maxWidth: '100%', margin: 'auto', padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        Timesheet
      </Typography>
      
      {timesheet ? (
        <TimesheetCalendar timesheet={timesheet} />
      ) : (
        <Typography variant="body1">
          You are not currently scheduled to take any medications.
        </Typography>
      )}
    </Box>
  );
};

export default Timesheet; 