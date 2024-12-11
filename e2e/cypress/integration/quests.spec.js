describe('Quest Progression', () => {
  it('allows a player to complete a quest', () => {
    cy.visit('/quests/1');
    cy.get('button.complete-quest').click();
    cy.contains('Quest Completed!');
  });
});
