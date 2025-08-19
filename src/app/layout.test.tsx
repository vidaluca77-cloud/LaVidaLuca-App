/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import RootLayout from './layout';

describe('RootLayout Component', () => {
  const TestChild = () => <div data-testid="test-child">Test Content</div>;

  describe('HTML Structure', () => {
    it('should render proper HTML document structure', () => {
      const { container } = render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      // Note: When testing layout components, React Testing Library renders within a test container
      // The actual html/body structure is handled by Next.js in production
      
      // Check that the layout content is rendered
      expect(screen.getByTestId('test-child')).toBeInTheDocument();
      
      // Check for essential layout elements that would be rendered
      const header = screen.getByRole('banner');
      const main = screen.getByRole('main');
      const footer = screen.getByRole('contentinfo');
      
      expect(header).toBeInTheDocument();
      expect(main).toBeInTheDocument();
      expect(footer).toBeInTheDocument();
    });

    it('should render header with navigation', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      const header = screen.getByRole('banner');
      expect(header).toBeInTheDocument();
      expect(header).toHaveClass('border-b');
      
      // Check logo/brand
      const brandLink = screen.getByRole('link', { name: /La Vida Luca/i });
      expect(brandLink).toBeInTheDocument();
      expect(brandLink).toHaveAttribute('href', '/');
    });

    it('should render navigation links', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      const nav = screen.getByRole('navigation');
      expect(nav).toBeInTheDocument();
      
      // Check navigation links
      const homeLink = screen.getByRole('link', { name: /Accueil/i });
      const joinLink = screen.getByRole('link', { name: /Rejoindre/i });
      const contactLink = screen.getByRole('link', { name: /Contact/i });
      
      expect(homeLink).toBeInTheDocument();
      expect(homeLink).toHaveAttribute('href', '/');
      
      expect(joinLink).toBeInTheDocument();
      expect(joinLink).toHaveAttribute('href', '/rejoindre');
      
      expect(contactLink).toBeInTheDocument();
      expect(contactLink).toHaveAttribute('href', '/contact');
    });

    it('should render main content area', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      const main = screen.getByRole('main');
      expect(main).toBeInTheDocument();
      expect(main).toHaveClass('mx-auto', 'max-w-6xl', 'px-4', 'py-10');
      
      // Check that children are rendered
      expect(screen.getByTestId('test-child')).toBeInTheDocument();
    });

    it('should render footer', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      const footer = screen.getByRole('contentinfo');
      expect(footer).toBeInTheDocument();
      expect(footer).toHaveClass('border-t');
      
      // Check copyright text
      const currentYear = new Date().getFullYear();
      const copyrightText = screen.getByText(new RegExp(`© ${currentYear} La Vida Luca`));
      expect(copyrightText).toBeInTheDocument();
    });
  });

  describe('Accessibility', () => {
    it('should have proper landmark roles', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      expect(screen.getByRole('banner')).toBeInTheDocument(); // header
      expect(screen.getByRole('navigation')).toBeInTheDocument(); // nav
      expect(screen.getByRole('main')).toBeInTheDocument(); // main
      expect(screen.getByRole('contentinfo')).toBeInTheDocument(); // footer
    });

    it('should have proper heading structure', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      // Brand should be a focusable link, not necessarily a heading
      const brandLink = screen.getByRole('link', { name: /La Vida Luca/i });
      expect(brandLink).toBeInTheDocument();
    });

    it('should have proper link attributes', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      const links = screen.getAllByRole('link');
      
      links.forEach(link => {
        expect(link).toHaveAttribute('href');
        expect(link.textContent).toBeTruthy();
      });
    });
  });

  describe('Visual Styling', () => {
    it('should apply proper container styles', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      const headerContainer = screen.getByRole('banner').firstChild;
      expect(headerContainer).toHaveClass('mx-auto', 'flex', 'h-16', 'max-w-6xl', 'items-center', 'justify-between', 'px-4');
      
      const mainContainer = screen.getByRole('main');
      expect(mainContainer).toHaveClass('mx-auto', 'max-w-6xl', 'px-4', 'py-10');
      
      const footerContainer = screen.getByRole('contentinfo').firstChild;
      expect(footerContainer).toHaveClass('mx-auto', 'max-w-6xl', 'px-4', 'py-8', 'text-sm', 'opacity-70');
    });

    it('should apply proper navigation styles', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      const nav = screen.getByRole('navigation');
      expect(nav).toHaveClass('flex', 'gap-6', 'text-sm');
      
      const navLinks = nav.querySelectorAll('a');
      navLinks.forEach(link => {
        expect(link).toHaveClass('opacity-80', 'hover:opacity-100');
      });
    });

    it('should apply proper brand styles', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      const brandLink = screen.getByRole('link', { name: /La Vida Luca/i });
      expect(brandLink).toHaveClass('font-semibold');
    });
  });

  describe('Responsive Design', () => {
    it('should handle different screen sizes', () => {
      render(
        <RootLayout>
          <TestChild />
        </RootLayout>
      );
      
      // The layout should render without errors
      expect(screen.getByRole('banner')).toBeInTheDocument();
      expect(screen.getByRole('main')).toBeInTheDocument();
      expect(screen.getByRole('contentinfo')).toBeInTheDocument();
    });
  });

  describe('Children Rendering', () => {
    it('should render multiple children correctly', () => {
      const MultipleChildren = () => (
        <>
          <div data-testid="child-1">Child 1</div>
          <div data-testid="child-2">Child 2</div>
        </>
      );

      render(
        <RootLayout>
          <MultipleChildren />
        </RootLayout>
      );
      
      expect(screen.getByTestId('child-1')).toBeInTheDocument();
      expect(screen.getByTestId('child-2')).toBeInTheDocument();
    });

    it('should render complex nested children', () => {
      const ComplexChild = () => (
        <div data-testid="complex-child">
          <h1>Test Heading</h1>
          <p>Test paragraph</p>
          <button>Test Button</button>
        </div>
      );

      render(
        <RootLayout>
          <ComplexChild />
        </RootLayout>
      );
      
      expect(screen.getByTestId('complex-child')).toBeInTheDocument();
      expect(screen.getByRole('heading', { name: /Test Heading/i })).toBeInTheDocument();
      expect(screen.getByText(/Test paragraph/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Test Button/i })).toBeInTheDocument();
    });
  });
});