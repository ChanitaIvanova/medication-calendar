import React from 'react';
import { useUser } from '../../context/UserContext';
import { Card, CardContent, Typography, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import Timesheet from '../timesheet/Timesheet';

const Home: React.FC = () => {
    const { user } = useUser();
    const navigate = useNavigate();

    if (!user) {
        return (
            <Card>
                <CardContent>
                    <Typography variant="h5">Welcome to Medication Timesheet</Typography>
                    <Typography variant="body2">Please log in to view your medication schedule.</Typography>
                    <Button variant="contained" onClick={() => navigate('/login')}>
                        Login
                    </Button>
                </CardContent>
            </Card>
        );
    }

    if (user.role === 'admin') {
        return (
            <Card>
                <CardContent>
                    <Typography variant="h5">Admin Dashboard</Typography>
                    <Typography variant="body2">Welcome to the admin dashboard. You can manage medications here.</Typography>
                    <Button variant="contained" onClick={() => navigate('/medications')} sx={{ mr: 2, mt: 2 }}>
                        View Medications
                    </Button>
                    <Button variant="contained" onClick={() => navigate('/new-medication')} sx={{ mt: 2 }}>
                        Add New Medication
                    </Button>
                </CardContent>
            </Card>
        );
    }

    return <Timesheet />;
};

export default Home;
