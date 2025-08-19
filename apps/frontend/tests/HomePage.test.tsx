import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import HomePage from '../src/components/HomePage';

// Mock the useAuth hook since we're not testing authentication
jest.mock('../src/hooks/useAuth', () => ({
  useAuth: () => ({
    user: null,
    login: jest.fn(),
    register: jest.fn(),
    logout: jest.fn(),
    isLoading: false,
  }),
}));

describe('HomePage', () => {
  it('renders the main heading', () => {
    render(<HomePage />);
    
    const heading = screen.getByRole('heading', { name: /la vida luca/i });
    expect(heading).toBeInTheDocument();
  });

  it('shows "Rejoindre le projet" button for non-authenticated users', () => {
    render(<HomePage />);
    
    const joinButton = screen.getByRole('link', { name: /rejoindre le projet/i });
    expect(joinButton).toBeInTheDocument();
  });

  it('displays the vision section', () => {
    render(<HomePage />);
    
    const visionHeading = screen.getByRole('heading', { name: /notre vision/i });
    expect(visionHeading).toBeInTheDocument();
    
    const formationSection = screen.getByText(/former et accompagner les jeunes/i);
    expect(formationSection).toBeInTheDocument();
  });
});