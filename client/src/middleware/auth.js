// auth.js

/**
 * Authentication Middleware
 * Handles attaching authentication tokens to API requests and managing authentication errors.
 */

import axios from 'axios';
import { store } from '../store';
import { logoutUser, setUser } from '../slices/userSlice';
import { Navigate } from 'react-router-dom';

/**
 * Create an Axios instance with default configurations.
 * This instance will be used for all API requests requiring authentication.
 */
const api = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL || 'https://api.palaceofquests.com', // Replace with your API base URL
    headers: {
        'Content-Type': 'application/json',
    },
    // You can add more default configurations here if needed
});

/**
 * Request Interceptor
 * Attaches the JWT token from localStorage to the Authorization header of each request.
 */
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // Handle request errors here
        return Promise.reject(error);
    }
);

/**
 * Response Interceptor
 * Handles global responses, such as unauthorized access, and refreshes tokens if necessary.
 */
api.interceptors.response.use(
    (response) => response,
    (error) => {
        const originalRequest = error.config;

        // If the error response status is 401 (Unauthorized) and the request hasn't been retried yet
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            // Optionally, implement token refresh logic here
            // For example, call a refresh token endpoint to get a new token

            // If token refresh fails or is not implemented, logout the user
            store.dispatch(logoutUser());
            window.location.href = '/login'; // Redirect to login page

            return Promise.reject(error);
        }

        // Handle other error statuses as needed
        return Promise.reject(error);
    }
);

/**
 * Function to set the authentication token.
 * Stores the token in localStorage and updates the Axios instance.
 * @param {string} token - JWT authentication token.
 */
export const setAuthToken = (token) => {
    if (token) {
        localStorage.setItem('authToken', token);
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
        localStorage.removeItem('authToken');
        delete api.defaults.headers.common['Authorization'];
    }
};

/**
 * Function to logout the user.
 * Clears the authentication token and updates the Redux store.
 */
export const logout = () => {
    setAuthToken(null);
    store.dispatch(logoutUser());
    window.location.href = '/login'; // Redirect to login page
};

/**
 * Example Function: Fetch Current User Profile
 * Utilizes the Axios instance to fetch the authenticated user's profile.
 * Dispatches actions to update the Redux store based on the response.
 */
export const fetchCurrentUser = async () => {
    try {
        const response = await api.get('/users/profile'); // Replace with your API endpoint
        store.dispatch(setUser(response.data));
    } catch (error) {
        console.error('Failed to fetch user profile:', error);
        // Optionally, handle specific error scenarios here
    }
};

/**
 * Export the Axios instance for use in controllers and other parts of the application.
 */
export default api;
