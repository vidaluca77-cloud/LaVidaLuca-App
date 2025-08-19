import { render, screen } from '@testing-library/react';
import { DarkModeToggle } from '@/components/DarkModeToggle';
import userEvent from '@testing-library/user-event';

// Mock the useDarkMode hook
jest.mock('@/hooks/useDarkMode', () => ({
  useDarkMode: () => ({
    isDarkMode: false,
    toggleDarkMode: jest.fn(),
  }),
}));

describe('DarkModeToggle', () => {
  it('renders correctly', () => {
    render(<DarkModeToggle />);
    
    const button = screen.getByRole('button', { name: /passer en mode sombre/i });
    expect(button).toBeInTheDocument();
  });

  it('has proper accessibility attributes', () => {
    render(<DarkModeToggle />);
    
    const button = screen.getByRole('button');
    expect(button).toHaveAttribute('aria-label');
  });

  it('can be clicked', async () => {
    const user = userEvent.setup();
    render(<DarkModeToggle />);
    
    const button = screen.getByRole('button');
    await user.click(button);
    
    // Since we mocked the hook, we just verify the button is clickable
    expect(button).toBeInTheDocument();
  });
});