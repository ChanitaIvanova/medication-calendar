import React, { useState } from 'react';
import axios from 'axios';
import SignUpForm from './SignUpForm';
import { useNavigate } from "react-router-dom";
import User from '../../types/User'

const Login: React.FC = () => {
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const navigate = useNavigate();

    const handleSignUp = (email: string, username: string, password: string) => {
        axios
            .post<User>('http://127.0.0.1:9000/api/auth/sign-up', { email: email, username: username, password: password })
            .then(() => {
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
        <SignUpForm onSignUp={handleSignUp} error={error} />
    );
};

export default Login