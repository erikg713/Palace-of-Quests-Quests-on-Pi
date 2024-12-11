describe('Payment Flow', () => {
  it('processes a successful Pi payment', () => {
    cy.visit('/quests/1');
    cy.get('button.purchase').click();
    cy.get('#payment-modal').should('be.visible');
    cy.get('button.confirm-payment').click();
    cy.contains('Payment Successful!');
  });

  it('shows an error for insufficient balance', () => {
    cy.visit('/quests/1');
    cy.get('button.purchase').click();
    cy.get('#payment-modal').should('be.visible');
    cy.get('button.confirm-payment').click();
    cy.contains('Insufficient Balance');
  });
});
