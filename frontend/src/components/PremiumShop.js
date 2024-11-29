import React, { useState, useEffect } from "react";
import { getPremiumBenefits, initiatePayment } from "../api/premiumAPI";

const PremiumShop = () => {
  const [benefits, setBenefits] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBenefits = async () => {
      const data = await getPremiumBenefits();
      setBenefits(data);
      setLoading(false);
    };
    fetchBenefits();
  }, []);

  const handlePurchase = async (benefitId) => {
    const result = await initiatePayment(benefitId);
    if (result.error) {
      alert(result.error);
    } else {
      alert("Payment initiated. Complete in the Pi app.");
    }
  };

  if (loading) return <p>Loading premium shop...</p>;

  return (
    <div className="container">
      <h2>Premium Shop</h2>
      <ul>
        {benefits.map(benefit => (
          <li key={benefit.id}>
            <h3>{benefit.name}</h3>
            <p>{benefit.description}</p>
            <p>Price: {benefit.price_pi} Pi</p>
            <button onClick={() => handlePurchase(benefit.id)}>Purchase</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PremiumShop;

import React, { useState, useEffect } from "react";
import { getPremiumBenefits, initiatePayment } from "../api/premiumAPI";
import "./PremiumShop.css";

const PremiumShop = () => {
  const [benefits, setBenefits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchBenefits = async () => {
      try {
        const data = await getPremiumBenefits();
        setBenefits(data);
      } catch (err) {
        setError("Failed to load premium benefits.");
      } finally {
        setLoading(false);
      }
    };
    fetchBenefits();
  }, []);

  const handlePurchase = async (benefitId) => {
    try {
      const result = await initiatePayment(benefitId);
      if (result.error) {
        alert(`Purchase failed: ${result.error}`);
      } else {
        alert("Payment initiated. Complete the purchase in the Pi Network app.");
      }
    } catch (err) {
      alert("Payment initiation failed. Please try again.");
    }
  };

  if (loading) return <p>Loading premium shop...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="premium-shop">
      <h2>Premium Shop</h2>
      <ul>
        {benefits.map(benefit => (
          <li key={benefit.id}>
            <h3>{benefit.name}</h3>
            <p>{benefit.description}</p>
            <p>Price: {benefit.price_pi} Pi</p>
            <button onClick={() => handlePurchase(benefit.id)}>Purchase</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PremiumShop;
