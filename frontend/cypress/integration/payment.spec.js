describe("Pi Network Payment Flow", () => {
  it("should complete a payment using Pi Network", () => {
    cy.visit("http://localhost:3000/shop");

    // Mock Pi.createPayment() and payment lifecycle callbacks
    cy.window().then((win) => {
      win.Pi = {
        createPayment: (paymentData, callbacks) => {
          callbacks.onReadyForServerApproval("fake_payment_id");
          callbacks.onReadyForServerCompletion("fake_payment_id", "fake_txid");
          return Promise.resolve({ paymentId: "fake_payment_id" });
        }
      };
    });

    // Intercept the approval and completion requests
    cy.intercept("POST", "/approve", (req) => {
      expect(req.body.paymentId).to.equal("fake_payment_id");
      req.reply({ statusCode: 200, body: { message: "Payment approved" } });
    });

    cy.intercept("POST", "/complete", (req) => {
      expect(req.body.paymentId).to.equal("fake_payment_id");
      expect(req.body.txid).to.equal("fake_txid");
      req.reply({ statusCode: 200, body: { message: "Payment completed" } });
    });

    // Simulate placing an order and initiating a payment
    cy.get("button").contains("Order Now").click();

    // Confirm payment status message or success indication
    cy.contains("Payment completed").should("exist");
  });

  it("should handle payment cancellation", () => {
    cy.visit("http://localhost:3000/shop");

    // Mock Pi.createPayment() with a cancellation callback
    cy.window().then((win) => {
      win.Pi = {
        createPayment: (paymentData, callbacks) => {
          callbacks.onCancel("fake_payment_id");
          return Promise.reject(new Error("Payment canceled"));
        }
      };
    });

    // Intercept the cancellation request
    cy.intercept("POST", "/cancelled_payment", (req) => {
      expect(req.body.paymentId).to.equal("fake_payment_id");
      req.reply({ statusCode: 200, body: { message: "Payment canceled" } });
    });

    // Attempt to place an order and expect cancellation handling
    cy.get("button").contains("Order Now").click();

    // Confirm cancellation message or error indication
    cy.contains("Payment canceled").should("exist");
  });
});

it("should handle failed authentication gracefully", () => {
  cy.visit("http://localhost:3000");

  cy.window().then((win) => {
    win.Pi = {
      authenticate: () => {
        return Promise.reject(new Error("Authentication failed"));
      }
    };
  });

  cy.get("button").contains("Sign In with Pi").click();

  cy.on("window:alert", (str) => {
    expect(str).to.equal("Failed to authenticate with Pi Network.");
  });
});

describe("Payment Flow", () => {
  it("should successfully complete a payment with Pi Network", () => {
    cy.visit("http://localhost:3000/shop");

    cy.window().then((win) => {
      win.Pi = {
        createPayment: (paymentData, callbacks) => {
          callbacks.onReadyForServerApproval("fake_payment_id");
          callbacks.onReadyForServerCompletion("fake_payment_id", "fake_txid");
          return Promise.resolve({ paymentId: "fake_payment_id" });
        }
      };
    });

    cy.intercept("POST", "/approve", (req) => {
      expect(req.body.paymentId).to.equal("fake_payment_id");
      req.reply({ statusCode: 200, body: { message: "Payment approved" } });
    }).as("approvePayment");

    cy.intercept("POST", "/complete", (req) => {
      expect(req.body.paymentId).to.equal("fake_payment_id");
      expect(req.body.txid).to.equal("fake_txid");
      req.reply({ statusCode: 200, body: { message: "Payment completed" } });
    }).as("completePayment");

    cy.get("button").contains("Order Now").click();

    cy.wait("@approvePayment");
    cy.wait("@completePayment");

    cy.contains("Payment completed").should("be.visible");
  });
});

it("should handle payment cancellation", () => {
  cy.visit("http://localhost:3000/shop");

  cy.window().then((win) => {
    win.Pi = {
      createPayment: (paymentData, callbacks) => {
        callbacks.onCancel("fake_payment_id");
        return Promise.reject(new Error("Payment canceled"));
      }
    };
  });

  cy.intercept("POST", "/cancelled_payment", (req) => {
    expect(req.body.paymentId).to.equal("fake_payment_id");
    req.reply({ statusCode: 200, body: { message: "Payment canceled" } });
  }).as("cancelPayment");

  cy.get("button").contains("Order Now").click();

  cy.wait("@cancelPayment");

  cy.contains("Payment canceled").should("be.visible");
});
