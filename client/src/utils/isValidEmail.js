/**
 * Validates if the input is a properly formatted email address.
 * @param {string} email - The email address to validate.
 * @returns {boolean} - Returns true if the email is valid, false otherwise.
 */
const isValidEmail = (email) => {
    if (typeof email !== 'string') {
        return false; // Invalid input type
    }
    // Regex for validating email format
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailRegex.test(email);
};

export default isValidEmail;
