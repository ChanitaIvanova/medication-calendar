import React from 'react';
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

  return (
    <>
      <ThemeProvider theme={defaultTheme}>
        <UserProvider>
          <Container component="main" maxWidth="lg">
            <CssBaseline />
            <Navigation />
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