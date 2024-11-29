import API from "./api";

export const login = async (email, password) => {
    const response = await API.post("/auth/login", { email, password });
    return response.data;
};

export const register = async (userDetails) => {
    const response = await API.post("/auth/register", userDetails);
    return response.data;
};
