import { render, screen } from '@testing-library/react';
import Footer from '../Footer';

describe('Footer Component', () => {
  it('renders the footer content', () => {
    render(<Footer />);
    
    const currentYear = new Date().getFullYear();
    expect(screen.getByText(`© ${currentYear} La Vida Luca — Tous droits réservés`)).toBeInTheDocument();
  });

  it('has correct styling classes', () => {
    const { container } = render(<Footer />);
    const footerElement = container.querySelector('footer');
    
    expect(footerElement).toHaveClass('border-t');
  });
});