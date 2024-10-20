import React, { useEffect, useState } from 'react';
import { fetchActiveTimesheet } from '../../services/timesheetService'; // New service function
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, Typography, Button, CircularProgress } from '@mui/material';
import TimesheetCalendar from '../timesheet/TimesheetCalendar';

const Home: React.FC = () => {
    const [activeTimesheet, setActiveTimesheet] = useState(null);
    const [loading, setLoading] = useState(true); // New loading state
    const navigate = useNavigate();

    useEffect(() => {
        const loadActiveTimesheet = async () => {
            setLoading(true); // Set loading to true when starting to fetch
            try {
                const timesheet = await fetchActiveTimesheet(); // Fetch the active timesheet
                setActiveTimesheet(timesheet);
            } catch (err) {
                console.error('Failed to load active timesheet');
            } finally {
                setLoading(false); // Set loading to false after fetching
            }
        };

        loadActiveTimesheet();
    }, []);

    if (loading) {
        return (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <CircularProgress /> {/* Loading spinner */}
            </div>
        );
    }

    return (
        <div>
            {activeTimesheet ? (
                <TimesheetCalendar timesheet={activeTimesheet} /> // Pass the timesheet directly
            ) : (
                <Card>
                    <CardContent>
                        <Typography variant="h5">No Active Timesheet</Typography>
                        <Typography variant="body2">You don't have an active timesheet. Please create one.</Typography>
                        <Button variant="contained" onClick={() => navigate('/new-timesheet')}>
                            New Timesheet
                        </Button>
                    </CardContent>
                </Card>
            )}
        </div>
    );
};

export default Home;
