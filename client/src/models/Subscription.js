// Subscription.js
export class Subscription {
  constructor(planName, price, duration, perks) {
    this.planName = planName;
    this.price = price; // e.g., 9.99 for Premium
    this.duration = duration; // e.g., '1 year'
    this.perks = perks; // Array of perks
  }

  // Example method to format price
  getFormattedPrice(currency = '$') {
    return `${currency}${this.price}`;
  }
}

import { Subscription } from '../models/Subscription';

const premium = new Subscription('Premium', 9.99, '1 year', [
  'Access to premium levels',
  'Priority support',
  'Exclusive rewards',
]);

console.log(premium.getFormattedPrice()); // "$9.99"
