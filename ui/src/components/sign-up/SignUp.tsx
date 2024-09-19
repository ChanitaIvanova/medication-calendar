import React, { useState } from 'react';
import SignUpForm from './SignUpForm';
import { useNavigate } from "react-router-dom";
import { userService } from '../../services/userService';

const SignUp: React.FC = () => {
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    const navigate = useNavigate();

    const handleSignUp = async (email: string, username: string, password: string) => {
        try {
            await userService.signUp(email, username, password);
            setLoading(false);
            navigate('/');
        } catch (err) {
            console.log(err);
            setError(err.response?.data?.error || 'An error occurred');
            setLoading(false);
        }
    };

    if (loading) {
        return <p>Loading...</p>;
    }

    return (
        <SignUpForm onSignUp={handleSignUp} error={error} />
    );
};

export default SignUp;