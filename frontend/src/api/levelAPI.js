import axios from 'axios';

export const getLevelRewards = async (level) => {
  const response = await axios.get(`/level_rewards/${level}`);
  return response.data;
};

export const upgradeLevel = async () => {
  const response = await axios.post('/upgrade_level');
  return response.data;
};
