import { render } from '@testing-library/react';
import { axe } from 'jest-axe';
import Quest from '../components/Quest';

test('Quest component is accessible', async () => {
  const { container } = render(<Quest title="Defeat the Dragon" />);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
});
