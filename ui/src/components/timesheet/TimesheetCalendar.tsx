import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

const TimesheetCalendar: React.FC<{ id: string }> = () => {
    const { id } = useParams<{ id: string }>();
    const [timesheet, setTimesheet] = useState(null);

    useEffect(() => {
        const fetchTimesheet = async () => {
            const response = await axios.get(`/api/timesheets/timesheet/${id}`, { withCredentials: true });
            setTimesheet(response.data);
        };
        fetchTimesheet();
    }, [id]);

    return (
        <div>
            <h1>Timesheet Calendar</h1>
            {timesheet ? (
                <div>
                    {/* Render calendar based on timesheet data */}
                    <h2>{timesheet.start_date} to {timesheet.end_date}</h2>
                    {/* Additional rendering logic for calendar */}
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default TimesheetCalendar;
