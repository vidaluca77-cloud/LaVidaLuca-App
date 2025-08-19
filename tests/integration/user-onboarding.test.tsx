import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../../src/app/page';

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

describe('User Onboarding and AI Matching Flow', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('completes full onboarding flow and receives AI suggestions', async () => {
    const user = userEvent.setup();
    render(<App />);

    // 1. Start from home page
    expect(screen.getByText(/Le cœur/i)).toBeInTheDocument();

    // 2. Click "Proposer mon aide" to start onboarding
    const proposeButton = screen.getByText('Proposer mon aide');
    await user.click(proposeButton);

    await waitFor(() => {
      expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
    });

    // 3. Step 1: Select skills
    expect(screen.getByText('Vos compétences :')).toBeInTheDocument();
    
    // Select multiple relevant skills
    const elevageSkill = screen.getByText('elevage');
    const hygieneSkill = screen.getByText('hygiene');
    const patienceSkill = screen.getByText('patience');
    
    await user.click(elevageSkill);
    await user.click(hygieneSkill);
    await user.click(patienceSkill);

    // Verify skills are selected
    expect(elevageSkill).toHaveClass('bg-green-500');
    expect(hygieneSkill).toHaveClass('bg-green-500');
    expect(patienceSkill).toHaveClass('bg-green-500');

    // Move to next step
    await user.click(screen.getByText('Suivant'));

    // 4. Step 2: Select availability
    await waitFor(() => {
      expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
    });

    const weekendAvail = screen.getByText('weekend');
    const matinAvail = screen.getByText('matin');
    
    await user.click(weekendAvail);
    await user.click(matinAvail);

    expect(weekendAvail).toHaveClass('bg-green-500');
    expect(matinAvail).toHaveClass('bg-green-500');

    await user.click(screen.getByText('Suivant'));

    // 5. Step 3: Enter location
    await waitFor(() => {
      expect(screen.getByText('Votre région')).toBeInTheDocument();
    });

    const locationInput = screen.getByPlaceholderText(/Ex: Ile-de-France/i);
    await user.type(locationInput, 'Calvados');
    expect(locationInput).toHaveValue('Calvados');

    await user.click(screen.getByText('Suivant'));

    // 6. Step 4: Select preferences
    await waitFor(() => {
      expect(screen.getByText('Vos préférences')).toBeInTheDocument();
    });

    // Select Agriculture and Social categories
    const agriPreference = screen.getByText('Agriculture');
    const socialPreference = screen.getByText('Animation');
    
    await user.click(agriPreference);
    await user.click(socialPreference);

    expect(agriPreference).toHaveClass('bg-green-500');
    expect(socialPreference).toHaveClass('bg-green-500');

    // Complete onboarding
    await user.click(screen.getByText('Voir mes propositions'));

    // 7. Verify AI suggestions page
    await waitFor(() => {
      expect(screen.getByText('Vos propositions personnalisées')).toBeInTheDocument();
      expect(screen.getByText('Notre IA a sélectionné ces activités spécialement pour vous')).toBeInTheDocument();
    });

    // 8. Verify suggestion cards are displayed
    const suggestionCards = screen.getAllByText(/Voir le guide & m'inscrire/);
    expect(suggestionCards.length).toBeGreaterThan(0);

    // Verify compatibility scores are shown
    const compatibilityScores = screen.getAllByText(/%/);
    expect(compatibilityScores.length).toBeGreaterThan(0);

    // 9. Check specific activity suggestions based on profile
    // Should include animal care activities due to "elevage" skill
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();
  });

  it('navigates through onboarding with different user profiles', async () => {
    const user = userEvent.setup();
    
    const profiles = [
      {
        name: 'Agricultural Enthusiast',
        skills: ['elevage', 'soins_animaux', 'sol'],
        availability: ['weekend', 'vacances'],
        location: 'Normandie',
        preferences: ['Agriculture', 'Environnement']
      },
      {
        name: 'Creative Artisan',
        skills: ['creativite', 'precision', 'bois'],
        availability: ['apres-midi', 'semaine'],
        location: 'Bretagne',
        preferences: ['Artisanat', 'Transformation']
      },
      {
        name: 'Social Animator',
        skills: ['pedagogie', 'accueil', 'expression'],
        availability: ['matin', 'weekend'],
        location: 'Île-de-France',
        preferences: ['Animation']
      }
    ];

    for (const profile of profiles) {
      const { rerender } = render(<App />);

      // Start onboarding
      const proposeButton = screen.getByText('Proposer mon aide');
      await user.click(proposeButton);

      await waitFor(() => {
        expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
      });

      // Select skills for this profile
      for (const skill of profile.skills) {
        const skillButton = screen.getByText(skill);
        await user.click(skillButton);
      }
      await user.click(screen.getByText('Suivant'));

      // Select availability
      await waitFor(() => {
        expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
      });
      for (const avail of profile.availability) {
        const availButton = screen.getByText(avail);
        await user.click(availButton);
      }
      await user.click(screen.getByText('Suivant'));

      // Enter location
      await waitFor(() => {
        expect(screen.getByText('Votre région')).toBeInTheDocument();
      });
      const locationInput = screen.getByPlaceholderText(/Ex: Ile-de-France/i);
      await user.type(locationInput, profile.location);
      await user.click(screen.getByText('Suivant'));

      // Select preferences
      await waitFor(() => {
        expect(screen.getByText('Vos préférences')).toBeInTheDocument();
      });
      for (const pref of profile.preferences) {
        const prefButton = screen.getByText(pref);
        await user.click(prefButton);
      }
      await user.click(screen.getByText('Voir mes propositions'));

      // Verify suggestions page
      await waitFor(() => {
        expect(screen.getByText('Vos propositions personnalisées')).toBeInTheDocument();
      });

      // Verify personalized suggestions are shown
      const suggestionCards = screen.getAllByText(/Voir le guide & m'inscrire/);
      expect(suggestionCards.length).toBeGreaterThan(0);

      // Reset for next profile
      rerender(<App />);
    }
  });

  it('handles back navigation through onboarding steps', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Start onboarding
    const proposeButton = screen.getByText('Proposer mon aide');
    await user.click(proposeButton);

    await waitFor(() => {
      expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
    });

    // Go through all steps forward
    await user.click(screen.getByText('elevage'));
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
    });
    await user.click(screen.getByText('weekend'));
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Votre région')).toBeInTheDocument();
    });
    await user.type(screen.getByPlaceholderText(/Ex: Ile-de-France/i), 'Test Region');
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Vos préférences')).toBeInTheDocument();
    });

    // Now navigate back through steps
    await user.click(screen.getByText('Retour'));

    await waitFor(() => {
      expect(screen.getByText('Votre région')).toBeInTheDocument();
    });

    await user.click(screen.getByText('Retour'));

    await waitFor(() => {
      expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
    });

    await user.click(screen.getByText('Retour'));

    await waitFor(() => {
      expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
    });
  });

  it('allows users to restart onboarding from suggestions page', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Complete onboarding quickly
    const proposeButton = screen.getByText('Proposer mon aide');
    await user.click(proposeButton);

    await waitFor(() => {
      expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
    });

    // Quick completion
    await user.click(screen.getByText('elevage'));
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
    });
    await user.click(screen.getByText('weekend'));
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Votre région')).toBeInTheDocument();
    });
    await user.type(screen.getByPlaceholderText(/Ex: Ile-de-France/i), 'Test');
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Vos préférences')).toBeInTheDocument();
    });
    await user.click(screen.getByText('Agriculture'));
    await user.click(screen.getByText('Voir mes propositions'));

    // Reach suggestions page
    await waitFor(() => {
      expect(screen.getByText('Vos propositions personnalisées')).toBeInTheDocument();
    });

    // Click restart button
    const restartButton = screen.getByText('Refaire le questionnaire');
    await user.click(restartButton);

    // Should reload the page (based on window.location.reload())
    // In this test environment, we can't test actual page reload,
    // but we can verify the button exists and is clickable
    expect(restartButton).toBeInTheDocument();
  });

  it('provides detailed activity information in suggestions', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Complete onboarding to reach suggestions
    const proposeButton = screen.getByText('Proposer mon aide');
    await user.click(proposeButton);

    await waitFor(() => {
      expect(screen.getByText('Comment souhaitez-vous participer ?')).toBeInTheDocument();
    });

    await user.click(screen.getByText('elevage'));
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Vos disponibilités')).toBeInTheDocument();
    });
    await user.click(screen.getByText('weekend'));
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Votre région')).toBeInTheDocument();
    });
    await user.type(screen.getByPlaceholderText(/Ex: Ile-de-France/i), 'Calvados');
    await user.click(screen.getByText('Suivant'));

    await waitFor(() => {
      expect(screen.getByText('Vos préférences')).toBeInTheDocument();
    });
    await user.click(screen.getByText('Agriculture'));
    await user.click(screen.getByText('Voir mes propositions'));

    await waitFor(() => {
      expect(screen.getByText('Vos propositions personnalisées')).toBeInTheDocument();
    });

    // Verify detailed information is shown for suggestions
    expect(screen.getByText(/compatibilité/)).toBeInTheDocument();
    expect(screen.getByText(/Pourquoi cette activité vous correspond :/)).toBeInTheDocument();
    
    // Check for activity details buttons
    const detailButtons = screen.getAllByText('Détails');
    const guideButtons = screen.getAllByText(/Voir le guide & m'inscrire/);
    
    expect(detailButtons.length).toBeGreaterThan(0);
    expect(guideButtons.length).toBeGreaterThan(0);
  });
});