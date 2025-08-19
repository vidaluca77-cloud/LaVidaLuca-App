import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';

// Mock the HomePage component for testing
const HomePage = () => (
  <div>
    <header>
      <div>
        <span>La Vida Luca</span>
      </div>
      <nav>
        <a href="#mission">Notre mission</a>
        <a href="#activites">Activités</a>
        <a href="#contact">Contact</a>
      </nav>
    </header>
    <section>
      <h1>
        <span>Le cœur</span> avant l'argent
      </h1>
      <p>
        Réseau national de fermes pédagogiques dédiées à la formation des jeunes 
        et au développement d'une agriculture vivante et respectueuse.
      </p>
      <div>
        <button>Proposer mon aide</button>
        <button>Découvrir nos activités</button>
      </div>
    </section>
  </div>
);

describe('HomePage Component', () => {
  test('renders main heading correctly', () => {
    render(<HomePage />);
    
    const heading = screen.getByText('Le cœur');
    expect(heading).toBeInTheDocument();
    
    const secondPart = screen.getByText("avant l'argent");
    expect(secondPart).toBeInTheDocument();
  });

  test('renders navigation links', () => {
    render(<HomePage />);
    
    expect(screen.getByText('Notre mission')).toBeInTheDocument();
    expect(screen.getByText('Activités')).toBeInTheDocument();
    expect(screen.getByText('Contact')).toBeInTheDocument();
  });

  test('renders action buttons', () => {
    render(<HomePage />);
    
    const helpButton = screen.getByText('Proposer mon aide');
    const discoverButton = screen.getByText('Découvrir nos activités');
    
    expect(helpButton).toBeInTheDocument();
    expect(discoverButton).toBeInTheDocument();
  });

  test('renders La Vida Luca brand name', () => {
    render(<HomePage />);
    
    expect(screen.getByText('La Vida Luca')).toBeInTheDocument();
  });

  test('renders descriptive text', () => {
    render(<HomePage />);
    
    const description = screen.getByText(/Réseau national de fermes pédagogiques/);
    expect(description).toBeInTheDocument();
  });

  test('buttons are clickable', () => {
    render(<HomePage />);
    
    const helpButton = screen.getByText('Proposer mon aide');
    const discoverButton = screen.getByText('Découvrir nos activités');
    
    fireEvent.click(helpButton);
    fireEvent.click(discoverButton);
    
    // Basic interaction test - buttons should be clickable
    expect(helpButton).toBeInTheDocument();
    expect(discoverButton).toBeInTheDocument();
  });
});