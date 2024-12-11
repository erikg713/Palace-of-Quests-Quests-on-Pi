import { render, screen, fireEvent } from '@testing-library/react';
import GameScreen from '../screens/GameScreen';

test('displays player stats correctly', () => {
  render(<GameScreen player={{ username: 'Player1', level: 10, inventory: [] }} />);
  expect(screen.getByText('Player1')).toBeInTheDocument();
  expect(screen.getByText('Level: 10')).toBeInTheDocument();
});

test('triggers level-up action', () => {
  const mockLevelUp = jest.fn();
  render(<GameScreen player={{ level: 10 }} onLevelUp={mockLevelUp} />);

  fireEvent.click(screen.getByText('Level Up'));
  expect(mockLevelUp).toHaveBeenCalled();
});
