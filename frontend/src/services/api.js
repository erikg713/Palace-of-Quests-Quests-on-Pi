const API_URL = 'https://api.palaceofquests.com';  // Your backend API URL

export const getPlayerData = async () => {
  const response = await fetch(`${API_URL}/player/data`);
  return await response.json();
};

export const getShopItems = async () => {
  const response = await fetch(`${API_URL}/shop/items`);
  return await response.json();
};

export const purchaseItem = async (itemId) => {
  const response = await fetch(`${API_URL}/shop/purchase`, {
    method: 'POST',
    body: JSON.stringify({ itemId }),
    headers: { 'Content-Type': 'application/json' },
  });
  return await response.json();
};
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
});

export const registerUser = (data) => api.post('/auth/register', data);
export const loginUser = (data) => api.post('/auth/login', data);
export const getMarketplaceItems = () => api.get('/marketplace/items');
