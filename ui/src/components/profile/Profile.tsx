import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';
import { useUser } from '../../context/UserContext';

function Profile(): JSX.Element {
  const { user } = useUser();

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ mt: 4, p: 4 }}>
        <Typography variant="h4" gutterBottom>
          User Profile
        </Typography>
        <Box sx={{ mt: 2 }}>
          <Typography variant="body1">
            <strong>Username:</strong> {user?.username}
          </Typography>
        </Box>
        <Box sx={{ mt: 2 }}>
          <Typography variant="body1">
            <strong>Email:</strong> {user?.email}
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
}

export default Profile;
