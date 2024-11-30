import React, { useState } from 'react';
import { registerUser , loginUser  } from './services/api'; // Adjust the path as necessary

const AuthComponent = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');

    const handleRegister = async () => {
        try {
            const response = await registerUser (username, password);
            setMessage(response.message);
        } catch (error) {
            setMessage("Registration failed!");
        }
    };

    const handleLogin = async () => {
        try {
            const response = await loginUser (username, password);
            setMessage(response.message);
        } catch (error) {
            setMessage("Login failed!");
        }
    };

    return (
        <div>
            <h1>Authentication</h1>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleRegister}>Register</button>
            <button onClick={handleLogin}>Login</button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default AuthComponent;