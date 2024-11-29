import axios from 'axios';

export const getPremiumBenefits = async () => {
  const response = await axios.get("/premium/benefits");
  return response.data;
};

export const initiatePayment = async (benefitId) => {
  const response = await axios.post("/premium/purchase_premium", { benefit_id: benefitId });
  return response.data;
};

import axios from 'axios';

export const getPremiumBenefits = async () => {
  try {
    const response = await axios.get("/premium/benefits");
    return response.data;
  } catch (error) {
    throw new Error("Error fetching premium benefits.");
  }
};

export const initiatePayment = async (benefitId) => {
  try {
    const response = await axios.post("/premium/purchase_premium", { benefit_id: benefitId });
    return response.data;
  } catch (error) {
    return { error: "Payment initiation failed." };
  }
};
