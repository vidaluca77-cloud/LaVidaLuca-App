// src/components/Header.tsx
import React from "react";

interface HeaderProps {
  onHomeClick?: () => void;
  onOnboardingClick?: () => void;
  onCatalogClick?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  onHomeClick,
  onOnboardingClick,
  onCatalogClick,
}) => {
  return (
    <header className="bg-white/90 backdrop-blur-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <button
            onClick={onHomeClick}
            className="flex items-center space-x-2 text-green-500 hover:text-green-600"
          >
            <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">VL</span>
            </div>
            <span className="font-bold text-xl text-gray-900">
              La Vida Luca
            </span>
          </button>

          <nav className="hidden md:flex space-x-8">
            <a
              href="#mission"
              className="text-gray-700 hover:text-green-500 font-medium"
            >
              Notre mission
            </a>
            <button
              onClick={onCatalogClick}
              className="text-gray-700 hover:text-green-500 font-medium"
            >
              Activités
            </button>
            <a
              href="#contact"
              className="text-gray-700 hover:text-green-500 font-medium"
            >
              Contact
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
};
