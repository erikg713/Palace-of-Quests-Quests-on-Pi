// logger.js

const levels = {
    INFO: 'INFO',
    WARN: 'WARN',
    ERROR: 'ERROR',
    DEBUG: 'DEBUG',
};

/**
 * Logs a message to the console with a specific level and context
 * @param {string} level - Log level (INFO, WARN, ERROR, DEBUG)
 * @param {string} message - Log message
 * @param {Object} [context] - Additional context or data to log
 */
const log = (level, message, context = null) => {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] [${level}] ${message}`;

    if (context) {
        console[level.toLowerCase()](logMessage, context);
    } else {
        console[level.toLowerCase()](logMessage);
    }
};

/**
 * Logs an informational message
 * @param {string} message - Log message
 * @param {Object} [context] - Additional context or data to log
 */
export const info = (message, context = null) => {
    log(levels.INFO, message, context);
};

/**
 * Logs a warning message
 * @param {string} message - Log message
 * @param {Object} [context] - Additional context or data to log
 */
export const warn = (message, context = null) => {
    log(levels.WARN, message, context);
};

/**
 * Logs an error message
 * @param {string} message - Log message
 * @param {Object} [context] - Additional context or data to log
 */
export const error = (message, context = null) => {
    log(levels.ERROR, message, context);
};

/**
 * Logs a debug message
 * @param {string} message - Log message
 * @param {Object} [context] - Additional context or data to log
 */
export const debug = (message, context = null) => {
    log(levels.DEBUG, message, context);
};
