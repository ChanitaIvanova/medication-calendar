import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchTimesheet } from '../../services/timesheetService'; // Import the service function
import { TimeSheet, Medication } from '../../models/timesheet_model'; // Import the model
import Tooltip from '@mui/material/Tooltip';
import './TimesheetCalendar.css';
import { Button, Box, Typography } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

const TimesheetCalendar: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [timesheet, setTimesheet] = useState<TimeSheet | null>(null);
    const [currentMonth, setCurrentMonth] = useState(new Date());

    useEffect(() => {
        const fetchTimesheetData = async () => {
            const data = await fetchTimesheet(id); // Use the service function
            setTimesheet(data);
        };
        fetchTimesheetData();
    }, [id]);

    const handleMonthChange = (direction: 'next' | 'prev') => {
        setCurrentMonth(prev => {
            const newMonth = new Date(prev);
            newMonth.setMonth(prev.getMonth() + (direction === 'next' ? 1 : -1));
            return newMonth;
        });
    };

    const buildMedicationsMapPerKey = (key: string, medications: any): Record<string, Medication[]> => {
        const medicationsMap: Record<string, Medication[]> = {};
        medications.forEach(med => {
            med.dates.forEach(medDate => {
                const dateKey = medDate[key]; // Use the date as the key
                if (!medicationsMap[dateKey]) {
                    medicationsMap[dateKey] = [];
                }
                const newMed = new Medication({ id: med.id, name: med.name, dosage: med.dosage, advise: med.advise, dates: [] });
                newMed.dates.push(medDate);
                medicationsMap[dateKey].push(newMed);
            });
        });

        return medicationsMap;
    }

    const renderCalendar = () => {
        if (!timesheet) return null;

        const monthDays = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0).getDate();
        const firstDay = (new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1).getDay() + 6) % 7; // Adjust to start on Monday
        const calendar = [];

        // Create a map to hold medications for each day
        const medicationsMap = buildMedicationsMapPerKey("date",  timesheet.medications);

        // Fill the calendar with empty cells for days before the first day of the month
        for (let i = 0; i < firstDay; i++) {
            calendar.push(<div key={`empty-${i}`} className="calendar-cell empty"></div>);
        }

        // Fill the calendar with days of the month
        for (let day = 1; day <= monthDays; day++) {
            const date = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), day);
            const dateKey = date.toISOString().split('T')[0]; // Get the date key

            const medicationsForDay = medicationsMap[dateKey] || []; // Get medications for the day

            // Sort medications by time
            medicationsForDay.sort((a, b) => {
                const timeA = a.dates[0].time; // Assuming the first date contains the time
                const timeB = b.dates[0].time;
                return timeA.localeCompare(timeB); // Use localeCompare for string comparison
            });

            // Create a map to hold medications for each day
            const medicationsForTimeMap = buildMedicationsMapPerKey("time",  medicationsForDay);
            const times = [];
            for (const time in medicationsForTimeMap) {
                times.push(time);
            }

            times.sort((a, b) => {
                return a.localeCompare(b); // Use localeCompare for string comparison
            });

            calendar.push(
                <div key={day} className="calendar-cell">
                    <div key={day} className="calendar-content">
                        <div className="day-number">{day}</div>
                        {times.map(time => (
                            <div className="medication-entry" key={time}><div>{time}</div> 
                                <ul>
                                {medicationsForTimeMap[time].map(med => (
                                    <li key={med.id + "_" + med.dates[0].time}>{med.name}
                                    <Tooltip title={`Dosage: ${med.dosage}, Advise: ${med.advise}`} arrow>
                                            <InfoOutlinedIcon sx={{fontSize: '0.6rem'}}/>
                                    </Tooltip>
                                    </li>
                                ))}
                                </ul>
                            </div>
                        ))}
                    </div>
                </div>
            );
        }

        // Fill the rest of the calendar grid with empty cells
        const totalCells = 35; // 5 rows and 7 columns to accommodate all months
        const remainingCells = totalCells - (firstDay + monthDays);
        for (let i = 0; i < remainingCells; i++) {
            calendar.push(<div key={`empty-end-${i}`} className="calendar-cell empty"></div>);
        }

        return calendar;
    };

    return (
        <div>
            <Typography variant="h4" gutterBottom>
                Timesheet Calendar
            </Typography>
            <Typography variant="h5" gutterBottom>
            {currentMonth.toLocaleString('default', { month: 'long' })} {currentMonth.getFullYear()}
            </Typography>
            <Box sx={{ height: '100%', width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'space-between', padding: '0 1rem' }}>
                <Button
                    variant="outlined"
                    startIcon={<ArrowBackIcon  />}
                    onClick={() => handleMonthChange('prev')}
                    >
                    Previous
                </Button>
                <Button
                    variant="outlined"
                    startIcon={<ArrowForwardIcon />}
                    onClick={() => handleMonthChange('next')}
                    >
                    Next
                </Button>
            </Box>
            <div className="calendar-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(7, 1fr)', gridTemplateRows: 'repeat(5, 1fr)' }}>
                {renderCalendar()}
            </div>
        </div>
    );
};

export default TimesheetCalendar;
