import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:5000/api' });

export const registerUser = (userData) => API.post('/register', userData);
export const loginUser = (userData) => API.post('/login', userData);
export const getPlayerStats = (userId) => API.get(`/player/${userId}/stats`);
export const getMarketplaceItems = () => API.get('/marketplace');
