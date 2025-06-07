// constants.js

// ========== API Configuration ==========
export const API_BASE_URL =
  process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// ========== Pi Network Settings ==========
export const PI_NETWORK_SANDBOX =
  process.env.REACT_APP_PI_SANDBOX === 'true';

// ========== Application Metadata ==========
export const APP_NAME = 'Palace of Quests';
export const APP_VERSION = process.env.REACT_APP_APP_VERSION || '1.0.0';

// ========== Subscription Plans ==========
const defaultPremiumPerks = [
  'Access to all premium levels (50, 100, 150, 200, 250)',
  'Exclusive avatar upgrades',
  'Priority support',
];

export const SUBSCRIPTION_PLANS = {
  PREMIUM: {
    price: Number(process.env.REACT_APP_PREMIUM_PRICE) || 9.99,
    duration: process.env.REACT_APP_PREMIUM_DURATION || '1 year',
    perks: process.env.REACT_APP_PREMIUM_PERKS
      ? process.env.REACT_APP_PREMIUM_PERKS.split('|').map(p => p.trim())
      : defaultPremiumPerks,
  },
};

// ========== Game Levels ==========
const PREMIUM_UNLOCK_LEVELS = [50, 100, 150, 200, 250];

export const GAME_LEVELS = {
  MAX_LEVEL: Math.max(...PREMIUM_UNLOCK_LEVELS),
  PREMIUM_UNLOCK_LEVELS,
};

// ========== Payment Configuration ==========
export const PAYMENT = {
  CURRENCY: process.env.REACT_APP_PAYMENT_CURRENCY || 'Pi',
  DEFAULT_MEMO:
    process.env.REACT_APP_PAYMENT_MEMO || 'Palace of Quests transaction',
};

// ========== Logging Levels ==========
export const LOG_LEVELS = Object.freeze({
  INFO: 'INFO',
  WARN: 'WARN',
  ERROR: 'ERROR',
  DEBUG: 'DEBUG',
});

// ========== Messages ==========
export const MESSAGES = Object.freeze({
  AUTH_ERROR: 'Authentication failed. Please try again.',
  PAYMENT_SUCCESS: 'Payment processed successfully!',
  PAYMENT_ERROR: 'There was an error processing your payment.',
  FETCH_ERROR: 'Failed to fetch data. Please check your connection.',
});

// ========== Game Events ==========
export const EVENTS = Object.freeze({
  CHAMBER_QUEST: {
    name: 'The Chamber to Guilded Quests',
    description: 'Battle to conquer gold, land, and castles!',
  },
  BACK_CASTLE_QUEST: {
    name: 'Back Castle Survivor Series',
    description: 'Solve puzzles and compete to survive!',
  },
});

// ========== Environment ==========
export const ENV = Object.freeze({
  NODE_ENV: process.env.NODE_ENV,
  IS_PRODUCTION: process.env.NODE_ENV === 'production',
  IS_DEVELOPMENT: process.env.NODE_ENV === 'development',
});
