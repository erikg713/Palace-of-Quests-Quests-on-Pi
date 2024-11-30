import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api';

/**
 * Places an order for an in-game purchase or avatar upgrade.
 * @param {Object} orderData - The order details (e.g., userId, itemId, paymentDetails).
 * @returns {Promise<Object>} - The created order and transaction details.
 */
export const placeOrder = async (orderData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/quests/orders`, orderData);
    return response.data;
  } catch (error) {
    console.error('Error placing order:', error);
    throw error.response?.data || error.message;
  }
};

/**
 * Fetches all orders for a specific user (e.g., their transaction history).
 * @param {string} userId - The ID of the user.
 * @returns {Promise<Array>} - A list of orders for the user.
 */
export const getUserOrders = async (userId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/quests/orders/user/${userId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching orders for user ${userId}:`, error);
    throw error.response?.data || error.message;
  }
};

/**
 * Fetches the details of a specific order by its ID.
 * @param {string} orderId - The ID of the order.
 * @returns {Promise<Object>} - The details of the order.
 */
export const getOrderById = async (orderId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/quests/orders/${orderId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching order with ID ${orderId}:`, error);
    throw error.response?.data || error.message;
  }
};

/**
 * Updates the status of an order (e.g., "Processing", "Completed").
 * @param {string} orderId - The ID of the order.
 * @param {Object} statusUpdate - The new status details.
 * @returns {Promise<Object>} - The updated order details.
 */
export const updateOrderStatus = async (orderId, statusUpdate) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/quests/orders/${orderId}/status`, statusUpdate);
    return response.data;
  } catch (error) {
    console.error(`Error updating order status for ID ${orderId}:`, error);
    throw error.response?.data || error.message;
  }
};

/**
 * Deletes an order by ID (e.g., for refund requests or errors).
 * @param {string} orderId - The ID of the order.
 * @returns {Promise<Object>} - Confirmation of deletion.
 */
export const deleteOrder = async (orderId) => {
  try {
    const response = await axios.delete(`${API_BASE_URL}/quests/orders/${orderId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting order with ID ${orderId}:`, error);
    throw error.response?.data || error.message;
  }
};
