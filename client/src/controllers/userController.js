// userController.js

import axios from 'axios';

// API Base URL
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Fetch all users
 * @returns {Promise<Array>} - List of all users
 */
export const getAllUsers = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/users`);
        return response.data;
    } catch (error) {
        console.error('Error fetching users:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Fetch user by ID
 * @param {string} userId - ID of the user
 * @returns {Promise<Object>} - User details
 */
export const getUserById = async (userId) => {
    try {
        const response = await axios.get(`${BASE_URL}/users/${userId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching user:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Register a new user
 * @param {Object} userData - Data of the user to register
 * @returns {Promise<Object>} - Registered user details
 */
export const registerUser = async (userData) => {
    try {
        const response = await axios.post(`${BASE_URL}/users/register`, userData);
        return response.data;
    } catch (error) {
        console.error('Error registering user:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Login a user
 * @param {Object} credentials - User login credentials
 * @returns {Promise<Object>} - Login response with user details and token
 */
export const loginUser = async (credentials) => {
    try {
        const response = await axios.post(`${BASE_URL}/users/login`, credentials);
        return response.data;
    } catch (error) {
        console.error('Error logging in user:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Update user information
 * @param {string} userId - ID of the user to update
 * @param {Object} userData - Updated user data
 * @returns {Promise<Object>} - Updated user details
 */
export const updateUser = async (userId, userData) => {
    try {
        const response = await axios.put(`${BASE_URL}/users/${userId}`, userData);
        return response.data;
    } catch (error) {
        console.error('Error updating user:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Delete a user
 * @param {string} userId - ID of the user to delete
 * @returns {Promise<Object>} - Confirmation of deletion
 */
export const deleteUser = async (userId) => {
    try {
        const response = await axios.delete(`${BASE_URL}/users/${userId}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting user:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Fetch user's transaction history
 * @param {string} userId - User's unique ID
 * @returns {Promise<Array>} - List of user transactions
 */
export const getUserTransactionHistory = async (userId) => {
    try {
        const response = await axios.get(`${BASE_URL}/users/${userId}/transactions`);
        return response.data;
    } catch (error) {
        console.error('Error fetching user transactions:', error);
        throw error.response ? error.response.data : error.message;
    }
};
