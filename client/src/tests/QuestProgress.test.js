import { render, screen } from '@testing-library/react';
import QuestProgress from '../components/QuestProgress';

test('displays quest progress correctly', () => {
  const progress = { completed: 3, total: 5 };

  render(<QuestProgress progress={progress} />);
  expect(screen.getByText('3 of 5 Quests Completed')).toBeInTheDocument();
});
