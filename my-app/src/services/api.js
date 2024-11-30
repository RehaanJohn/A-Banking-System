import axios from 'axios';

// Base URL for the API
const API_URL = 'http://localhost:5000';

// Function to register a new user
export const registerUser  = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/register`, {
            username,
            password
        });
        return response.data; // Return the response data
    } catch (error) {
        console.error("There was an error registering!", error);
        throw error; // Rethrow the error for further handling
    }
};

// Function to log in a user
export const loginUser  = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/login`, {
            username,
            password
        });
        return response.data; // Return the response data
    } catch (error) {
        console.error("There was an error logging in!", error);
        throw error; // Rethrow the error for further handling
    }
};