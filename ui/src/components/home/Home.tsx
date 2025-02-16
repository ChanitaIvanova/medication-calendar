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

    return <Timesheet />;
};

export default Home;
