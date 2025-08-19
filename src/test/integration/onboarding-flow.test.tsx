/**
 * @jest-environment jsdom
 */
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from '../../app/page';

describe('User Onboarding Flow Integration', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    // Reset any DOM state
    document.body.innerHTML = '';
  });

  describe('Complete Onboarding Flow', () => {
    it('should allow user to complete the full onboarding process', async () => {
      render(<App />);
      
      // 1. Start from homepage
      expect(screen.getByRole('heading', { name: /Le cœur.*avant l'argent/i })).toBeInTheDocument();
      
      // 2. Click "Proposer mon aide" to start onboarding
      const proposeButton = screen.getByRole('button', { name: /Proposer mon aide/i });
      await user.click(proposeButton);
      
      // 3. Should navigate to onboarding step 1 (skills)
      await waitFor(() => {
        expect(screen.getByText(/Comment souhaitez-vous participer/i)).toBeInTheDocument();
        expect(screen.getByText(/Sélectionnez vos compétences/i)).toBeInTheDocument();
      });
      
      // 4. Select some skills
      const elevageSkill = screen.getByRole('button', { name: /elevage/i });
      const hygieneSkill = screen.getByRole('button', { name: /hygiene/i });
      
      await user.click(elevageSkill);
      await user.click(hygieneSkill);
      
      // Skills should be selected (active state)
      expect(elevageSkill).toHaveClass('bg-green-500', 'text-white');
      expect(hygieneSkill).toHaveClass('bg-green-500', 'text-white');
      
      // 5. Go to next step (availability)
      const nextButton1 = screen.getByRole('button', { name: /Suivant/i });
      await user.click(nextButton1);
      
      await waitFor(() => {
        expect(screen.getByText(/Vos disponibilités/i)).toBeInTheDocument();
      });
      
      // 6. Select availability
      const weekendOption = screen.getByRole('button', { name: /weekend/i });
      const morningOption = screen.getByRole('button', { name: /matin/i });
      
      await user.click(weekendOption);
      await user.click(morningOption);
      
      expect(weekendOption).toHaveClass('bg-green-500', 'text-white');
      expect(morningOption).toHaveClass('bg-green-500', 'text-white');
      
      // 7. Go to next step (location)
      const nextButton2 = screen.getByRole('button', { name: /Suivant/i });
      await user.click(nextButton2);
      
      await waitFor(() => {
        expect(screen.getByText(/Votre région/i)).toBeInTheDocument();
      });
      
      // 8. Enter location
      const locationInput = screen.getByPlaceholderText(/Ex: Ile-de-France/i);
      await user.type(locationInput, 'Ile-de-France');
      
      expect(locationInput).toHaveValue('Ile-de-France');
      
      // 9. Go to next step (preferences)
      const nextButton3 = screen.getByRole('button', { name: /Suivant/i });
      await user.click(nextButton3);
      
      await waitFor(() => {
        expect(screen.getByText(/Vos préférences/i)).toBeInTheDocument();
      });
      
      // 10. Select preferences
      const agriPreference = screen.getByRole('button', { name: /Agriculture/i });
      const naturePreference = screen.getByRole('button', { name: /Environnement/i });
      
      await user.click(agriPreference);
      await user.click(naturePreference);
      
      expect(agriPreference).toHaveClass('bg-green-500', 'text-white');
      expect(naturePreference).toHaveClass('bg-green-500', 'text-white');
      
      // 11. Complete onboarding
      const completeButton = screen.getByRole('button', { name: /Voir mes propositions/i });
      await user.click(completeButton);
      
      // 12. Should navigate to suggestions page
      await waitFor(() => {
        expect(screen.getByText(/Vos propositions personnalisées/i)).toBeInTheDocument();
        expect(screen.getByText(/Notre IA a sélectionné ces activités/i)).toBeInTheDocument();
      });
      
      // 13. Should show activity suggestions
      const suggestions = screen.getAllByText(/#\d+/); // Activity numbers
      expect(suggestions.length).toBeGreaterThan(0);
      
      // Should show compatibility scores
      const scores = screen.getAllByText(/\d+%/);
      expect(scores.length).toBeGreaterThan(0);
    }, 30000); // Increase timeout for this long test

    it('should allow user to navigate back through onboarding steps', async () => {
      render(<App />);
      
      // Start onboarding
      const proposeButton = screen.getByRole('button', { name: /Proposer mon aide/i });
      await user.click(proposeButton);
      
      // Go through to step 2
      await waitFor(() => {
        expect(screen.getByText(/Comment souhaitez-vous participer/i)).toBeInTheDocument();
      });
      
      const elevageSkill = screen.getByRole('button', { name: /elevage/i });
      await user.click(elevageSkill);
      
      const nextButton = screen.getByRole('button', { name: /Suivant/i });
      await user.click(nextButton);
      
      // At step 2, go back
      await waitFor(() => {
        expect(screen.getByText(/Vos disponibilités/i)).toBeInTheDocument();
      });
      
      const backButton = screen.getByRole('button', { name: /Retour/i });
      await user.click(backButton);
      
      // Should be back at step 1
      await waitFor(() => {
        expect(screen.getByText(/Comment souhaitez-vous participer/i)).toBeInTheDocument();
      });
      
      // Previous selections should be preserved
      const elevageSkillAgain = screen.getByRole('button', { name: /elevage/i });
      expect(elevageSkillAgain).toHaveClass('bg-green-500', 'text-white');
    });

    it('should handle activity catalog navigation', async () => {
      render(<App />);
      
      // Start from homepage
      expect(screen.getByRole('heading', { name: /Le cœur.*avant l'argent/i })).toBeInTheDocument();
      
      // Click "Découvrir nos activités"
      const discoverButton = screen.getByRole('button', { name: /Découvrir nos activités/i });
      await user.click(discoverButton);
      
      // Should navigate to catalog
      await waitFor(() => {
        expect(screen.getByText(/Catalogue des activités/i)).toBeInTheDocument();
        expect(screen.getByText(/30 activités pour apprendre/i)).toBeInTheDocument();
      });
      
      // Should show category filters
      expect(screen.getByRole('button', { name: /Toutes \(30\)/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Agriculture \(6\)/i })).toBeInTheDocument();
      
      // Should show activity cards
      const activityCards = screen.getAllByText(/En savoir plus/i);
      expect(activityCards.length).toBeGreaterThan(0);
      
      // Test category filtering
      const agriFilter = screen.getByRole('button', { name: /Agriculture \(6\)/i });
      await user.click(agriFilter);
      
      // Filter should be active
      expect(agriFilter).toHaveClass('bg-green-500', 'text-white');
    });
  });

  describe('User Experience Edge Cases', () => {
    it('should handle incomplete onboarding gracefully', async () => {
      render(<App />);
      
      // Start onboarding but don't select anything
      const proposeButton = screen.getByRole('button', { name: /Proposer mon aide/i });
      await user.click(proposeButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Comment souhaitez-vous participer/i)).toBeInTheDocument();
      });
      
      // Try to proceed without selecting skills
      const nextButton = screen.getByRole('button', { name: /Suivant/i });
      await user.click(nextButton);
      
      // Should still proceed (no validation in current implementation)
      await waitFor(() => {
        expect(screen.getByText(/Vos disponibilités/i)).toBeInTheDocument();
      });
    });

    it('should handle rapid navigation clicks', async () => {
      render(<App />);
      
      // Start onboarding
      const proposeButton = screen.getByRole('button', { name: /Proposer mon aide/i });
      
      // Click multiple times rapidly
      await user.click(proposeButton);
      await user.click(proposeButton);
      await user.click(proposeButton);
      
      // Should only navigate once
      await waitFor(() => {
        expect(screen.getByText(/Comment souhaitez-vous participer/i)).toBeInTheDocument();
      });
    });

    it('should maintain state when navigating between flows', async () => {
      render(<App />);
      
      // Start onboarding
      const proposeButton = screen.getByRole('button', { name: /Proposer mon aide/i });
      await user.click(proposeButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Comment souhaitez-vous participer/i)).toBeInTheDocument();
      });
      
      // Go back to home
      const homeButton = screen.getByText('La Vida Luca'); // Logo button
      await user.click(homeButton);
      
      await waitFor(() => {
        expect(screen.getByRole('heading', { name: /Le cœur.*avant l'argent/i })).toBeInTheDocument();
      });
      
      // Navigate to catalog instead
      const discoverButton = screen.getByRole('button', { name: /Découvrir nos activités/i });
      await user.click(discoverButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Catalogue des activités/i)).toBeInTheDocument();
      });
    });
  });

  describe('Activity Suggestions Flow', () => {
    it('should handle activity suggestion interactions', async () => {
      render(<App />);
      
      // Complete onboarding to get to suggestions
      const proposeButton = screen.getByRole('button', { name: /Proposer mon aide/i });
      await user.click(proposeButton);
      
      // Skip through onboarding quickly
      await waitFor(() => {
        expect(screen.getByText(/Comment souhaitez-vous participer/i)).toBeInTheDocument();
      });
      
      // Select minimal requirements and proceed through all steps
      const elevageSkill = screen.getByRole('button', { name: /elevage/i });
      await user.click(elevageSkill);
      
      let nextButton = screen.getByRole('button', { name: /Suivant/i });
      await user.click(nextButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Vos disponibilités/i)).toBeInTheDocument();
      });
      
      const weekendOption = screen.getByRole('button', { name: /weekend/i });
      await user.click(weekendOption);
      
      nextButton = screen.getByRole('button', { name: /Suivant/i });
      await user.click(nextButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Votre région/i)).toBeInTheDocument();
      });
      
      const locationInput = screen.getByPlaceholderText(/Ex: Ile-de-France/i);
      await user.type(locationInput, 'Test Region');
      
      nextButton = screen.getByRole('button', { name: /Suivant/i });
      await user.click(nextButton);
      
      await waitFor(() => {
        expect(screen.getByText(/Vos préférences/i)).toBeInTheDocument();
      });
      
      const agriPreference = screen.getByRole('button', { name: /Agriculture/i });
      await user.click(agriPreference);
      
      const completeButton = screen.getByRole('button', { name: /Voir mes propositions/i });
      await user.click(completeButton);
      
      // At suggestions page
      await waitFor(() => {
        expect(screen.getByText(/Vos propositions personnalisées/i)).toBeInTheDocument();
      });
      
      // Should be able to interact with suggestions
      const guideButtons = screen.getAllByText(/Voir le guide & m'inscrire/i);
      expect(guideButtons.length).toBeGreaterThan(0);
      
      // Click on first guide button
      await user.click(guideButtons[0]);
      
      // Should show safety guide
      await waitFor(() => {
        expect(screen.getByText(/Guide sécurité/i)).toBeInTheDocument();
        expect(screen.getByText(/Règles de sécurité/i)).toBeInTheDocument();
      });
      
      // Should have inscription button
      const inscriptionButton = screen.getByRole('button', { name: /Je m'inscris/i });
      expect(inscriptionButton).toBeInTheDocument();
    }, 30000);
  });
});