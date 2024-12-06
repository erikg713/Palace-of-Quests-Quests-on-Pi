// Inventory.js
export class Inventory {
  constructor(userId, items = []) {
    this.userId = userId;
    this.items = items; // Array of item objects
  }

  // Method to add an item
  addItem(item) {
    this.items.push(item);
  }

  // Method to remove an item by ID
  removeItem(itemId) {
    this.items = this.items.filter((item) => item.id !== itemId);
  }
}

import { Inventory } from '../models/Inventory';

const inventory = new Inventory(1);
inventory.addItem({ id: 101, name: 'Sword', type: 'Weapon' });
inventory.removeItem(101);
console.log(inventory.items); // []
