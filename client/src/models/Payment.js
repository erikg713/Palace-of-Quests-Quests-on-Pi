// Payment.js

/**
 * Payment Model
 * Represents a payment entity within the Palace of Quests application.
 */

class Payment {
    /**
     * Creates an instance of Payment.
     * @param {Object} params - Payment parameters.
     * @param {string} params.id - Unique identifier for the payment.
     * @param {string} params.userId - Identifier of the user who made the payment.
     * @param {number} params.amount - Amount paid in Pi.
     * @param {string} params.currency - Currency type (e.g., 'Pi').
     * @param {string} params.status - Current status of the payment ('pending', 'completed', 'failed').
     * @param {Date} params.date - Date and time when the payment was made.
     * @param {string} [params.memo] - Optional memo or description for the payment.
     */
    constructor({ id, userId, amount, currency, status, date, memo = '' }) {
        this.id = id;
        this.userId = userId;
        this.amount = amount;
        this.currency = currency;
        this.status = status;
        this.date = date instanceof Date ? date : new Date(date);
        this.memo = memo;
    }

    /**
     * Updates the status of the payment.
     * @param {string} newStatus - The new status ('pending', 'completed', 'failed').
     */
    updateStatus(newStatus) {
        const validStatuses = ['pending', 'completed', 'failed'];
        if (!validStatuses.includes(newStatus)) {
            throw new Error(`Invalid status: ${newStatus}. Valid statuses are ${validStatuses.join(', ')}`);
        }
        this.status = newStatus;
    }

    /**
     * Formats the payment date to a readable string.
     * @returns {string} - Formatted date string.
     */
    getFormattedDate() {
        return this.date.toLocaleString();
    }

    /**
     * Returns a summary of the payment.
     * @returns {string} - Summary string.
     */
    getSummary() {
        return `Payment #${this.id} of ${this.amount} ${this.currency} by User ${this.userId} on ${this.getFormattedDate()} is ${this.status}.`;
    }
}

export default Payment;
