/**
 * Formats a given date into a readable string with customizable options.
 *
 * @param {string | Date} date - The date to be formatted.
 * @param {Object} [options={}] - Formatting options for locale or output style.
 * @param {string} [locale='en-US'] - Locale string for formatting.
 * @returns {string} - A formatted date string.
 */
export const formatDate = (date, options = {}, locale = 'en-US') => {
    try {
        const parsedDate = new Date(date);
        if (isNaN(parsedDate)) {
            throw new Error('Invalid date');
        }
        // Default options for formatting
        const defaultOptions = { year: 'numeric', month: 'long', day: 'numeric' };
        return parsedDate.toLocaleDateString(locale, { ...defaultOptions, ...options });
    } catch (error) {
        console.error('Error formatting date:', error.message);
        return 'Invalid Date';
    }
};
