import { render, screen, fireEvent } from '@testing-library/react';
import { useRouter } from 'next/navigation';
import Header from '../Header';
import { AuthProvider } from '@/contexts/AuthContext';

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: jest.fn(),
  usePathname: jest.fn(() => '/'),
}));

// Test wrapper with AuthProvider
const TestWrapper = ({ children }: { children: React.ReactNode }) => (
  <AuthProvider>{children}</AuthProvider>
);

describe('Header Component', () => {
  beforeEach(() => {
    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(),
        setItem: jest.fn(),
        removeItem: jest.fn(),
      },
      writable: true,
    });
  });

  it('renders the logo and navigation links', () => {
    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    expect(screen.getByText('La Vida Luca')).toBeInTheDocument();
    expect(screen.getByText('Accueil')).toBeInTheDocument();
    expect(screen.getByText('Catalogue')).toBeInTheDocument();
    expect(screen.getByText('Rejoindre')).toBeInTheDocument();
    expect(screen.getByText('Contact')).toBeInTheDocument();
  });

  it('shows login and register buttons when not authenticated', () => {
    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    expect(screen.getByText('Connexion')).toBeInTheDocument();
    expect(screen.getByText('S\'inscrire')).toBeInTheDocument();
  });

  it('opens auth modal when login button is clicked', () => {
    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    const loginButton = screen.getByText('Connexion');
    fireEvent.click(loginButton);
    
    // Modal should appear - look for the heading specifically
    expect(screen.getByRole('heading', { name: 'Se connecter' })).toBeInTheDocument();
  });

  it('has correct link structure', () => {
    render(
      <TestWrapper>
        <Header />
      </TestWrapper>
    );
    
    const homeLink = screen.getByRole('link', { name: 'La Vida Luca' });
    expect(homeLink).toHaveAttribute('href', '/');
    
    const catalogueLink = screen.getByRole('link', { name: 'Catalogue' });
    expect(catalogueLink).toHaveAttribute('href', '/catalogue');
  });
});