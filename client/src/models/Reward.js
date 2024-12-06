// Reward.js
export class Reward {
  constructor(type, value, description) {
    this.type = type; // e.g., 'XP', 'item'
    this.value = value; // Numeric value of the reward
    this.description = description; // Optional description
  }

  // Example method to display reward details
  getDetails() {
    return `${this.value} ${this.type} - ${this.description || 'No description'}`;
  }
}
