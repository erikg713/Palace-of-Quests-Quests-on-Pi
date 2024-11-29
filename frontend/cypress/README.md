This README file goes inside the cypress folder to provide clear instructions for running and configuring Cypress tests for PiQuest.

File: frontend/cypress/README.md

# Cypress Tests for PiQuest

This directory contains end-to-end (E2E) tests for PiQuest’s authentication and payment flows using **Cypress**.

## Prerequisites

1. **Frontend and Backend**: Ensure both frontend (`npm start`) and backend (`flask run`) servers are running.
2. **Cypress**: Make sure Cypress is installed. You can install it by running:

   ```bash
   npm install cypress --save-dev

Running Tests

1. Run Cypress in Interactive Mode

Use interactive mode to visually debug tests:

npx cypress open

Select a test file from the Cypress window (e.g., auth.spec.js or payment.spec.js).

Watch tests execute in the Cypress test runner.


2. Run Cypress in Headless Mode

For automated testing or CI/CD environments, run Cypress in headless mode:

npx cypress run

Test Structure

Integration Tests: Located in cypress/integration/, covering different flows:

auth.spec.js: Authentication tests with Pi Network.

payment.spec.js: Payment flow tests, including approval, completion, and cancellation.


Mocking Pi SDK: Each test mocks the Pi SDK methods (e.g., Pi.authenticate and Pi.createPayment) to simulate different responses without needing live Pi Network access.


Writing New Tests

1. Create New Test Files: Add a new test file in cypress/integration/ with .spec.js extension.


2. Mock API Calls: Use cy.intercept() to mock backend API requests and responses.


3. Run and Validate: Use cy.get() and cy.contains() to locate elements and validate responses.



Example Commands

Locate and Interact with Elements:

cy.get("button").contains("Sign In with Pi").click();

Assert Expected Behavior:

cy.contains("Welcome, testuser").should("be.visible");

Mock API Calls:

cy.intercept("POST", "/approve", { statusCode: 200, body: { message: "Payment approved" } });


Troubleshooting

Backend Not Running: Ensure the Flask server is up and running.

CORS Issues: Verify that CORS is enabled on the backend for localhost.

Mocking Errors: Double-check the API paths and payloads in cy.intercept().


Resources

Cypress Documentation

Pi Network Documentation


---

## **3. Setting Up Configuration**

To simplify running tests with Cypress, configure some settings in `cypress.json`.

#### **File:** `frontend/cypress.json`

```json
{
  "baseUrl": "http://localhost:3000",
  "viewportWidth": 1280,
  "viewportHeight": 720,
  "watchForFileChanges": true
}

Explanation:

baseUrl: Sets the base URL for all tests, so you can use relative paths in cy.visit().

viewportWidth and viewportHeight: Set the screen resolution for consistent testing across environments.

watchForFileChanges: Automatically re-runs tests when files change.

