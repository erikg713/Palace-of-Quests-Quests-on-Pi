// productController.js

import axios from 'axios';

// API Base URL
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Fetch all products
 * @returns {Promise<Array>} - List of all products
 */
export const getAllProducts = async () => {
    try {
        const response = await axios.get(`${BASE_URL}/products`);
        return response.data;
    } catch (error) {
        console.error('Error fetching products:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Fetch product by ID
 * @param {string} productId - ID of the product
 * @returns {Promise<Object>} - Product details
 */
export const getProductById = async (productId) => {
    try {
        const response = await axios.get(`${BASE_URL}/products/${productId}`);
        return response.data;
    } catch (error) {
        console.error('Error fetching product:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Create a new product
 * @param {Object} productData - Data of the product to create
 * @returns {Promise<Object>} - Created product details
 */
export const createProduct = async (productData) => {
    try {
        const response = await axios.post(`${BASE_URL}/products`, productData);
        return response.data;
    } catch (error) {
        console.error('Error creating product:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Update an existing product
 * @param {string} productId - ID of the product to update
 * @param {Object} productData - Updated product data
 * @returns {Promise<Object>} - Updated product details
 */
export const updateProduct = async (productId, productData) => {
    try {
        const response = await axios.put(`${BASE_URL}/products/${productId}`, productData);
        return response.data;
    } catch (error) {
        console.error('Error updating product:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Delete a product
 * @param {string} productId - ID of the product to delete
 * @returns {Promise<Object>} - Confirmation of deletion
 */
export const deleteProduct = async (productId) => {
    try {
        const response = await axios.delete(`${BASE_URL}/products/${productId}`);
        return response.data;
    } catch (error) {
        console.error('Error deleting product:', error);
        throw error.response ? error.response.data : error.message;
    }
};

/**
 * Search products
 * @param {string} query - Search query
 * @returns {Promise<Array>} - List of products matching the query
 */
export const searchProducts = async (query) => {
    try {
        const response = await axios.get(`${BASE_URL}/products/search`, {
            params: { query },
        });
        return response.data;
    } catch (error) {
        console.error('Error searching products:', error);
        throw error.response ? error.response.data : error.message;
    }
};
