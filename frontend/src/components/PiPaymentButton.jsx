import React from 'react';
import { Pi } from "@minepi/pi-web-sdk";

const PiPaymentButton = ({ amount, userId, onSuccess }) => {
  const handlePayment = async () => {
    try {
      const payment = await Pi.createPayment({
        amount,
        memo: "Premium Subscription",
        metadata: { userId },
      });

      if (payment.status === "completed") {
        onSuccess(payment);
      }
    } catch (error) {
      console.error("Payment failed", error);
    }
  };

  return <button onClick={handlePayment}>Pay {amount} Pi</button>;
};

export default PiPaymentButton;
