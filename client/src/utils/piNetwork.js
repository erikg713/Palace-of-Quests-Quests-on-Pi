// client/src/utils/piNetwork.js

import { Pi } from '@pinetwork-js/sdk';

const PI_VERSION = '2.0';
const SANDBOX = process.env.REACT_APP_PI_SANDBOX === 'true';
const API_URL = (process.env.REACT_APP_API_URL || '').replace(/\/$/, '');

/**
 * Simple logger for consistent debugging.
 */
function log(type, ...args) {
  if (type === 'error') {
    console.error('[PiNetwork]', ...args);
  } else if (type === 'warn') {
    console.warn('[PiNetwork]', ...args);
  } else {
    console.log('[PiNetwork]', ...args);
  }
}

/**
 * Initialize Pi Network SDK.
 * Call this early in your app, e.g. in App.js.
 * @throws {Error} If Pi SDK initialization fails.
 */
export function initializePiNetwork() {
  try {
    Pi.init({
      version: PI_VERSION,
      sandbox: SANDBOX,
    });
    log('info', 'SDK initialized (sandbox:', SANDBOX, ')');
  } catch (err) {
    log('error', 'SDK initialization failed:', err);
    throw err;
  }
}

/**
 * Authenticate user via Pi Network.
 * @param {Function} [onSuccess] - Called with authData on success.
 * @param {Function} [onError] - Called with error on failure.
 * @returns {Promise<object>} Resolves with authData if no callbacks are provided.
 */
export function authenticateUser(onSuccess, onError) {
  return new Promise((resolve, reject) => {
    try {
      Pi.authenticate(
        (authData) => {
          log('info', 'User authenticated:', authData);
          onSuccess?.(authData);
          resolve(authData);
        },
        (error) => {
          log('error', 'Authentication failed:', error);
          onError?.(error);
          reject(error);
        }
      );
    } catch (err) {
      log('error', 'Error during authentication:', err);
      onError?.(err);
      reject(err);
    }
  });
}

/**
 * Create a Pi payment.
 * @param {object} params
 * @param {string} params.userId - User ID.
 * @param {number} params.amount - Payment amount in Pi.
 * @param {string} params.memo - Description of payment.
 * @param {Function} [onSuccess] - Callback for successful payment.
 * @param {Function} [onError] - Callback for payment failure.
 * @returns {Promise<object>} Resolves with payment on success.
 */
export function createPayment({ userId, amount, memo }, onSuccess, onError) {
  if (!userId || typeof amount !== 'number' || !memo) {
    const err = { type: 'validation', message: 'Invalid payment params' };
    log('error', err.message, { userId, amount, memo });
    onError?.(err);
    return Promise.reject(err);
  }

  return new Promise((resolve, reject) => {
    try {
      Pi.createPayment(
        {
          amount,
          memo,
          metadata: { userId },
        },
        {
          onReadyForServerApproval: (paymentId) => {
            log('info', 'Ready for server approval:', paymentId);
          },
          onReadyForServerCompletion: (paymentId, txId) => {
            log('info', 'Ready for server completion:', { paymentId, txId });
          },
          onCancel: (paymentId) => {
            const err = { type: 'cancel', paymentId };
            log('warn', 'Payment cancelled:', paymentId);
            onError?.(err);
            reject(err);
          },
          onError: (error) => {
            log('error', 'Payment error:', error);
            onError?.(error);
            reject(error);
          },
          onSuccess: (payment) => {
            log('info', 'Payment successful:', payment);
            onSuccess?.(payment);
            resolve(payment);
          },
        }
      );
    } catch (err) {
      log('error', 'Error creating payment:', err);
      onError?.(err);
      reject(err);
    }
  });
}

/**
 * Verify a payment.
 * @param {string} paymentId - ID of the payment to verify.
 * @param {Function} [onSuccess] - Callback on successful verification.
 * @param {Function} [onError] - Callback on verification failure.
 * @returns {Promise<object>} Resolves with verification result.
 */
export async function verifyPayment(paymentId, onSuccess, onError) {
  if (!paymentId) {
    const err = { type: 'validation', message: 'Payment ID required' };
    log('error', err.message);
    onError?.(err);
    return Promise.reject(err);
  }
  if (!API_URL) {
    const err = { type: 'configuration', message: 'API_URL not set' };
    log('error', err.message);
    onError?.(err);
    return Promise.reject(err);
  }

  try {
    const response = await fetch(`${API_URL}/payments/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ paymentId }),
    });
    const result = await response.json();
    if (response.ok) {
      log('info', 'Payment verified:', result);
      onSuccess?.(result);
      return result;
    } else {
      log('error', 'Payment verification failed:', result);
      onError?.(result);
      throw result;
    }
  } catch (err) {
    log('error', 'Error verifying payment:', err);
    onError?.(err);
    throw err;
  }
}
