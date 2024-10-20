import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { fetchTimesheets } from '../../services/timesheetService'; // Import the service function
import { DataGrid } from '@mui/x-data-grid'; // Import DataGrid from Material-UI
import VisibilityIcon from '@mui/icons-material/Visibility';

const TimesheetList: React.FC = () => {
    const [timesheets, setTimesheets] = useState([]);
    const [selectedTimesheetId, setSelectedTimesheetId] = useState<string | null>(null); // Rename state for clarity
    const navigate = useNavigate();

    useEffect(() => {
        const fetchTimesheetData = async () => {
            const data = await fetchTimesheets(); // Use the service function
            setTimesheets(data);
        };
        fetchTimesheetData();
    }, []);

    const columns = [ // Define columns for DataGrid
        { field: 'status', headerName: 'Status', minWidth: 150, },
        { field: 'start_date', headerName: 'Start Date', minWidth: 150, },
        { field: 'end_date', headerName: 'End Date', minWidth: 150, },
    ];

    return (
    <Box sx={{ height: '100%', width: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h4" gutterBottom>
        Your Timesheets
      </Typography>
      <Box sx={{ mb: 2, textAlign: "left" }}>
        <Button
          sx={{ mr: 1}}
          variant="outlined"
          startIcon={<VisibilityIcon />}
          disabled={!selectedTimesheetId}
          onClick={() => navigate(`/timesheet/${selectedTimesheetId}`)}
        >
          View
        </Button>
      </Box>
      <Paper sx={{ flexGrow: 1, width: '100%', height: "100%", overflow: 'hidden' }}>
      <DataGrid
          autoHeight
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
