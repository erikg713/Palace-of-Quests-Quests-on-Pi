import axios from "axios";

const API = axios.create({
    baseURL: "http://localhost:5000/api",
});

export const login = async (email, password) => {
    return API.post("/auth/login", { email, password });
};

export const fetchDashboardData = async () => {
    return API.get("/dashboard");
};

export default API;
