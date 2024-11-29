// components/Premium/Subscription.js
import React from 'react';

const Subscription = () => {
  const handleSubscription = () => {
    // Handle Pi Network payment here using Pi Network SDK
    console.log('Processing Pi payment for premium subscription...');
  };

  return (
    <div>
      <h2>Premium Subscription</h2>
      <p>Get all upgrades unlocked for 1 year for $9.99</p>
      <button onClick={handleSubscription}>Subscribe</button>
    </div>
  );
};

export default Subscription;
import React, { useState, useEffect } from 'react';
import { getSubscriptionStatus, subscribe } from '../../services/payment';

const Subscription = () => {
  const [subscriptionStatus, setSubscriptionStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSubscriptionStatus = async () => {
      const status = await getSubscriptionStatus();
      setSubscriptionStatus(status);
      setLoading(false);
    };

    fetchSubscriptionStatus();
  }, []);

  const handleSubscription = async () => {
    try {
      await subscribe();
      alert('Subscription activated!');
    } catch (error) {
      alert('Subscription failed! Please try again.');
    }
  };

  if (loading) {
    return <div>Loading subscription status...</div>;
  }

  return (
    <div className="subscription">
      <h2>Premium Subscription</h2>
      {subscriptionStatus ? (
        <div>
          <p>Your subscription is active until {subscriptionStatus.expiryDate}.</p>
        </div>
      ) : (
        <div>
          <button onClick={handleSubscription}>Activate Premium</button>
        </div>
      )}
    </div>
  );
};

export default Subscription;