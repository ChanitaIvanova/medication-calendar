import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { fetchTimesheets, deleteTimesheet } from '../../services/timesheetService'; // Import the service function
import { DataGrid, GridColDef } from '@mui/x-data-grid'; // Import DataGrid from Material-UI
import VisibilityIcon from '@mui/icons-material/Visibility';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

const TimesheetList: React.FC = () => {
    const [timesheets, setTimesheets] = useState([]);
    const [selectedTimesheetId, setSelectedTimesheetId] = useState<string | null>(null);
    const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
    const navigate = useNavigate();

    const columns: GridColDef[] = [
        { field: 'status', headerName: 'Status', minWidth: 150 },
        { field: 'start_date', headerName: 'Start Date', minWidth: 150 },
        { field: 'end_date', headerName: 'End Date', minWidth: 150 },
    ];

    useEffect(() => {
        const fetchTimesheetData = async () => {
            const data = await fetchTimesheets(); // Use the service function
            setTimesheets(data);
        };
        fetchTimesheetData();
    }, []);

    const handleDelete = async () => {
        if (selectedTimesheetId) {
            await deleteTimesheet(selectedTimesheetId); // Implement this function in your service
            setDeleteDialogOpen(false);
            setSelectedTimesheetId(null);
            // Refresh the list after deletion
            const data = await fetchTimesheets();
            setTimesheets(data);
        }
    };

    return (
        <Box sx={{ height: '100%', width: '100%', display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h4" gutterBottom>
                Your Timesheets
            </Typography>
            <Box sx={{ mb: 2, textAlign: "left" }}>
                <Button
                    sx={{ mr: 1 }}
                    variant="outlined"
                    startIcon={<VisibilityIcon />}
                    disabled={!selectedTimesheetId}
                    onClick={() => navigate(`/timesheet/${selectedTimesheetId}`)}
                >
                    View
                </Button>
                <Button
                    sx={{ mr: 1 }}
                    variant="outlined"
                    startIcon={<EditIcon />}
                    disabled={!selectedTimesheetId}
                    onClick={() => navigate(`/edit-timesheet/${selectedTimesheetId}`)} // Navigate to edit page
                >
                    Edit
                </Button>
                <Button
                    sx={{ mr: 1 }}
                    variant="outlined"
                    startIcon={<DeleteIcon />}
                    disabled={!selectedTimesheetId}
                    onClick={() => setDeleteDialogOpen(true)}
                >
                    Delete
                </Button>
            </Box>
            <Paper sx={{ flexGrow: 1, width: '100%', height: "100%", overflow: 'hidden' }}>
                <DataGrid
                    autoHeight
                    rows={timesheets}
                    columns={columns}
                    pagination
                    paginationModel={{ pageSize: 5, page: 0 }}
                    pageSizeOptions={[5]}
                    onRowSelectionModelChange={(newSelection) => setSelectedTimesheetId(newSelection[0] as string)} // Update selectedTimesheetId
                    checkboxSelection={false}
                />
            </Paper>
            <Dialog
                open={deleteDialogOpen}
                onClose={() => setDeleteDialogOpen(false)}
            >
                <DialogTitle>Confirm Delete</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Are you sure you want to delete this timesheet?
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
                    <Button onClick={handleDelete} color="error">Delete</Button>
                </DialogActions>
            </Dialog>
        </Box>
    );
};

export default TimesheetList;
