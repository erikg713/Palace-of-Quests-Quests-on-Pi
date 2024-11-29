describe("Authentication Flow", () => {
  it("should authenticate the user with Pi Network successfully", () => {
    cy.visit("http://localhost:3000");

    cy.window().then((win) => {
      win.Pi = {
        authenticate: (scopes, onIncompletePaymentFound) => {
          return Promise.resolve({ user: { username: "testuser" }, accessToken: "fake_access_token" });
        }
      };
    });

    cy.intercept("POST", "/auth/signin", (req) => {
      expect(req.body.authResult.accessToken).to.equal("fake_access_token");
      req.reply({ statusCode: 200, body: { username: "testuser" } });
    });

    cy.get("button").contains("Sign In with Pi").click();
    cy.contains("Welcome, testuser").should("be.visible");
  });
});

describe("Pi Network Authentication Flow", () => {
  it("should authenticate user with Pi Network", () => {
    // Visit the app's main page where the sign-in button is located
    cy.visit("http://localhost:3000");

    // Mock Pi.authenticate() in the browser
    cy.window().then((win) => {
      win.Pi = {
        authenticate: (scopes, onIncompletePaymentFound) => {
          return new Promise((resolve) => {
            const fakeAuthResult = {
              user: { username: "test_user" },
              accessToken: "fake_access_token"
            };
            resolve(fakeAuthResult);
          });
        }
      };
    });

    // Simulate clicking the "Sign In with Pi" button
    cy.get("button").contains("Sign In with Pi").click();

    // Verify that the backend received the access token
    cy.intercept("POST", "/signin", (req) => {
      expect(req.body.authResult.accessToken).to.equal("fake_access_token");
      req.reply({ statusCode: 200, body: { message: "User authenticated" } });
    });

    // Check that the user sees a success message or their username
    cy.contains("Welcome, test_user").should("exist");
  });
});

describe("Authentication Flow", () => {
  it("should authenticate the user with Pi Network successfully", () => {
    // Visit the login page
    cy.visit("http://localhost:3000");

    // Mock Pi.authenticate() in the browser
    cy.window().then((win) => {
      win.Pi = {
        authenticate: (scopes, onIncompletePaymentFound) => {
          return new Promise((resolve) => {
            const fakeAuthResult = {
              user: { username: "testuser" },
              accessToken: "fake_access_token"
            };
            resolve(fakeAuthResult);
          });
        }
      };
    });

    // Intercept and verify backend request
    cy.intercept("POST", "/signin", (req) => {
      expect(req.body.authResult.accessToken).to.equal("fake_access_token");
      req.reply({ statusCode: 200, body: { username: "testuser" } });
    }).as("signin");

    // Trigger sign-in action
    cy.get("button").contains("Sign In with Pi").click();

    // Confirm user is successfully signed in
    cy.contains("Welcome, testuser").should("be.visible");
  });
});
