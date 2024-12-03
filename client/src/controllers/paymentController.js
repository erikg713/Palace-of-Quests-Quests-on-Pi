// paymentController.js

import axios from 'axios';

// Payment API endpoint
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Initiates a payment request with the Pi Network SDK
 * @param {string} userId - User's unique ID
 * @param {number} amount - Payment amount in Pi
 * @param {string} description - Payment description
 * @returns {Promise<object>} - Payment response from the backend
 */
export const initiatePayment = async (userId, amount, description) => {
    try {
        const response = await axios.post(`${BASE_URL}/payments/initiate`, {
            userId,
            amount,
            description,
        });
        return response.data;
    } catch (error) {
        console.error('Error initiating payment:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Verifies a completed payment
 * @param {string} paymentId - Payment identifier
 * @returns {Promise<object>} - Verification response from the backend
 */
export const verifyPayment = async (paymentId) => {
    try {
        const response = await axios.post(`${BASE_URL}/payments/verify`, {
            paymentId,
        });
        return response.data;
    } catch (error) {
        console.error('Error verifying payment:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Fetches the user's transaction history
 * @param {string} userId - User's unique ID
 * @returns {Promise<array>} - List of transactions
 */
export const getTransactionHistory = async (userId) => {
    try {
        const response = await axios.get(`${BASE_URL}/payments/history/${userId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching transaction history:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Handles payment cancellation
 * @param {string} paymentId - Payment identifier
 * @returns {Promise<object>} - Cancellation response from the backend
 */
export const cancelPayment = async (paymentId) => {
    try {
        const response = await axios.post(`${BASE_URL}/payments/cancel`, {
            paymentId,
        });
        return response.data;
    } catch (error) {
        console.error('Error cancelling payment:', error);
        throw error.response ? error.response.data : error.message;
    }
};
