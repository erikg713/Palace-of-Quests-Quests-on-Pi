// piNetwork.js

import { Pi } from '@pinetwork-js/sdk';

const initializePiNetwork = () => {
    try {
        Pi.init({
            version: '2.0',
            sandbox: process.env.REACT_APP_PI_SANDBOX === 'true',
        });
        console.log('Pi Network SDK initialized successfully');
    } catch (error) {
        console.error('Failed to initialize Pi Network SDK:', error);
    }
};

/**
 * Authenticate a user via Pi Network
 * @param {Function} onSuccess - Callback on successful authentication
 * @param {Function} onError - Callback on authentication failure
 */
export const authenticateUser = (onSuccess, onError) => {
    try {
        Pi.authenticate(
            (authData) => {
                console.log('User authenticated:', authData);
                if (onSuccess) onSuccess(authData);
            },
            (error) => {
                console.error('Authentication failed:', error);
                if (onError) onError(error);
            }
        );
    } catch (error) {
        console.error('Error during authentication:', error);
        if (onError) onError(error);
    }
};

/**
 * Create a Pi payment
 * @param {string} userId - User ID
 * @param {number} amount - Payment amount in Pi
 * @param {string} memo - Description of the payment
 * @param {Function} onSuccess - Callback on successful payment
 * @param {Function} onError - Callback on payment failure
 */
export const createPayment = (userId, amount, memo, onSuccess, onError) => {
    try {
        Pi.createPayment(
            {
                amount,
                memo,
                metadata: { userId },
            },
            {
                onReadyForServerApproval: (paymentId) => {
                    console.log('Payment ready for server approval:', paymentId);
                },
                onReadyForServerCompletion: (paymentId, txId) => {
                    console.log('Payment ready for server completion:', { paymentId, txId });
                },
                onCancel: (paymentId) => {
                    console.warn('Payment cancelled:', paymentId);
                    if (onError) onError({ type: 'cancel', paymentId });
                },
                onError: (error) => {
                    console.error('Payment error:', error);
                    if (onError) onError(error);
                },
                onSuccess: (payment) => {
                    console.log('Payment successful:', payment);
                    if (onSuccess) onSuccess(payment);
                },
            }
        );
    } catch (error) {
        console.error('Error creating payment:', error);
        if (onError) onError(error);
    }
};

/**
 * Verify a payment
 * @param {string} paymentId - ID of the payment to verify
 * @param {Function} onSuccess - Callback on successful verification
 * @param {Function} onError - Callback on verification failure
 */
export const verifyPayment = async (paymentId, onSuccess, onError) => {
    try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/payments/verify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paymentId }),
        });
        const result = await response.json();

        if (response.ok) {
            console.log('Payment verified:', result);
            if (onSuccess) onSuccess(result);
        } else {
            console.error('Payment verification failed:', result);
            if (onError) onError(result);
        }
    } catch (error) {
        console.error('Error verifying payment:', error);
        if (onError) onError(error);
    }
};

// Initialize Pi Network SDK on app load
initializePiNetwork();
