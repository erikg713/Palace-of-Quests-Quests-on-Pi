import axios from 'axios';

// Authenticate user with Pi Network
export const authenticateUser = async () => {
  const scopes = ["username", "payments"];
  
  try {
    const authResult = await window.Pi.authenticate(scopes, onIncompletePaymentFound);
    await axios.post("/signin", { authResult });
    return authResult.user;
  } catch (error) {
    console.error("Authentication Error:", error);
    alert("Failed to authenticate with Pi Network.");
  }
};

// Handles incomplete payments found during authentication
const onIncompletePaymentFound = (payment) => {
  return axios.post("/incomplete", { payment });
};

// Payment initiation function
export const initiatePayment = async (amount, memo, metadata) => {
  const paymentData = { amount, memo, metadata };
  const callbacks = {
    onReadyForServerApproval,
    onReadyForServerCompletion,
    onCancel,
    onError,
  };

  try {
    return await window.Pi.createPayment(paymentData, callbacks);
  } catch (error) {
    console.error("Payment initiation failed:", error);
    alert("Failed to initiate payment.");
  }
};

const onReadyForServerApproval = (paymentId) => axios.post("/approve", { paymentId });
const onReadyForServerCompletion = (paymentId, txid) => axios.post("/complete", { paymentId, txid });
const onCancel = (paymentId) => axios.post("/cancelled_payment", { paymentId });
const onError = (error, payment) => console.error("Payment Error:", error, payment);

import axios from 'axios';

// Helper function to authenticate with Pi SDK
export const authenticateUser = async () => {
  const scopes = ["username", "payments"];
  
  try {
    // Initiate Pi SDK authentication
    const authResult = await window.Pi.authenticate(scopes, onIncompletePaymentFound);
    await axios.post("/signin", { authResult });
    return authResult.user;
  } catch (error) {
    console.error("Authentication Error:", error);
    alert("Failed to authenticate with Pi Network.");
  }
};

// Handles incomplete payments found during authentication
const onIncompletePaymentFound = (payment) => {
  console.log("Incomplete Payment Found:", payment);
  return axios.post("/incomplete", { payment });
};

// Initiate a payment request
export const initiatePayment = async (amount, memo, metadata) => {
  if (!window.Pi) {
    alert("Pi SDK is not available.");
    return;
  }

  const paymentData = { amount, memo, metadata };
  const callbacks = {
    onReadyForServerApproval,
    onReadyForServerCompletion,
    onCancel,
    onError,
  };

  try {
    const payment = await window.Pi.createPayment(paymentData, callbacks);
    console.log("Payment initiated:", payment);
  } catch (error) {
    console.error("Payment initiation failed:", error);
    alert("Failed to initiate payment. Please try again.");
  }
};

// Callback when ready for server approval
const onReadyForServerApproval = (paymentId) => {
  axios.post("/approve", { paymentId });
};

// Callback when payment is ready for completion
const onReadyForServerCompletion = (paymentId, txid) => {
  axios.post("/complete", { paymentId, txid });
};

// Handle cancellation and errors
const onCancel = (paymentId) => {
  axios.post("/cancelled_payment", { paymentId });
};

const onError = (error, payment) => {
  console.error("Payment Error:", error);
  if (payment) {
    console.error("Error Details:", payment);
  }
};
