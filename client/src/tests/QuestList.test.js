import { render, screen, fireEvent } from '@testing-library/react';
import QuestList from '../components/QuestList';

test('displays a list of quests', () => {
  const quests = [
    { id: 1, title: 'Find the Treasure', level_required: 5 },
    { id: 2, title: 'Defeat the Dragon', level_required: 10 },
  ];

  render(<QuestList quests={quests} />);
  expect(screen.getByText('Find the Treasure')).toBeInTheDocument();
  expect(screen.getByText('Defeat the Dragon')).toBeInTheDocument();
});

test('filters quests by level', () => {
  const quests = [
    { id: 1, title: 'Find the Treasure', level_required: 5 },
    { id: 2, title: 'Defeat the Dragon', level_required: 10 },
  ];

  render(<QuestList quests={quests} playerLevel={5} />);
  expect(screen.queryByText('Defeat the Dragon')).not.toBeInTheDocument();
});
