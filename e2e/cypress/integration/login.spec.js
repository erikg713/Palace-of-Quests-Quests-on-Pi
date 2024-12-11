describe('Login Page', () => {
  it('allows the user to log in with correct credentials', () => {
    cy.visit('/login');
    cy.get('input[name="username"]').type('test_user');
    cy.get('input[name="password"]').type('password123');
    cy.get('button[type="submit"]').click();
    cy.contains('Welcome, test_user!');
  });

  it('shows an error message for incorrect credentials', () => {
    cy.visit('/login');
    cy.get('input[name="username"]').type('test_user');
    cy.get('input[name="password"]').type('wrongpassword');
    cy.get('button[type="submit"]').click();
    cy.contains('Invalid username or password');
  });
});
