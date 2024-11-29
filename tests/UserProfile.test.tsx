// UserProfile.test.tsx
import React from 'react';
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import configureStore from 'redux-mock-store';
import UserProfile from './UserProfile';

const mockStore = configureStore([]);

describe('UserProfile Component', () => {
  it('should render login prompt when user is not logged in', () => {
    const store = mockStore({
      auth: { user: null },
    });

    const { getByText } = render(
      <Provider store={store}>
        <UserProfile />
      </Provider>
    );

    expect(getByText('Please log in.')).toBeInTheDocument();
  });

  it('should render welcome message with username', () => {
    const store = mockStore({
      auth: { user: { username: 'JohnDoe' } },
    });

    const { getByText } = render(
      <Provider store={store}>
        <UserProfile />
      </Provider>
    );

    expect(getByText('Welcome, JohnDoe!')).toBeInTheDocument();
  });

  it('should render fallback message for user without username', () => {
    const store = mockStore({
      auth: { user: {} },
    });

    const { getByText } = render(
      <Provider store={store}>
        <UserProfile />
      </Provider>
    );

    expect(getByText('Welcome, Guest!')).toBeInTheDocument();
  });
});
