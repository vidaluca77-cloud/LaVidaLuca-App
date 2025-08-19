import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Catalogue from '../catalogue/page';

describe('Catalogue Page', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders catalogue page with title and description', () => {
    render(<Catalogue />);
    
    expect(screen.getByText('Catalogue')).toBeInTheDocument();
    expect(screen.getByText('Sélectionne une catégorie ou cherche un mot-clé.')).toBeInTheDocument();
  });

  it('renders search input and category dropdown', () => {
    render(<Catalogue />);
    
    expect(screen.getByPlaceholderText('Rechercher…')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Toutes')).toBeInTheDocument();
  });

  it('displays default items on initial load', () => {
    render(<Catalogue />);
    
    // Check if some default items are displayed
    expect(screen.getByText('Agneau broutard (vivant)')).toBeInTheDocument();
    expect(screen.getByText('Journée découverte ferme')).toBeInTheDocument();
    expect(screen.getByText('Plants & arbres (saison)')).toBeInTheDocument();
  });

  it('filters items by search query', async () => {
    const user = userEvent.setup();
    render(<Catalogue />);
    
    const searchInput = screen.getByPlaceholderText('Rechercher…');
    await user.type(searchInput, 'agneau');
    
    // Should show items containing "agneau"
    expect(screen.getByText('Agneau broutard (vivant)')).toBeInTheDocument();
    
    // Should not show items not containing "agneau"
    expect(screen.queryByText('Journée découverte ferme')).not.toBeInTheDocument();
  });

  it('filters items by category', async () => {
    const user = userEvent.setup();
    render(<Catalogue />);
    
    const categorySelect = screen.getByDisplayValue('Toutes');
    await user.selectOptions(categorySelect, 'Produits vivants');
    
    // Should show only "Produits vivants" items
    expect(screen.getByText('Agneau broutard (vivant)')).toBeInTheDocument();
    expect(screen.getByText('Plants & arbres (saison)')).toBeInTheDocument();
    
    // Should not show items from other categories
    expect(screen.queryByText('Journée découverte ferme')).not.toBeInTheDocument();
  });

  it('shows contact link for each item', () => {
    render(<Catalogue />);
    
    const contactLinks = screen.getAllByText('Contacter');
    expect(contactLinks.length).toBeGreaterThan(0);
    
    // Check if contact links have correct href
    contactLinks.forEach(link => {
      expect(link.closest('a')).toHaveAttribute('href', '/contact');
    });
  });

  it('displays item details correctly', () => {
    render(<Catalogue />);
    
    // Check first item details - use getAllByText for multiple matches
    expect(screen.getByText('Agneau broutard (vivant)')).toBeInTheDocument();
    expect(screen.getByText('Réservation locale, qualité élevée.')).toBeInTheDocument();
    expect(screen.getByText('299 € TTC')).toBeInTheDocument();
    expect(screen.getAllByText('Calvados (14)')[0]).toBeInTheDocument();
    expect(screen.getByText('local')).toBeInTheDocument();
    expect(screen.getByText('réservation')).toBeInTheDocument();
  });

  it('shows "no results" message when no items match search', async () => {
    const user = userEvent.setup();
    render(<Catalogue />);
    
    const searchInput = screen.getByPlaceholderText('Rechercher…');
    await user.type(searchInput, 'inexistant');
    
    expect(screen.getByText('Aucun résultat.')).toBeInTheDocument();
  });

  it('combines search and category filters correctly', async () => {
    const user = userEvent.setup();
    render(<Catalogue />);
    
    // First select category
    const categorySelect = screen.getByDisplayValue('Toutes');
    await user.selectOptions(categorySelect, 'Services');
    
    // Then search within that category
    const searchInput = screen.getByPlaceholderText('Rechercher…');
    await user.type(searchInput, 'pédagogique');
    
    // Should show only services containing "pédagogique"
    expect(screen.getByText('Visite pédagogique MFR/lycées')).toBeInTheDocument();
    
    // Should not show other items
    expect(screen.queryByText('Agneau broutard (vivant)')).not.toBeInTheDocument();
  });

  it('handles category filtering for all categories', async () => {
    const user = userEvent.setup();
    render(<Catalogue />);
    
    const categorySelect = screen.getByDisplayValue('Toutes');
    
    // Test each category
    await user.selectOptions(categorySelect, 'Activités terrain');
    expect(screen.getByText('Journée découverte ferme')).toBeInTheDocument();
    
    await user.selectOptions(categorySelect, 'Dons en nature');
    expect(screen.getAllByText('Dons en nature')[0]).toBeInTheDocument(); // Title appears twice
    
    await user.selectOptions(categorySelect, 'Toutes');
    expect(screen.getByText('Agneau broutard (vivant)')).toBeInTheDocument();
    expect(screen.getByText('Journée découverte ferme')).toBeInTheDocument();
  });

  it('renders image placeholders for all items', () => {
    render(<Catalogue />);
    
    const imagePlaceholders = screen.getAllByText('Image');
    expect(imagePlaceholders.length).toBeGreaterThan(0);
  });

  it('displays tags for each item', () => {
    render(<Catalogue />);
    
    // Check if tags are displayed
    expect(screen.getByText('local')).toBeInTheDocument();
    expect(screen.getByText('réservation')).toBeInTheDocument();
    expect(screen.getByText('groupes')).toBeInTheDocument();
    expect(screen.getByText('éducation')).toBeInTheDocument();
  });
});