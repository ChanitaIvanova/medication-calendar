import React, { useState } from 'react';
import LoginForm from './LoginForm';
import { useNavigate } from "react-router-dom";
import { useUser } from '../../context/UserContext';
import { userService } from '../../services/userService';
import { UserProvider } from '../../context/UserContext';

const Login: React.FC = () => {
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const { setUser } = useUser();

    const navigate = useNavigate();

    const handleLogin = async (username: string, password: string) => {
        try {
            const user = await userService.login(username, password);
            setUser(user);
            setLoading(false);
            navigate('/');
        } catch (err: any) {
            console.log(err);
            setError(err.response?.data?.error || 'An error occurred');
            setLoading(false);
        }
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <UserProvider><LoginForm onLogin={handleLogin} error={error} /></UserProvider>
    );
};

export default Login;