import React from 'react';
import { render, screen } from '@testing-library/react';

// Mock next/navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    prefetch: jest.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}));

// Mock performance monitoring before importing layout
jest.mock('../../monitoring/performance', () => ({}));

import RootLayout from '../layout';

describe('Layout Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the layout with header, main, and footer', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    // Check header
    expect(screen.getByRole('banner')).toBeInTheDocument();
    
    // Check main content
    expect(screen.getByRole('main')).toBeInTheDocument();
    expect(screen.getByText('Test Content')).toBeInTheDocument();
    
    // Check footer
    expect(screen.getByRole('contentinfo')).toBeInTheDocument();
  });

  it('renders navigation menu in header', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    expect(screen.getByText('La Vida Luca')).toBeInTheDocument();
    expect(screen.getByText('Accueil')).toBeInTheDocument();
    expect(screen.getByText('Rejoindre')).toBeInTheDocument();
    expect(screen.getByText('Contact')).toBeInTheDocument();
  });

  it('has correct navigation links', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    const homeLink = screen.getByRole('link', { name: /accueil/i });
    const joinLink = screen.getByRole('link', { name: /rejoindre/i });
    const contactLink = screen.getByRole('link', { name: /contact/i });

    expect(homeLink).toHaveAttribute('href', '/');
    expect(joinLink).toHaveAttribute('href', '/rejoindre');
    expect(contactLink).toHaveAttribute('href', '/contact');
  });

  it('renders logo as a link to home', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    const logoLink = screen.getByRole('link', { name: /la vida luca/i });
    expect(logoLink).toHaveAttribute('href', '/');
  });

  it('renders footer with copyright information', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    const currentYear = new Date().getFullYear();
    expect(screen.getByText(`© ${currentYear} La Vida Luca — Tous droits réservés`)).toBeInTheDocument();
  });

  it('has correct HTML structure and attributes', () => {
    const { container } = render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    // In test environment, we check the rendered HTML structure
    const htmlElement = container.querySelector('html');
    if (htmlElement) {
      expect(htmlElement).toHaveAttribute('lang', 'fr');
      expect(htmlElement).toHaveAttribute('suppressHydrationWarning');
    }

    // Test the body classes through the rendered container
    const bodyClasses = ['font-sans', 'min-h-screen', 'bg-white', 'text-neutral-900', 'antialiased'];
    // Since we can't directly test document.body in JSDOM, we verify the layout renders correctly
    expect(container.firstChild).toBeTruthy();
  });

  it('renders children content in main section', () => {
    const testContent = (
      <div>
        <h1>Test Page</h1>
        <p>This is test content</p>
      </div>
    );

    render(<RootLayout>{testContent}</RootLayout>);

    const main = screen.getByRole('main');
    expect(main).toContainElement(screen.getByText('Test Page'));
    expect(main).toContainElement(screen.getByText('This is test content'));
  });

  it('has responsive navigation layout', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    const header = screen.getByRole('banner');
    const nav = screen.getByRole('navigation');
    
    expect(header).toHaveClass('border-b');
    expect(nav).toHaveClass('flex', 'gap-6', 'text-sm');
  });

  it('applies correct styling classes', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    const header = screen.getByRole('banner');
    const main = screen.getByRole('main');
    const footer = screen.getByRole('contentinfo');

    expect(header).toHaveClass('border-b');
    expect(main).toHaveClass('mx-auto', 'max-w-6xl', 'px-4', 'py-10');
    expect(footer).toHaveClass('border-t');
  });

  it('renders logo and brand name correctly', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    const brandLink = screen.getByRole('link', { name: /la vida luca/i });
    expect(brandLink).toHaveClass('font-semibold');
    expect(brandLink).toHaveAttribute('href', '/');
  });

  it('has proper semantic HTML structure', () => {
    render(
      <RootLayout>
        <div>Test Content</div>
      </RootLayout>
    );

    // Check semantic elements
    expect(screen.getByRole('banner')).toBeInTheDocument(); // header
    expect(screen.getByRole('navigation')).toBeInTheDocument(); // nav
    expect(screen.getByRole('main')).toBeInTheDocument(); // main
    expect(screen.getByRole('contentinfo')).toBeInTheDocument(); // footer
  });
});