import { render, screen } from '@testing-library/react';
import Inventory from '../components/Inventory';

test('renders inventory items', () => {
  const items = [
    { id: 1, name: 'Golden Sword', description: 'A legendary weapon' },
    { id: 2, name: 'Silver Shield', description: 'Provides strong defense' },
  ];

  render(<Inventory items={items} />);
  expect(screen.getByText('Golden Sword')).toBeInTheDocument();
  expect(screen.getByText('Silver Shield')).toBeInTheDocument();
});

test('displays item details on selection', () => {
  const items = [
    { id: 1, name: 'Golden Sword', description: 'A legendary weapon' },
  ];

  render(<Inventory items={items} />);
  screen.getByText('Golden Sword').click();
  expect(screen.getByText('A legendary weapon')).toBeInTheDocument();
});
