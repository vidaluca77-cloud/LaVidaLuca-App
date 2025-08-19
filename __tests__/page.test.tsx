import { render, screen } from '@testing-library/react';
import HomePage from '@/app/page';

describe('HomePage', () => {
  it('renders the home page without crashing', () => {
    render(<HomePage />);

    // Check for some key elements that should be present
    expect(screen.getByText('La Vida Luca')).toBeInTheDocument();
  });

  it('has the correct title structure', () => {
    render(<HomePage />);

    // Check for heading elements
    const headings = screen.getAllByRole('heading');
    expect(headings.length).toBeGreaterThan(0);
  });
});
