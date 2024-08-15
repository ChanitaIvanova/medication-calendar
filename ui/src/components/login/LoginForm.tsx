import React, { useState } from 'react';

import { TextField, Button, Box, Typography } from '@mui/material';

interface LoginFormProps {
    onLogin: (username: string, password: string) => void;
    error: string | null
}

const LoginForm: React.FC<LoginFormProps> = ({ onLogin, error }) => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [diplayError, setError] = useState<string | null>(null);

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(null);

        if (username.trim() === '' || password.trim() === '') {
            setError('Username and password are required');
            return;
        }

        onLogin(username, password);
    };

    return (
        <>
            <Box component="form" onSubmit={handleSubmit} sx={{ maxWidth: 400, margin: 'auto' }}>
                <Typography variant="h4" component="h1" gutterBottom>
                    Log In
                </Typography>
                <TextField
                    fullWidth
                    margin="normal"
                    label="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                <TextField
                    fullWidth
                    margin="normal"
                    label="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                {(diplayError || error) && (
                    <Typography color="error" sx={{ mt: 2 }}>
                        {(diplayError || error)}
                    </Typography>
                )}
                <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                    sx={{ mt: 3 }}
                >
                    Log In
                </Button>
            </Box>
        </>
    )
}

export default LoginForm;
