import { render, screen } from '@testing-library/react';
import Quest from '../components/Quest';

test('renders quest title', () => {
  render(<Quest title="The Golden Castle" />);
  const titleElement = screen.getByText(/The Golden Castle/i);
  expect(titleElement).toBeInTheDocument();
});
