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

describe('Activity Browsing Flow', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('completes full activity browsing flow from home to catalog', async () => {
    const user = userEvent.setup();
    render(<App />);

    // 1. Start from home page
    expect(screen.getByText(/Le cœur/i)).toBeInTheDocument();
    expect(screen.getByText(/avant l'argent/i)).toBeInTheDocument();

    // 2. Click "Découvrir nos activités" button
    const discoverButton = screen.getByText('Découvrir nos activités');
    await user.click(discoverButton);

    // 3. Should navigate to catalog page
    await waitFor(() => {
      expect(screen.getByText('Catalogue des activités')).toBeInTheDocument();
      expect(screen.getByText('30 activités pour apprendre et découvrir l\'agriculture vivante')).toBeInTheDocument();
    });

    // 4. Verify catalog functionality
    expect(screen.getByText('Toutes (30)')).toBeInTheDocument();
    expect(screen.getByText('Agriculture (6)')).toBeInTheDocument();
    expect(screen.getByText('Transformation (6)')).toBeInTheDocument();

    // 5. Filter by Agriculture category
    const agriFilter = screen.getByText('Agriculture (6)');
    await user.click(agriFilter);

    // 6. Verify agriculture activities are shown
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();
    expect(screen.getByText('Tonte & entretien du troupeau')).toBeInTheDocument();

    // 7. Test search functionality
    const searchInput = screen.getByPlaceholderText('Rechercher…');
    await user.type(searchInput, 'moutons');

    // 8. Should show filtered results
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();
    expect(screen.queryByText('Tonte & entretien du troupeau')).not.toBeInTheDocument();

    // 9. Clear search to see all agriculture activities again
    await user.clear(searchInput);
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();
    expect(screen.getByText('Tonte & entretien du troupeau')).toBeInTheDocument();

    // 10. Switch back to all categories
    const allFilter = screen.getByText('Toutes (30)');
    await user.click(allFilter);

    // 11. Should see activities from all categories
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();
    expect(screen.getByText('Fabrication de fromage')).toBeInTheDocument();
    expect(screen.getByText('Construction d\'abris')).toBeInTheDocument();
  });

  it('browses activities by different categories systematically', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Navigate to catalog
    const discoverButton = screen.getByText('Découvrir nos activités');
    await user.click(discoverButton);

    await waitFor(() => {
      expect(screen.getByText('Catalogue des activités')).toBeInTheDocument();
    });

    // Test Agriculture category
    const agriFilter = screen.getByText('Agriculture (6)');
    await user.click(agriFilter);
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();

    // Test Transformation category
    const transfoFilter = screen.getByText('Transformation (6)');
    await user.click(transfoFilter);
    expect(screen.getByText('Fabrication de fromage')).toBeInTheDocument();
    expect(screen.getByText('Confitures & conserves')).toBeInTheDocument();

    // Test Artisanat category
    const artisanatFilter = screen.getByText('Artisanat (6)');
    await user.click(artisanatFilter);
    expect(screen.getByText('Construction d\'abris')).toBeInTheDocument();
    expect(screen.getByText('Réparation & entretien des outils')).toBeInTheDocument();

    // Test Environnement category
    const natureFilter = screen.getByText('Environnement (6)');
    await user.click(natureFilter);
    expect(screen.getByText('Entretien de la rivière')).toBeInTheDocument();
    expect(screen.getByText('Plantation d\'arbres')).toBeInTheDocument();

    // Test Animation category
    const socialFilter = screen.getByText('Animation (6)');
    await user.click(socialFilter);
    expect(screen.getByText('Journée portes ouvertes')).toBeInTheDocument();
    expect(screen.getByText('Visites guidées de la ferme')).toBeInTheDocument();
  });

  it('searches across all activity categories effectively', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Navigate to catalog
    const discoverButton = screen.getByText('Découvrir nos activités');
    await user.click(discoverButton);

    await waitFor(() => {
      expect(screen.getByText('Catalogue des activités')).toBeInTheDocument();
    });

    const searchInput = screen.getByPlaceholderText('Rechercher…');

    // Search for "fromage" - should find transformation activity
    await user.type(searchInput, 'fromage');
    expect(screen.getByText('Fabrication de fromage')).toBeInTheDocument();
    expect(screen.queryByText('Nourrir et soigner les moutons')).not.toBeInTheDocument();

    // Clear and search for "bois" - should find construction activities
    await user.clear(searchInput);
    await user.type(searchInput, 'bois');
    expect(screen.getByText('Construction d\'abris')).toBeInTheDocument();
    expect(screen.getByText('Pain au four à bois')).toBeInTheDocument();

    // Clear and search for "enfants" - should find social activities
    await user.clear(searchInput);
    await user.type(searchInput, 'enfants');
    expect(screen.getByText('Ateliers pour enfants')).toBeInTheDocument();

    // Search with no results
    await user.clear(searchInput);
    await user.type(searchInput, 'inexistant');
    expect(screen.getByText('Aucun résultat.')).toBeInTheDocument();
  });

  it('navigates back to home from catalog', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Navigate to catalog
    const discoverButton = screen.getByText('Découvrir nos activités');
    await user.click(discoverButton);

    await waitFor(() => {
      expect(screen.getByText('Catalogue des activités')).toBeInTheDocument();
    });

    // Click on La Vida Luca logo/title to go back home
    const homeLink = screen.getByText('La Vida Luca');
    await user.click(homeLink);

    await waitFor(() => {
      expect(screen.getByText(/Le cœur/i)).toBeInTheDocument();
      expect(screen.getByText(/avant l'argent/i)).toBeInTheDocument();
    });
  });

  it('maintains state during activity browsing session', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Navigate to catalog
    const discoverButton = screen.getByText('Découvrir nos activités');
    await user.click(discoverButton);

    await waitFor(() => {
      expect(screen.getByText('Catalogue des activités')).toBeInTheDocument();
    });

    // Apply category filter
    const agriFilter = screen.getByText('Agriculture (6)');
    await user.click(agriFilter);
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();

    // Add search on top of filter
    const searchInput = screen.getByPlaceholderText('Rechercher…');
    await user.type(searchInput, 'soigner');
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();
    expect(screen.queryByText('Tonte & entretien du troupeau')).not.toBeInTheDocument();

    // Clear search but keep category filter
    await user.clear(searchInput);
    expect(screen.getByText('Nourrir et soigner les moutons')).toBeInTheDocument();
    expect(screen.getByText('Tonte & entretien du troupeau')).toBeInTheDocument();
    
    // Should still be on Agriculture category
    const categorySelect = screen.getByDisplayValue('Agriculture');
    expect(categorySelect).toBeInTheDocument();
  });
});