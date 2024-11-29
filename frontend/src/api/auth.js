import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_BACKEND_URL,
  withCredentials: true,
});

export const login = async (username, password) => {
  try {
    const response = await api.post('/auth/login', { username, password });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

export const register = async (username, password) => {
  try {
    const response = await api.post('/auth/register', { username, password });
    return response.data;
  } catch (error) {
    handleError(error);
  }
};

const handleError = (error) => {
  if (error.response) {
    alert(`Error: ${error.response.data.message}`);
  } else {
    alert("Network Error: Please check your internet connection.");
  }
};
