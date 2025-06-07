import axios from "axios";

// Create an axios instance with a base URL and default configurations
const API = axios.create({
    baseURL: "http://localhost:5000/api",
    timeout: 10000, // Add a timeout to prevent hanging requests
    headers: {
        "Content-Type": "application/json",
    },
});

// Interceptor for handling request errors
API.interceptors.response.use(
    (response) => response,
    (error) => {
        console.error("API Error:", error?.response?.data || error.message);
        return Promise.reject(error?.response?.data || error.message);
    }
);

/**
 * Log in the user with their email and password
 * @param {string} email - User's email
 * @param {string} password - User's password
 * @returns {Promise} - Axios promise resolving to the login response
 */
export const login = async (email, password) => {
    try {
        const response = await API.post("/auth/login", { email, password });
        return response.data;
    } catch (error) {
        throw new Error(`Login failed: ${error}`);
    }
};

/**
 * Fetch dashboard data
 * @returns {Promise} - Axios promise resolving to dashboard data
 */
export const fetchDashboardData = async () => {
    try {
        const response = await API.get("/dashboard");
        return response.data;
    } catch (error) {
        throw new Error(`Fetching dashboard data failed: ${error}`);
    }
};

export default API;
