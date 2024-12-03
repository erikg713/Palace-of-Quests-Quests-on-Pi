// Product.js

/**
 * Product Model
 * Represents a product entity within the Palace of Quests application.
 */

class Product {
    /**
     * Creates an instance of Product.
     * @param {Object} params - Product parameters.
     * @param {string} params.id - Unique identifier for the product.
     * @param {string} params.name - Name of the product.
     * @param {number} params.price - Price of the product in Pi.
     * @param {string} params.description - Description of the product.
     * @param {string} params.category - Category of the product.
     * @param {number} params.stock - Available stock quantity.
     * @param {Date} params.createdAt - Date and time when the product was created.
     * @param {Date} params.updatedAt - Date and time when the product was last updated.
     * @param {string} [params.imageUrl] - Optional URL to the product image.
     */
    constructor({ id, name, price, description, category, stock, createdAt, updatedAt, imageUrl = '' }) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.description = description;
        this.category = category;
        this.stock = stock;
        this.createdAt = createdAt instanceof Date ? createdAt : new Date(createdAt);
        this.updatedAt = updatedAt instanceof Date ? updatedAt : new Date(updatedAt);
        this.imageUrl = imageUrl;
    }

    /**
     * Updates the stock quantity of the product.
     * @param {number} quantity - The quantity to add or subtract from the current stock.
     */
    updateStock(quantity) {
        const newStock = this.stock + quantity;
        if (newStock < 0) {
            throw new Error('Stock cannot be negative');
        }
        this.stock = newStock;
        this.updatedAt = new Date();
    }

    /**
     * Updates the price of the product.
     * @param {number} newPrice - The new price of the product in Pi.
     */
    updatePrice(newPrice) {
        if (newPrice < 0) {
            throw new Error('Price cannot be negative');
        }
        this.price = newPrice;
        this.updatedAt = new Date();
    }

    /**
     * Updates the product details.
     * @param {Object} updates - An object containing the fields to update.
     * @param {string} [updates.name] - New name of the product.
     * @param {string} [updates.description] - New description of the product.
     * @param {string} [updates.category] - New category of the product.
     * @param {string} [updates.imageUrl] - New image URL of the product.
     */
    updateDetails({ name, description, category, imageUrl }) {
        if (name !== undefined) this.name = name;
        if (description !== undefined) this.description = description;
        if (category !== undefined) this.category = category;
        if (imageUrl !== undefined) this.imageUrl = imageUrl;
        this.updatedAt = new Date();
    }

    /**
     * Formats the creation date to a readable string.
     * @returns {string} - Formatted creation date string.
     */
    getFormattedCreationDate() {
        return this.createdAt.toLocaleString();
    }

    /**
     * Formats the last updated date to a readable string.
     * @returns {string} - Formatted updated date string.
     */
    getFormattedUpdatedDate() {
        return this.updatedAt.toLocaleString();
    }

    /**
     * Returns a summary of the product.
     * @returns {string} - Summary string.
     */
    getSummary() {
        return `${this.name} (${this.category}) - ${this.price} Pi. Stock: ${this.stock}.`;
    }

    /**
     * Checks if the product is in stock.
     * @returns {boolean} - True if stock is greater than 0, else false.
     */
    isInStock() {
        return this.stock > 0;
    }
}

export default Product;
