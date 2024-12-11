import { render, screen } from '@testing-library/react';
import { I18nextProvider } from 'react-i18next';
import i18n from '../i18n';
import Quest from '../components/Quest';

test('renders quest title in Spanish', () => {
  i18n.changeLanguage('es');
  render(
    <I18nextProvider i18n={i18n}>
      <Quest title="Defeat the Dragon" />
    </I18nextProvider>
  );
  expect(screen.getByText(/Derrota al Dragón/i)).toBeInTheDocument();
});
