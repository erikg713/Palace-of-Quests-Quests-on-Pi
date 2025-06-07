// Reward.js

/**
 * Represents a reward in the game.
 * @class
 */
export class Reward {
  /**
   * Constructs a new Reward instance.
   * @param {string} type - The type of the reward (e.g., 'XP', 'item').
   * @param {number} value - The numeric value of the reward.
   * @param {string} [description] - An optional description of the reward.
   * @throws {TypeError} If provided arguments are of invalid types.
   */
  constructor(type, value, description = '') {
    if (typeof type !== 'string' || !type.trim()) {
      throw new TypeError('Reward type must be a non-empty string.');
    }
    if (typeof value !== 'number' || !Number.isFinite(value)) {
      throw new TypeError('Reward value must be a finite number.');
    }
    if (description && typeof description !== 'string') {
      throw new TypeError('Reward description, if provided, must be a string.');
    }

    this.type = type.trim();
    this.value = value;
    this.description = description.trim();
  }

  /**
   * Returns a human-readable string describing the reward.
   * @returns {string}
   */
  getDetails() {
    const desc = this.description.length ? this.description : 'No description';
    return `${this.value} ${this.type} - ${desc}`;
  }

  /**
   * Updates this reward's details.
   * Only valid fields will be updated.
   * @param {{type?: string, value?: number, description?: string}} updates
   */
  update(updates = {}) {
    if (typeof updates.type === 'string' && updates.type.trim()) {
      this.type = updates.type.trim();
    }
    if (typeof updates.value === 'number' && Number.isFinite(updates.value)) {
      this.value = updates.value;
    }
    if (typeof updates.description === 'string') {
      this.description = updates.description.trim();
    }
  }
}
