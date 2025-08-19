import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../page';

// Mock Heroicons
jest.mock('@heroicons/react/24/outline', () => ({
  HeartIcon: () => <div data-testid="heart-icon">Heart</div>,
  AcademicCapIcon: () => <div data-testid="academic-cap-icon">Academic</div>,
  GlobeAltIcon: () => <div data-testid="globe-alt-icon">Globe</div>,
  MapPinIcon: () => <div data-testid="map-pin-icon">MapPin</div>,
  ClockIcon: () => <div data-testid="clock-icon">Clock</div>,
  ShieldCheckIcon: () => <div data-testid="shield-check-icon">Shield</div>,
  UserGroupIcon: () => <div data-testid="user-group-icon">UserGroup</div>,
  StarIcon: () => <div data-testid="star-icon">Star</div>,
}));

describe('Home Page', () => {
  beforeEach(() => {
    // Reset any mocks
    jest.clearAllMocks();
  });

  describe('HomePage Component', () => {
    it('renders the main heading', () => {
      render(<App />);
      expect(screen.getByText(/Le cœur/i)).toBeInTheDocument();
      expect(screen.getByText(/avant l'argent/i)).toBeInTheDocument();
    });

    it('renders navigation menu', () => {
      render(<App />);
      expect(screen.getByText('Notre mission')).toBeInTheDocument();
      expect(screen.getByText('Activités')).toBeInTheDocument();
      expect(screen.getByText('Contact')).toBeInTheDocument();
    });

    it('renders mission section with three pillars', () => {
      render(<App />);
      expect(screen.getByText('Formation des jeunes')).toBeInTheDocument();
      expect(screen.getByText('Agriculture vivante')).toBeInTheDocument();
      expect(screen.getByText('Insertion sociale')).toBeInTheDocument();
    });

    it('renders contact information', () => {
      render(<App />);
      expect(screen.getByText('@lavidaluca77')).toBeInTheDocument();
      expect(screen.getByText('vidaluca77@gmail.com')).toBeInTheDocument();
    });

    it('navigates to onboarding when "Proposer mon aide" is clicked', async () => {
      const user = userEvent.setup();
      render(<App />);
      
      const proposeButton = screen.getByText('Proposer mon aide');
      await user.click(proposeButton);
      
      await waitFor(() => {
        expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
      });
    });

    it('navigates to catalog when "Découvrir nos activités" is clicked', async () => {
      const user = userEvent.setup();
      render(<App />);
      
      const discoverButton = screen.getByText('Découvrir nos activités');
      await user.click(discoverButton);
      
      await waitFor(() => {
        expect(screen.getByText('Catalogue des activités')).toBeInTheDocument();
      });
    });
  });

  describe('OnboardingFlow Component', () => {
    beforeEach(() => {
      const user = userEvent.setup();
      render(<App />);
      const proposeButton = screen.getByText('Proposer mon aide');
      user.click(proposeButton);
    });

    it('allows user to select skills in step 1', async () => {
      const user = userEvent.setup();
      render(<App />);
      
      const proposeButton = screen.getByText('Proposer mon aide');
      await user.click(proposeButton);
      
      await waitFor(() => {
        expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
      });

      // Check if some skill buttons are present
      expect(screen.getByText('elevage')).toBeInTheDocument();
      expect(screen.getByText('hygiene')).toBeInTheDocument();
      
      // Click on a skill
      const skillButton = screen.getByText('elevage');
      await user.click(skillButton);
      
      // Button should be selected (will have different styling)
      expect(skillButton).toHaveClass('bg-green-500');
    });

    it('progresses through onboarding steps', async () => {
      const user = userEvent.setup();
      render(<App />);
      
      const proposeButton = screen.getByText('Proposer mon aide');
      await user.click(proposeButton);
      
      await waitFor(() => {
        expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
      });

      // Step 1 - Select skills and go to next
      const nextButton = screen.getByText('Suivant');
      await user.click(nextButton);
      
      await waitFor(() => {
        expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
      });

      // Step 2 - Select availability and go to next
      const nextButton2 = screen.getByText('Suivant');
      await user.click(nextButton2);
      
      await waitFor(() => {
        expect(screen.getByText('Votre région')).toBeInTheDocument();
      });

      // Step 3 - Enter location and go to next
      const locationInput = screen.getByPlaceholderText(/Ex: Ile-de-France/i);
      await user.type(locationInput, 'Île-de-France');
      
      const nextButton3 = screen.getByText('Suivant');
      await user.click(nextButton3);
      
      await waitFor(() => {
        expect(screen.getByText('Vos préférences')).toBeInTheDocument();
      });
    });

    it('can go back through onboarding steps', async () => {
      const user = userEvent.setup();
      render(<App />);
      
      const proposeButton = screen.getByText('Proposer mon aide');
      await user.click(proposeButton);
      
      await waitFor(() => {
        expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
      });

      // Go to step 2
      const nextButton = screen.getByText('Suivant');
      await user.click(nextButton);
      
      await waitFor(() => {
        expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
      });

      // Go back to step 1
      const backButton = screen.getByText('Retour');
      await user.click(backButton);
      
      await waitFor(() => {
        expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
      });
    });
  });

  describe('ActivityCatalog Component', () => {
    beforeEach(async () => {
      const user = userEvent.setup();
      render(<App />);
      const discoverButton = screen.getByText('Découvrir nos activités');
      await user.click(discoverButton);
    });

    it('renders catalog with activities', async () => {
      const user = userEvent.setup();
      render(<App />);
      const discoverButton = screen.getByText('Découvrir nos activités');
      await user.click(discoverButton);
      
      await waitFor(() => {
        expect(screen.getByText('Catalogue des activités')).toBeInTheDocument();
        expect(screen.getByText('30 activités pour apprendre et découvrir l\'agriculture vivante')).toBeInTheDocument();
      });
    });

    it('filters activities by category', async () => {
      const user = userEvent.setup();
      render(<App />);
      const discoverButton = screen.getByText('Découvrir nos activités');
      await user.click(discoverButton);
      
      await waitFor(() => {
        expect(screen.getByText('Catalogue des activités')).toBeInTheDocument();
      });

      // Check if filter buttons are present
      expect(screen.getByText('Toutes (30)')).toBeInTheDocument();
      expect(screen.getByText('Agriculture (6)')).toBeInTheDocument();
      
      // Click on Agriculture filter
      const agriFilter = screen.getByText('Agriculture (6)');
      await user.click(agriFilter);
      
      // Should show agriculture activities
      expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();
    });
  });

  describe('SuggestionsPage Component', () => {
    it('completes onboarding flow and shows suggestions', async () => {
      const user = userEvent.setup();
      render(<App />);
      
      // Start onboarding
      const proposeButton = screen.getByText('Proposer mon aide');
      await user.click(proposeButton);
      
      await waitFor(() => {
        expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
      });

      // Step 1 - Select a skill
      const skillButton = screen.getByText('elevage');
      await user.click(skillButton);
      await user.click(screen.getByText('Suivant'));
      
      // Step 2 - Select availability
      await waitFor(() => {
        expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
      });
      const weekendButton = screen.getByText('weekend');
      await user.click(weekendButton);
      await user.click(screen.getByText('Suivant'));
      
      // Step 3 - Enter location
      await waitFor(() => {
        expect(screen.getByText('Votre région')).toBeInTheDocument();
      });
      const locationInput = screen.getByPlaceholderText(/Ex: Ile-de-France/i);
      await user.type(locationInput, 'Calvados');
      await user.click(screen.getByText('Suivant'));
      
      // Step 4 - Select preferences
      await waitFor(() => {
        expect(screen.getByText('Vos préférences')).toBeInTheDocument();
      });
      const agriPreference = screen.getByText('Agriculture');
      await user.click(agriPreference);
      await user.click(screen.getByText('Voir mes propositions'));
      
      // Should show suggestions page
      await waitFor(() => {
        expect(screen.getByText('Vos propositions personnalisées')).toBeInTheDocument();
        expect(screen.getByText('Notre IA a sélectionné ces activités spécialement pour vous')).toBeInTheDocument();
      });
    });
  });
});