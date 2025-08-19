'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../hooks/useAuth';

const Header: React.FC = () => {
  const { user, logout } = useAuth();

  return (
    <header className="border-b">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <Link href="/" className="font-semibold text-lg">
          La Vida Luca
        </Link>
        
        <nav className="flex gap-6 text-sm items-center">
          <Link href="/" className="opacity-80 hover:opacity-100">
            Accueil
          </Link>
          
          {user ? (
            <>
              <Link href="/catalogue" className="opacity-80 hover:opacity-100">
                Catalogue
              </Link>
              <Link href="/profil" className="opacity-80 hover:opacity-100">
                Mon Profil
              </Link>
              <span className="text-xs opacity-60">
                {user.full_name}
              </span>
              <button 
                onClick={logout}
                className="opacity-80 hover:opacity-100 text-red-600"
              >
                Déconnexion
              </button>
            </>
          ) : (
            <>
              <Link href="/rejoindre" className="opacity-80 hover:opacity-100">
                Rejoindre
              </Link>
              <Link href="/connexion" className="opacity-80 hover:opacity-100">
                Connexion
              </Link>
            </>
          )}
          
          <Link href="/contact" className="opacity-80 hover:opacity-100">
            Contact
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;