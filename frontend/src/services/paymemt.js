const API_URL = 'https://api.palaceofquests.com';  // Your backend API URL

export const getSubscriptionStatus = async () => {
  const response = await fetch(`${API_URL}/subscription/status`);
  return await response.json();
};

export const subscribe = async () => {
  const response = await fetch(`${API_URL}/subscription/activate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return await response.json();
};