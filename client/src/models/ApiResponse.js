// ApiResponse.js
export class ApiResponse {
  constructor(success, data, message = '') {
    this.success = success; // Boolean indicating if the response was successful
    this.data = data; // Actual data payload
    this.message = message; // Optional message (e.g., error message)
  }

  // Example method to check if the response has data
  hasData() {
    return this.data && Object.keys(this.data).length > 0;
  }
}

import { ApiResponse } from '../models/ApiResponse';

const response = new ApiResponse(true, { username: 'JohnDoe' }, 'Request successful');
if (response.hasData()) {
  console.log(response.data.username); // "JohnDoe"
}
