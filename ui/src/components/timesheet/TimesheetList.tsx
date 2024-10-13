import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { DataGrid } from '@mui/x-data-grid'; // Import DataGrid from Material-UI
import VisibilityIcon from '@mui/icons-material/Visibility';

const TimesheetList: React.FC = () => {
    const [timesheets, setTimesheets] = useState([]);
    const [selectedTimesheetId, setSelectedTimesheetId] = useState<string | null>(null); // Rename state for clarity
    const navigate = useNavigate();

    useEffect(() => {
        const fetchTimesheets = async () => {
            const response = await axios.get('/api/timesheets/timesheets', { withCredentials: true });
            setTimesheets(response.data);
        };
        fetchTimesheets();
    }, []);

    const columns = [ // Define columns for DataGrid
        { field: 'status', headerName: 'Status', width: 150 },
        { field: 'start_date', headerName: 'Start Date', width: 150 },
        { field: 'end_date', headerName: 'End Date', width: 150 },
    ];

    return (
    <Box sx={{ height: '100%', width: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h4" gutterBottom>
        Your Timesheets
      </Typography>
      <Box sx={{ mb: 2 }}>
        <Button
          startIcon={<VisibilityIcon />}
          disabled={!selectedTimesheetId}
          onClick={() => navigate(`/timesheet/${selectedTimesheetId}`)}
        >
          View
        </Button>
      </Box>
      <Paper sx={{ flexGrow: 1, width: '100%', height: "100%", overflow: 'hidden' }}>
      <DataGrid // Replace table with DataGrid
                rows={timesheets}
                columns={columns}
                paginationModel={{pageSize: 5, page: 0}}
                pageSizeOptions={[5]}
                onRowSelectionModelChange={(newSelection) => setSelectedTimesheetId(newSelection[0] as string)} // Update selectedTimesheetId
                checkboxSelection={false}
            />
      </Paper>
    </Box>
    );
};

export default TimesheetList;
