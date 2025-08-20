/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from './page';

describe('HomePage Component', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    // Reset any DOM state
    document.body.innerHTML = '';
  });

  describe('Initial Render', () => {
    it('should render the main heading', () => {
      render(<App />);
      
      const heading = screen.getByRole('heading', { level: 1 });
      expect(heading).toBeInTheDocument();
      expect(heading).toHaveTextContent(/Le cœur.*avant l'argent/);
    });

    it('should render the hero section with description', () => {
      render(<App />);
      
      const description = screen.getByText(/Réseau national de fermes pédagogiques/);
      expect(description).toBeInTheDocument();
    });

    it('should render primary action buttons', () => {
      render(<App />);
      
      const proposeButton = screen.getByRole('button', { name: /Proposer mon aide/i });
      const discoverButton = screen.getByRole('button', { name: /Découvrir nos activités/i });
      
      expect(proposeButton).toBeInTheDocument();
      expect(discoverButton).toBeInTheDocument();
    });
  });

  describe('Mission Section', () => {
    it('should render mission section with three pillars', () => {
      render(<App />);
      
      const missionHeading = screen.getByRole('heading', { name: /Notre mission/i });
      expect(missionHeading).toBeInTheDocument();

      // Check for the three pillars using headings
      expect(screen.getByRole('heading', { name: /Formation des jeunes/i })).toBeInTheDocument();
      expect(screen.getByRole('heading', { name: /Agriculture vivante/i })).toBeInTheDocument();
      expect(screen.getByRole('heading', { name: /Insertion sociale/i })).toBeInTheDocument();
    });

    it('should have proper icons for each pillar', () => {
      render(<App />);
      
      // Our mocked icons should be present
      expect(screen.getByTestId('academic-cap-icon')).toBeInTheDocument();
      expect(screen.getByTestId('globe-alt-icon')).toBeInTheDocument();
      expect(screen.getByTestId('heart-icon')).toBeInTheDocument();
    });
  });

  describe('Contact Section', () => {
    it('should render contact information', () => {
      render(<App />);
      
      const contactHeading = screen.getByRole('heading', { name: /Rejoignez l'aventure/i });
      expect(contactHeading).toBeInTheDocument();

      // Check for contact details
      expect(screen.getByText('@lavidaluca77')).toBeInTheDocument();
      expect(screen.getByText('vidaluca77@gmail.com')).toBeInTheDocument();
    });
  });

  describe('Navigation', () => {
    it('should render navigation with proper links', () => {
      render(<App />);
      
      const logo = screen.getByText('La Vida Luca');
      expect(logo).toBeInTheDocument();

      // Check for navigation links by href since they're not in nav role
      const links = screen.getAllByRole('link');
      const navLinks = links.filter(link => 
        link.getAttribute('href') === '#mission' ||
        link.getAttribute('href') === '#activites' || 
        link.getAttribute('href') === '#contact'
      );

      expect(navLinks.length).toBe(3);
    });
  });

  describe('User Interactions', () => {
    it('should handle "Proposer mon aide" button click', async () => {
      render(<App />);
      
      const proposeButton = screen.getByRole('button', { name: /Proposer mon aide/i });
      
      await user.click(proposeButton);
      
      // After clicking, should navigate to onboarding flow
      await waitFor(() => {
        expect(screen.getByText(/Comment souhaitez-vous participer/i)).toBeInTheDocument();
      });
    });

    it('should handle "Découvrir nos activités" button click', async () => {
      render(<App />);
      
      const discoverButton = screen.getByRole('button', { name: /Découvrir nos activités/i });
      
      await user.click(discoverButton);
      
      // After clicking, should navigate to catalog
      await waitFor(() => {
        expect(screen.getByText(/Catalogue des activités/i)).toBeInTheDocument();
      });
    });
  });

  describe('Accessibility', () => {
    it('should have proper heading hierarchy', () => {
      render(<App />);
      
      const h1 = screen.getByRole('heading', { level: 1 });
      const h2s = screen.getAllByRole('heading', { level: 2 });
      const h3s = screen.getAllByRole('heading', { level: 3 });
      
      expect(h1).toBeInTheDocument();
      expect(h2s.length).toBeGreaterThan(0);
      expect(h3s.length).toBeGreaterThan(0);
    });

    it('should have proper link accessibility', () => {
      render(<App />);
      
      const links = screen.getAllByRole('link');
      
      links.forEach(link => {
        // Each link should have accessible text
        expect(link).toHaveAttribute('href');
        expect(link.textContent).toBeTruthy();
      });
    });

    it('should have proper button accessibility', () => {
      render(<App />);
      
      const buttons = screen.getAllByRole('button');
      
      buttons.forEach(button => {
        // Each button should have accessible text
        expect(button.textContent).toBeTruthy();
      });
    });
  });

  describe('Responsive Design', () => {
    it('should handle mobile viewport', () => {
      // Mock mobile viewport
      Object.defineProperty(window, 'matchMedia', {
        writable: true,
        value: jest.fn().mockImplementation(query => ({
          matches: query === '(max-width: 768px)',
          media: query,
          onchange: null,
          addListener: jest.fn(),
          removeListener: jest.fn(),
          addEventListener: jest.fn(),
          removeEventListener: jest.fn(),
          dispatchEvent: jest.fn(),
        })),
      });

      render(<App />);
      
      // Component should render without errors on mobile
      expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
    });
  });
});