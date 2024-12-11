import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders the home page', () => {
  render(<App />);
  const homeElement = screen.getByText(/Welcome to Palace of Quests/i);
  expect(homeElement).toBeInTheDocument();
});
