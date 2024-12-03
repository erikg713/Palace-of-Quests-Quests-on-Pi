// constants.js

// API Endpoints
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Pi Network Settings
export const PI_NETWORK_SANDBOX = process.env.REACT_APP_PI_SANDBOX === 'true';

// Application Details
export const APP_NAME = 'Palace of Quests';
export const APP_VERSION = '1.0.0';

// Subscription Plans
export const SUBSCRIPTION_PLANS = {
    PREMIUM: {
        price: 9.99,
        duration: '1 year',
        perks: [
            'Access to all premium levels (50, 100, 150, 200, 250)',
            'Exclusive avatar upgrades',
            'Priority support',
        ],
    },
};

// Game Levels
export const GAME_LEVELS = {
    MAX_LEVEL: 250,
    PREMIUM_UNLOCK_LEVELS: [50, 100, 150, 200, 250],
};

// Payment Configuration
export const PAYMENT = {
    CURRENCY: 'Pi',
    DEFAULT_MEMO: 'Palace of Quests transaction',
};

// Logging Levels
export const LOG_LEVELS = {
    INFO: 'INFO',
    WARN: 'WARN',
    ERROR: 'ERROR',
    DEBUG: 'DEBUG',
};

// Default Messages
export const MESSAGES = {
    AUTH_ERROR: 'Authentication failed. Please try again.',
    PAYMENT_SUCCESS: 'Payment processed successfully!',
    PAYMENT_ERROR: 'There was an error processing your payment.',
    FETCH_ERROR: 'Failed to fetch data. Please check your connection.',
};

// Game Events
export const EVENTS = {
    CHAMBER_QUEST: {
        name: 'The Chamber to Guilded Quests',
        description: 'Battle to conquer gold, land, and castles!',
    },
    BACK_CASTLE_QUEST: {
        name: 'Back Castle Survivor Series',
        description: 'Solve puzzles and compete to survive!',
    },
};

// Environment Variables (for debugging)
export const ENV = {
    NODE_ENV: process.env.NODE_ENV,
    IS_PRODUCTION: process.env.NODE_ENV === 'production',
    IS_DEVELOPMENT: process.env.NODE_ENV === 'development',
};
