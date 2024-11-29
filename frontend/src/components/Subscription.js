import React, { useState, useEffect } from 'react';
import { getSubscriptionStatus, upgradeSubscription } from '../../services/payment';

const Subscription = () => {
  const [subscription, setSubscription] = useState(null);

  useEffect(() => {
    async function fetchSubscription() {
      const status = await getSubscriptionStatus();
      setSubscription(status);
    }
    fetchSubscription();
  }, []);

  const handleUpgrade = async () => {
    const success = await upgradeSubscription();
    if (success) {
      alert('Subscription upgraded!');
      fetchSubscription();
    }
  };

  return (
    <div>
      <h1>Your Subscription</h1>
      {subscription ? (
        <div>
          <p>Plan: {subscription.plan}</p>
          <button onClick={handleUpgrade}>Upgrade</button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default Subscription;