import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import UserProfile from './UserProfile';

describe('UserProfile Component', () => {
  const mockOnEdit = jest.fn();
  const mockOnDelete = jest.fn();
  const mockProps = {
    name: 'John Doe',
    bio: 'Software Developer. Passionate about Web3 and AI.',
    profilePicture: 'https://via.placeholder.com/100',
    onEdit: mockOnEdit,
    onDelete: mockOnDelete,
  };

  it('renders the user name', () => {
    render(<UserProfile {...mockProps} />);
    expect(screen.getByText('John Doe')).toBeInTheDocument();
  });

  it('renders the user bio', () => {
    render(<UserProfile {...mockProps} />);
    expect(
      screen.getByText('Software Developer. Passionate about Web3 and AI.')
    ).toBeInTheDocument();
  });

  it('renders the profile picture', () => {
    render(<UserProfile {...mockProps} />);
    const img = screen.getByAltText("John Doe's profile");
    expect(img).toBeInTheDocument();
    expect(img).toHaveAttribute('src', 'https://via.placeholder.com/100');
  });

  it('calls the onEdit function when the Edit button is clicked', () => {
    render(<UserProfile {...mockProps} />);
    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);
    expect(mockOnEdit).toHaveBeenCalledTimes(1);
  });

  it('calls the onDelete function when the Delete button is clicked', () => {
    render(<UserProfile {...mockProps} />);
    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);
    expect(mockOnDelete).toHaveBeenCalledTimes(1);
  });
});
