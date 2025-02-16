import React, { useState, useEffect } from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import { useUser } from '../../context/UserContext';
import { useNavigate } from 'react-router-dom';
import { Brightness4, Brightness7 } from '@mui/icons-material'; // Import icons
import { createTheme } from '@mui/material/styles'; // Import createTheme

function Navigation({ theme, setTheme }: { theme: any; setTheme: (theme: any) => void }): JSX.Element { // Accept theme and setTheme as props
    const { user, setUser, clearUser } = useUser();
    const navigate = useNavigate();

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const response = await fetch('/api/auth/user', {
                    method: 'GET',
                    credentials: 'include', // This is important for including cookies
                });
                if (response.ok) {
                    const userData = await response.json();
                    setUser(userData);
                } else {
                    clearUser();
                }
            } catch (error) {
                console.error('Error checking authentication:', error);
                clearUser();
            }
        };

        checkAuth();
    }, []);

    const logout = async () => {
        try {
            const response = await fetch('/api/auth/logout', {
                method: 'GET',
                credentials: 'include',
            });
            if (response.ok) {
                clearUser();
            } else {
                console.error('Logout failed');
            }
        } catch (error) {
            console.error('Error during logout:', error);
        }
    };

    const toggleTheme = () => {
        const newMode = theme.palette.mode === 'light' ? 'dark' : 'light';
        setTheme(createTheme({ palette: { mode: newMode } }));
    };

    return (
        <>
            <div>
                <AppBar
                    position="fixed"
                    sx={{
                        boxShadow: 0,
                        bgcolor: 'transparent',
                        backgroundImage: 'none',
                        mt: 2,
                    }}
                >
                    <Container maxWidth="lg">
                        <Toolbar
                            variant="regular"
                            sx={(theme) => ({
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between',
                                flexShrink: 0,
                                borderRadius: '999px',
                                backdropFilter: 'blur(24px)',
                                maxHeight: 40,
                                border: '1px solid',
                                borderColor: 'divider'
                            })}
                        >
                            <Box>
                                <Button
                                    color="primary"
                                    variant="text"
                                    size="small"
                                    onClick={() => navigate('/')}
                                >
                                    Home
                                </Button>
                                {user && (
                                    <>
                                        <Button
                                            color="primary"
                                            variant="text"
                                            size="small"
                                            onClick={() => navigate('/timesheet')}
                                        >
                                            Timesheet
                                        </Button>
                                        <Button
                                            color="primary"
                                            variant="text"
                                            size="small"
                                            onClick={() => navigate('/medications')}
                                        >
                                            Medications
                                        </Button>
                                        <Button
                                            color="primary"
                                            variant="text"
                                            size="small"
                                            onClick={() => navigate('/new-medication')}
                                        >
                                            New Medication
                                        </Button>
                                    </>
                                )}
                            </Box>
                            <Box>
                                {user ? (
                                    <>
                                        <Button
                                            color="primary"
                                            variant="text"
                                            size="small"
                                            onClick={() => navigate('/profile')}
                                        >
                                            Profile
                                        </Button>
                                        <Button
                                            color="primary"
                                            variant="text"
                                            size="small"
                                            onClick={logout}
                                        >
                                            Logout
                                        </Button>
                                    </>
                                ) : (
                                    <>
                                        <Button
                                            color="primary"
                                            variant="text"
                                            size="small"
                                            onClick={() => navigate('/login')}
                                        >
                                            Log In
                                        </Button>
                                        <Button
                                            color="primary"
                                            variant="text"
                                            size="small"
                                            onClick={() => navigate('/sign-up')}
                                        >
                                            Sign Up
                                        </Button>
                                    </>
                                )}
                                <Button
                                    color="primary"
                                    variant="text"
                                    size="small"
                                    onClick={toggleTheme} // Add theme toggle button
                                >
                                    {theme.palette.mode === 'dark' ? <Brightness7 /> : <Brightness4 />} {/* Use theme prop */}
                                </Button>
                            </Box>
                        </Toolbar>
                    </Container>
                </AppBar>
            </div>
        </>
    )
}

export default Navigation
