// Error.js
export class AppError {
  constructor(message, code = 500) {
    this.message = message; // Error message
    this.code = code; // HTTP status code or custom error code
  }

  // Example method to display error details
  getDetails() {
    return `Error ${this.code}: ${this.message}`;
  }
}

import { AppError } from '../models/Error';

const error = new AppError('Unauthorized access', 401);
console.log(error.getDetails()); // "Error 401: Unauthorized access"
