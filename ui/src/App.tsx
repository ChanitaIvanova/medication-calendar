import React, { useEffect, useState } from 'react';
import './App.css'
import { Outlet } from 'react-router-dom';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import { UserProvider } from './context/UserContext';
import Navigation from './components/navigation/Navigation'

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();

function App(): JSX.Element {
  const [theme, setTheme] = useState(() => {
    return sessionStorage.getItem('theme') === 'dark' ? createTheme({ palette: { mode: 'dark' } }) : defaultTheme;
  });

  useEffect(() => {
    sessionStorage.setItem('theme', theme.palette.mode);
  }, [theme]);

  return (
    <>
      <ThemeProvider theme={theme}>
        <UserProvider>
          <Container component="main" maxWidth="lg">
            <CssBaseline />
            <Navigation theme={theme} setTheme={setTheme} /> {/* Pass theme and setTheme to Navigation */}
            <Container maxWidth="lg" sx={{ my: 8 }}>
              <Outlet />
            </Container>
          </Container>
        </UserProvider>
      </ThemeProvider>
    </>
  )
}

export default App
