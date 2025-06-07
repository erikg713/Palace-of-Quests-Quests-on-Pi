/**
 * Professional Pi Network Integration Service
 * Handles authentication, payments, and blockchain interactions with proper error handling
 * 
 * @author Erik G. - Palace of Quests Development Team
 * @version 2.1.0
 * @since 2025-06-05
 */

import { Pi } from '@pinetwork-js/sdk';
import { EventEmitter } from 'events';
import CryptoJS from 'crypto-js';

class PiNetworkService extends EventEmitter {
    constructor() {
        super();
        this.isInitialized = false;
        this.isAuthenticated = false;
        this.userSession = null;
        this.pendingPayments = new Map();
        this.retryAttempts = 3;
        this.baseRetryDelay = 1000;
        
        this.initializeSDK();
    }

    /**
     * Initialize Pi Network SDK with enhanced error handling
     */
    async initializeSDK() {
        try {
            const config = {
                version: '2.0',
                sandbox: process.env.REACT_APP_PI_SANDBOX === 'true',
                timeout: 30000, // 30 second timeout
                enableLogging: process.env.NODE_ENV === 'development'
            };

            await Pi.init(config);
            this.isInitialized = true;
            
            console.info('🎯 Pi Network SDK initialized successfully', {
                sandbox: config.sandbox,
                version: config.version,
                timestamp: new Date().toISOString()
            });
            
            this.emit('sdk_initialized', config);
            
            // Auto-check authentication status
            await this.checkAuthenticationStatus();
            
        } catch (error) {
            console.error('❌ Failed to initialize Pi Network SDK:', error);
            this.emit('sdk_error', { 
                type: 'initialization', 
                error: error.message,
                timestamp: new Date().toISOString()
            });
            
            // Retry initialization with exponential backoff
            setTimeout(() => this.initializeSDK(), this.baseRetryDelay);
        }
    }

    /**
     * Check current authentication status
     */
    async checkAuthenticationStatus() {
        try {
            if (!this.isInitialized) {
                throw new Error('SDK not initialized');
            }

            const authStatus = await Pi.getAuthStatus();
            this.isAuthenticated = authStatus?.authenticated || false;
            
            if (this.isAuthenticated && authStatus.user) {
                this.userSession = {
                    uid: authStatus.user.uid,
                    username: authStatus.user.username,
                    accessToken: authStatus.accessToken,
                    authenticatedAt: new Date().toISOString(),
                    sessionExpires: this.calculateSessionExpiry()
                };
                
                this.emit('authentication_verified', this.userSession);
            }
            
            return this.isAuthenticated;
            
        } catch (error) {
            console.warn('🔍 Could not verify authentication status:', error.message);
            return false;
        }
    }

    /**
     * Authenticate user with comprehensive flow management
     */
    async authenticateUser(scopes = ['username', 'payments']) {
        return new Promise((resolve, reject) => {
            if (!this.isInitialized) {
                reject(new Error('Pi Network SDK not initialized'));
                return;
            }

            const authStartTime = Date.now();
            
            const authOptions = {
                scopes,
                onIncompletePaymentFound: (payment) => {
                    console.info('🔄 Incomplete payment found:', payment.identifier);
                    this.handleIncompletePayment(payment);
                }
            };

            Pi.authenticate(authOptions, (authResult) => {
                try {
                    const authDuration = Date.now() - authStartTime;
                    
                    if (authResult && authResult.user) {
                        this.isAuthenticated = true;
                        this.userSession = {
                            uid: authResult.user.uid,
                            username: authResult.user.username,
                            displayName: authResult.user.username,
                            accessToken: authResult.accessToken,
                            scopes: scopes,
                            authenticatedAt: new Date().toISOString(),
                            sessionExpires: this.calculateSessionExpiry(),
                            authDuration: authDuration
                        };

                        console.info('✅ User authenticated successfully:', {
                            username: this.userSession.username,
                            duration: `${authDuration}ms`,
                            scopes: scopes
                        });

                        this.emit('user_authenticated', this.userSession);
                        resolve(this.userSession);
                        
                        // Store session securely
                        this.storeSessionData();
                        
                    } else {
                        throw new Error('Authentication failed - no user data received');
                    }
                } catch (error) {
                    this.handleAuthenticationError(error, reject);
                }
            }, (error) => {
                this.handleAuthenticationError(error, reject);
            });
        });
    }

    /**
     * Create a payment with enhanced validation and tracking
     */
    async createPayment(paymentData) {
        return new Promise((resolve, reject) => {
            if (!this.isAuthenticated) {
                reject(new Error('User must be authenticated to create payments'));
                return;
            }

            const {
                amount,
                memo,
                metadata = {},
                userId,
                itemId,
                transactionType = 'purchase'
            } = paymentData;

            // Validate payment data
            const validation = this.validatePaymentData(paymentData);
            if (!validation.isValid) {
                reject(new Error(`Payment validation failed: ${validation.errors.join(', ')}`));
                return;
            }

            const paymentId = this.generatePaymentId();
            const enhancedMetadata = {
                ...metadata,
                userId,
                itemId,
                transactionType,
                initiatedAt: new Date().toISOString(),
                clientVersion: process.env.REACT_APP_VERSION || '1.0.0',
                sessionId: this.userSession?.sessionId,
                checksum: this.generatePaymentChecksum(amount, memo, userId)
            };

            const paymentConfig = {
                amount: parseFloat(amount),
                memo: memo.substring(0, 140), // Pi Network memo limit
                metadata: enhancedMetadata
            };

            console.info('💰 Initiating payment:', {
                paymentId,
                amount: paymentConfig.amount,
                memo: paymentConfig.memo,
                transactionType
            });

            const callbacks = {
                onReadyForServerApproval: (paymentId) => {
                    console.info('⏳ Payment ready for server approval:', paymentId);
                    this.pendingPayments.set(paymentId, {
                        ...paymentConfig,
                        status: 'server_approval',
                        createdAt: Date.now()
                    });
                    
                    this.emit('payment_server_approval', { paymentId, ...paymentConfig });
                },

                onReadyForServerCompletion: (paymentId, txid) => {
                    console.info('🎯 Payment ready for server completion:', { paymentId, txid });
                    
                    const payment = this.pendingPayments.get(paymentId);
                    if (payment) {
                        payment.status = 'server_completion';
                        payment.transactionId = txid;
                        payment.completionReadyAt = Date.now();
                    }
                    
                    this.emit('payment_server_completion', { paymentId, txid, ...paymentConfig });
                },

                onCancel: (paymentId) => {
                    console.warn('❌ Payment cancelled by user:', paymentId);
                    this.pendingPayments.delete(paymentId);
                    
                    this.emit('payment_cancelled', { paymentId, reason: 'user_cancelled' });
                    reject(new Error('Payment cancelled by user'));
                },

                onError: (error, payment) => {
                    console.error('💥 Payment error:', error);
                    
                    if (payment?.identifier) {
                        this.pendingPayments.delete(payment.identifier);
                    }
                    
                    this.emit('payment_error', { error, payment });
                    reject(error);
                }
            };

            try {
                Pi.createPayment(paymentConfig, callbacks);
                
                // Set up payment timeout
                setTimeout(() => {
                    if (this.pendingPayments.has(paymentId)) {
                        console.warn('⏰ Payment timeout:', paymentId);
                        this.pendingPayments.delete(paymentId);
                        this.emit('payment_timeout', { paymentId });
                    }
                }, 300000); // 5 minute timeout
                
                resolve({ paymentId, status: 'initiated' });
                
            } catch (error) {
                console.error('🚫 Failed to create payment:', error);
                reject(error);
            }
        });
    }

    /**
     * Verify payment completion with backend
     */
    async verifyPayment(paymentId) {
        try {
            const response = await fetch('/api/payments/verify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.userSession?.accessToken}`
                },
                body: JSON.stringify({ 
                    paymentId,
                    userId: this.userSession?.uid,
                    timestamp: new Date().toISOString()
                })
            });

            if (!response.ok) {
                throw new Error(`Payment verification failed: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.verified) {
                console.info('✅ Payment verified successfully:', paymentId);
                this.pendingPayments.delete(paymentId);
                this.emit('payment_verified', result);
            } else {
                console.error('❌ Payment verification failed:', result.reason);
                this.emit('payment_verification_failed', result);
            }

            return result;

        } catch (error) {
            console.error('🔍 Payment verification error:', error);
            this.emit('payment_verification_error', { paymentId, error: error.message });
            throw error;
        }
    }

    /**
     * Handle incomplete payments found during authentication
     */
    async handleIncompletePayment(payment) {
        try {
            console.info('🔄 Processing incomplete payment:', payment.identifier);
            
            const verificationResult = await this.verifyPayment(payment.identifier);
            
            if (verificationResult.verified) {
                console.info('✅ Incomplete payment successfully verified:', payment.identifier);
            } else {
                console.warn('⚠️ Incomplete payment could not be verified:', payment.identifier);
            }
            
        } catch (error) {
            console.error('💥 Error handling incomplete payment:', error);
        }
    }

    /**
     * Validate payment data before submission
     */
    validatePaymentData(paymentData) {
        const errors = [];
        const { amount, memo, userId } = paymentData;

        if (!amount || amount <= 0) {
            errors.push('Amount must be greater than 0');
        }

        if (!memo || memo.trim().length === 0) {
            errors.push('Payment memo is required');
        }

        if (memo && memo.length > 140) {
            errors.push('Payment memo exceeds 140 character limit');
        }

        if (!userId) {
            errors.push('User ID is required');
        }

        // Check for suspicious patterns
        if (amount > 10000) {
            errors.push('Payment amount exceeds maximum allowed limit');
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Generate unique payment identifier
     */
    generatePaymentId() {
        const timestamp = Date.now();
        const random = Math.random().toString(36).substring(2);
        return `pq_${timestamp}_${random}`;
    }

    /**
     * Generate payment checksum for verification
     */
    generatePaymentChecksum(amount, memo, userId) {
        const data = `${amount}:${memo}:${userId}:${Date.now()}`;
        return CryptoJS.SHA256(data).toString();
    }

    /**
     * Calculate session expiry time
     */
    calculateSessionExpiry() {
        const now = new Date();
        const expiry = new Date(now.getTime() + (24 * 60 * 60 * 1000)); // 24 hours
        return expiry.toISOString();
    }

    /**
     * Store session data securely
     */
    storeSessionData() {
        if (this.userSession) {
            const sessionData = {
                ...this.userSession,
                storedAt: new Date().toISOString()
            };
            
            // Store in secure storage (not localStorage for sensitive data)
            sessionStorage.setItem('pi_session', JSON.stringify(sessionData));
        }
    }

    /**
     * Handle authentication errors with proper logging
     */
    handleAuthenticationError(error, reject) {
        console.error('🔐 Authentication error:', error);
        
        this.isAuthenticated = false;
        this.userSession = null;
        
        this.emit('authentication_error', {
            error: error.message,
            timestamp: new Date().toISOString()
        });
        
        reject(error);
    }

    /**
     * Get current user session
     */
    getUserSession() {
        return this.userSession;
    }

    /**
     * Check if user is currently authenticated
     */
    isUserAuthenticated() {
        return this.isAuthenticated && this.userSession !== null;
    }

    /**
     * Get pending payments
     */
    getPendingPayments() {
        return Array.from(this.pendingPayments.entries()).map(([id, payment]) => ({
            id,
            ...payment
        }));
    }

    /**
     * Sign out user and cleanup session
     */
    async signOut() {
        try {
            if (this.isAuthenticated) {
                console.info('👋 Signing out user:', this.userSession?.username);
                
                this.isAuthenticated = false;
                this.userSession = null;
                this.pendingPayments.clear();
                
                // Clear stored session data
                sessionStorage.removeItem('pi_session');
                
                this.emit('user_signed_out');
                
                return true;
            }
        } catch (error) {
            console.error('Error during sign out:', error);
            return false;
        }
    }
}

// Create singleton instance
const piNetworkService = new PiNetworkService();
export default piNetworkService;

// Export additional utilities
export const PiNetworkUtils = {
    formatPiAmount: (amount) => {
        return new Intl.NumberFormat('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 6
        }).format(amount) + ' π';
    },
    
    validatePiAmount: (amount) => {
        return !isNaN(amount) && amount > 0 && amount <= 10000;
    }
};
