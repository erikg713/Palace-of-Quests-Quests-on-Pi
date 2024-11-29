export const getSubscriptionStatus = async () => {
  // Replace with actual API call
  return await fetch('/api/subscription').then((res) => res.json());
};

export const upgradeSubscription = async () => {
  // Replace with actual API call
  return await fetch('/api/upgrade', { method: 'POST' }).then((res) => res.ok);
};