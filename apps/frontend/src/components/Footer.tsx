import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="border-t">
      <div className="mx-auto max-w-6xl px-4 py-8 text-sm opacity-70">
        © {new Date().getFullYear()} La Vida Luca — Tous droits réservés
      </div>
    </footer>
  );
};

export default Footer;