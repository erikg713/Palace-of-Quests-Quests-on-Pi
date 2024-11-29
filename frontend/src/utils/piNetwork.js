import axios from "axios";

const BASE_URL = "http://localhost:5000"; // Your backend server URL

export const initiateSubscription = async (token) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/payment/subscribe`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Subscription initiation failed:", error.response.data);
    throw error;
  }
};

export const verifyPayment = async (paymentId, token) => {
  try {
    const response = await axios.post(
      `${BASE_URL}/payment/verify`,
      { payment_id: paymentId },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Payment verification failed:", error.response.data);
    throw error;
  }
};