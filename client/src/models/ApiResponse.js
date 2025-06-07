/**
 * @class ApiResponse
 * Represents a standard API response structure.
 */
export class ApiResponse {
  /**
   * @param {boolean} success - Indicates if the response was successful.
   * @param {Object|Array|null} data - The actual data payload.
   * @param {string} [message=""] - Optional message (e.g., error description).
   */
  constructor(success, data = null, message = '') {
    if (typeof success !== 'boolean') {
      throw new TypeError('ApiResponse "success" must be a boolean.');
    }
    this.success = success;

    // Defensive copy and freezing for immutability
    if (data && (typeof data === 'object' || Array.isArray(data))) {
      this.data = Array.isArray(data)
        ? Object.freeze([...data])
        : Object.freeze({ ...data });
    } else {
      this.data = data;
    }

    this.message = typeof message === 'string' ? message : String(message);

    Object.freeze(this); // Make the ApiResponse instance immutable
  }

  /**
   * Checks if the response contains non-empty data.
   * @returns {boolean}
   */
  hasData() {
    if (Array.isArray(this.data)) {
      return this.data.length > 0;
    }
    if (this.data && typeof this.data === 'object') {
      return Object.keys(this.data).length > 0;
    }
    return !!this.data;
  }
}
