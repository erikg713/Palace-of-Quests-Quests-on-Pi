describe('UserProfile E2E Test', () => {
  beforeEach(() => {
    cy.intercept('GET', '/user', {
      statusCode: 200,
      body: { username: 'JohnDoe' }, // Mock API response
    }).as('getUser');
  });

  it('should show loading state initially', () => {
    cy.visit('/');
    cy.contains('Loading...').should('be.visible');
  });

  it('should display user welcome message after fetching user', () => {
    cy.visit('/');
    cy.wait('@getUser');
    cy.contains('Welcome, JohnDoe!').should('be.visible');
  });

  it('should show error if API call fails', () => {
    cy.intercept('GET', '/user', { statusCode: 500, body: {} }).as('getUserError');
    cy.visit('/');
    cy.wait('@getUserError');
    cy.contains('Error: Failed to fetch user data').should('be.visible');
  });
});
