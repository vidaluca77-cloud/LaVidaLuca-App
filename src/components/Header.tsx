'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import AuthModal from './auth/AuthModal';

export default function Header() {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');

  const isActive = (path: string) => {
    return pathname === path ? 'opacity-100 font-medium' : 'opacity-80 hover:opacity-100';
  };

  const handleAuthClick = (mode: 'login' | 'register') => {
    setAuthMode(mode);
    setShowAuthModal(true);
  };

  return (
    <>
      <header className="border-b">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <Link href="/" className="font-semibold text-lg">
            La Vida Luca
          </Link>
          
          <nav className="flex items-center gap-6 text-sm">
            <Link href="/" className={isActive('/')}>
              Accueil
            </Link>
            <Link href="/catalogue" className={isActive('/catalogue')}>
              Catalogue
            </Link>
            <Link href="/rejoindre" className={isActive('/rejoindre')}>
              Rejoindre
            </Link>
            <Link href="/contact" className={isActive('/contact')}>
              Contact
            </Link>
            
            <div className="border-l pl-6">
              {user ? (
                <div className="flex items-center gap-3">
                  <span className="text-gray-600">Bonjour, {user.name}</span>
                  <button
                    onClick={logout}
                    className="text-gray-500 hover:text-gray-700"
                  >
                    Déconnexion
                  </button>
                </div>
              ) : (
                <div className="flex items-center gap-3">
                  <button
                    onClick={() => handleAuthClick('login')}
                    className="text-gray-600 hover:text-gray-900"
                  >
                    Connexion
                  </button>
                  <button
                    onClick={() => handleAuthClick('register')}
                    className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
                  >
                    S'inscrire
                  </button>
                </div>
              )}
            </div>
          </nav>
        </div>
      </header>
      
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        initialMode={authMode}
      />
    </>
  );
}