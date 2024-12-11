import { render, screen, fireEvent } from '@testing-library/react';
import LoginForm from '../components/LoginForm';

test('submits login form successfully', () => {
  const mockSubmit = jest.fn();
  render(<LoginForm onSubmit={mockSubmit} />);

  fireEvent.change(screen.getByLabelText(/Username/i), { target: { value: 'test_user' } });
  fireEvent.change(screen.getByLabelText(/Password/i), { target: { value: 'password123' } });
  fireEvent.click(screen.getByText(/Submit/i));

  expect(mockSubmit).toHaveBeenCalledWith({ username: 'test_user', password: 'password123' });
});
