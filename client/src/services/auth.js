import API from "./api";

/**
 * Authenticate user with email and password.
 * @param {string} email
 * @param {string} password
 * @returns {Promise<Object>} Authenticated user data
 * @throws {Error} If login fails
 */
export async function login(email, password) {
    try {
        const { data } = await API.post("/auth/login", { email, password });
        return data;
    } catch (err) {
        // Provide clear error feedback for UI or logging
        const message =
            err.response?.data?.message ||
            err.response?.data?.error ||
            err.message ||
            "Login failed";
        throw new Error(message);
    }
}

/**
 * Register a new user with provided details.
 * @param {Object} userDetails
 * @returns {Promise<Object>} Registered user data
 * @throws {Error} If registration fails
 */
export async function register(userDetails) {
    try {
        const { data } = await API.post("/auth/register", userDetails);
        return data;
    } catch (err) {
        const message =
            err.response?.data?.message ||
            err.response?.data?.error ||
            err.message ||
            "Registration failed";
        throw new Error(message);
    }
}
