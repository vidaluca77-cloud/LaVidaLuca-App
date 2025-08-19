'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../context/AuthContext';
import { UserIcon, ArrowRightOnRectangleIcon } from '@heroicons/react/24/outline';

export default function Navigation() {
  const { isAuthenticated, user, logout } = useAuth();

  return (
    <header className="border-b bg-white sticky top-0 z-50">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <Link href="/" className="font-bold text-lg text-green-600">
          La Vida Luca
        </Link>
        
        <nav className="hidden md:flex gap-6 text-sm">
          <Link href="/" className="opacity-80 hover:opacity-100 transition-opacity">
            Accueil
          </Link>
          <Link href="/catalogue" className="opacity-80 hover:opacity-100 transition-opacity">
            Catalogue
          </Link>
          {isAuthenticated && (
            <Link href="/recommendations" className="opacity-80 hover:opacity-100 transition-opacity">
              Mes recommandations
            </Link>
          )}
          <Link href="/rejoindre" className="opacity-80 hover:opacity-100 transition-opacity">
            Rejoindre
          </Link>
          <Link href="/contact" className="opacity-80 hover:opacity-100 transition-opacity">
            Contact
          </Link>
        </nav>

        <div className="flex items-center gap-4">
          {isAuthenticated ? (
            <>
              <Link
                href="/profile"
                className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:text-green-600 transition-colors"
              >
                <UserIcon className="h-4 w-4" />
                {user?.full_name || user?.email?.split('@')[0] || 'Profil'}
              </Link>
              <button
                onClick={logout}
                className="flex items-center gap-2 px-3 py-2 text-sm text-gray-700 hover:text-red-600 transition-colors"
              >
                <ArrowRightOnRectangleIcon className="h-4 w-4" />
                Déconnexion
              </button>
            </>
          ) : (
            <>
              <Link
                href="/auth/login"
                className="px-4 py-2 text-sm text-gray-700 hover:text-green-600 transition-colors"
              >
                Connexion
              </Link>
              <Link
                href="/auth/register"
                className="px-4 py-2 text-sm bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
              >
                S'inscrire
              </Link>
            </>
          )}
        </div>
      </div>

      {/* Mobile menu */}
      <nav className="md:hidden border-t bg-gray-50 px-4 py-2">
        <div className="flex flex-wrap gap-4 text-sm">
          <Link href="/" className="opacity-80 hover:opacity-100">
            Accueil
          </Link>
          <Link href="/catalogue" className="opacity-80 hover:opacity-100">
            Catalogue
          </Link>
          {isAuthenticated && (
            <Link href="/recommendations" className="opacity-80 hover:opacity-100">
              Recommandations
            </Link>
          )}
          <Link href="/rejoindre" className="opacity-80 hover:opacity-100">
            Rejoindre
          </Link>
          <Link href="/contact" className="opacity-80 hover:opacity-100">
            Contact
          </Link>
        </div>
      </nav>
    </header>
  );
}