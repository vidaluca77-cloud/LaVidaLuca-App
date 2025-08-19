import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Contact from '../contact/page';

// Mock fetch for API calls
const mockFetch = jest.fn();
global.fetch = mockFetch;

describe('Contact Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockFetch.mockClear();
  });

  it('renders contact form with all required fields', () => {
    render(<Contact />);
    
    expect(screen.getByText('Contact')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Nom')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Ton message')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /envoyer/i })).toBeInTheDocument();
  });

  it('requires all fields to be filled', async () => {
    const user = userEvent.setup();
    render(<Contact />);
    
    const submitButton = screen.getByRole('button', { name: /envoyer/i });
    
    // Try to submit without filling fields
    await user.click(submitButton);
    
    // Check if form validation works (HTML5 validation)
    const nameInput = screen.getByPlaceholderText('Nom');
    const emailInput = screen.getByPlaceholderText('Email');
    const messageInput = screen.getByPlaceholderText('Ton message');
    
    expect(nameInput).toBeRequired();
    expect(emailInput).toBeRequired();
    expect(messageInput).toBeRequired();
  });

  it('validates email field type', () => {
    render(<Contact />);
    
    const emailInput = screen.getByPlaceholderText('Email');
    expect(emailInput).toHaveAttribute('type', 'email');
  });

  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    
    // Mock successful API response
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ success: true })
    });
    
    render(<Contact />);
    
    // Fill in the form
    await user.type(screen.getByPlaceholderText('Nom'), 'Jean Dupont');
    await user.type(screen.getByPlaceholderText('Email'), 'jean.dupont@example.com');
    await user.type(screen.getByPlaceholderText('Ton message'), 'Bonjour, je souhaiterais plus d\'informations.');
    
    // Submit the form
    await user.click(screen.getByRole('button', { name: /envoyer/i }));
    
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith('/api/contact', {
        method: 'POST',
        body: JSON.stringify({
          name: 'Jean Dupont',
          email: 'jean.dupont@example.com',
          message: 'Bonjour, je souhaiterais plus d\'informations.'
        })
      });
    });
    
    // Check success message
    await waitFor(() => {
      expect(screen.getByText('Merci ! On te répond vite.')).toBeInTheDocument();
    });
  });

  it('hides form after successful submission', async () => {
    const user = userEvent.setup();
    
    // Mock successful API response
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ success: true })
    });
    
    render(<Contact />);
    
    // Fill and submit form
    await user.type(screen.getByPlaceholderText('Nom'), 'Test User');
    await user.type(screen.getByPlaceholderText('Email'), 'test@example.com');
    await user.type(screen.getByPlaceholderText('Ton message'), 'Test message');
    await user.click(screen.getByRole('button', { name: /envoyer/i }));
    
    await waitFor(() => {
      expect(screen.getByText('Merci ! On te répond vite.')).toBeInTheDocument();
    });
    
    // Form should be hidden
    expect(screen.queryByPlaceholderText('Nom')).not.toBeInTheDocument();
    expect(screen.queryByPlaceholderText('Email')).not.toBeInTheDocument();
    expect(screen.queryByPlaceholderText('Ton message')).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /envoyer/i })).not.toBeInTheDocument();
  });

  it('submits form and calls API correctly', async () => {
    const user = userEvent.setup();
    
    // Mock successful API response
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ success: true })
    });
    
    render(<Contact />);
    
    // Fill and submit form
    await user.type(screen.getByPlaceholderText('Nom'), 'Test User');
    await user.type(screen.getByPlaceholderText('Email'), 'test@example.com');
    await user.type(screen.getByPlaceholderText('Ton message'), 'Test message');
    await user.click(screen.getByRole('button', { name: /envoyer/i }));
    
    await waitFor(() => {
      expect(mockFetch).toHaveBeenCalledWith('/api/contact', {
        method: 'POST',
        body: JSON.stringify({
          name: 'Test User',
          email: 'test@example.com',
          message: 'Test message'
        })
      });
    });
    
    // Should show success message
    await waitFor(() => {
      expect(screen.getByText('Merci ! On te répond vite.')).toBeInTheDocument();
    });
  });

  it('has correct form structure and accessibility', () => {
    render(<Contact />);
    
    const nameInput = screen.getByPlaceholderText('Nom');
    const emailInput = screen.getByPlaceholderText('Email');
    const messageInput = screen.getByPlaceholderText('Ton message');
    const submitButton = screen.getByRole('button', { name: /envoyer/i });
    
    // Check input attributes
    expect(nameInput).toHaveAttribute('name', 'name');
    expect(emailInput).toHaveAttribute('name', 'email');
    expect(messageInput).toHaveAttribute('name', 'message');
    
    // Check required attributes
    expect(nameInput).toBeRequired();
    expect(emailInput).toBeRequired();
    expect(messageInput).toBeRequired();
    
    // Check email input type
    expect(emailInput).toHaveAttribute('type', 'email');
  });

  it('allows user to type in all form fields', async () => {
    const user = userEvent.setup();
    render(<Contact />);
    
    const nameInput = screen.getByPlaceholderText('Nom');
    const emailInput = screen.getByPlaceholderText('Email');
    const messageInput = screen.getByPlaceholderText('Ton message');
    
    await user.type(nameInput, 'Marie Dubois');
    await user.type(emailInput, 'marie@example.com');
    await user.type(messageInput, 'Je suis intéressée par vos activités agricoles.');
    
    expect(nameInput).toHaveValue('Marie Dubois');
    expect(emailInput).toHaveValue('marie@example.com');
    expect(messageInput).toHaveValue('Je suis intéressée par vos activités agricoles.');
  });

  it('maintains form state during typing', async () => {
    const user = userEvent.setup();
    render(<Contact />);
    
    const nameInput = screen.getByPlaceholderText('Nom');
    const emailInput = screen.getByPlaceholderText('Email');
    
    // Type in name field
    await user.type(nameInput, 'Test');
    expect(nameInput).toHaveValue('Test');
    
    // Click on email field and type
    await user.click(emailInput);
    await user.type(emailInput, 'test@example.com');
    
    // Name field should still have its value
    expect(nameInput).toHaveValue('Test');
    expect(emailInput).toHaveValue('test@example.com');
  });
});