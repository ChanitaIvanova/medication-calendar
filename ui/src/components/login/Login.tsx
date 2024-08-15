import React, { useState } from 'react';
import axios from 'axios';
import LoginForm from './LoginForm';
import { useNavigate } from "react-router-dom";
import User from '../../types/User'
import { UserProvider, useUser } from '../../context/UserContext';

interface LoginData {
    username: string;
    password: string;
}

const Login: React.FC = () => {
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const { setUser } = useUser();

    const navigate = useNavigate();

    const handleLogin = (username: string, password: string) => {
        axios
            .post<User>('http://127.0.0.1:9000/api/auth/login', { username: username, password: password })
            .then((response) => {
                setUser(response.data);
                setLoading(false);
                navigate('/');
            })
            .catch((err) => {
                console.log(err)
                setError(err.response.data.error);
                setLoading(false);
            });
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <UserProvider><LoginForm onLogin={handleLogin} error={error} /></UserProvider>
    );
};

export default Login