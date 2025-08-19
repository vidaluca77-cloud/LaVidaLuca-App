/**
 * Header component for La Vida Luca App
 */
import React from 'react';

interface HeaderProps {
  className?: string;
}

/**
 * Application header with navigation
 * @param props Component props
 * @returns JSX element
 */
const Header: React.FC<HeaderProps> = ({ className = '' }) => {
  return (
    <header
      className={`bg-white/90 backdrop-blur-sm border-b border-gray-100 ${className}`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">VL</span>
            </div>
            <span className="font-bold text-xl text-gray-900">
              La Vida Luca
            </span>
          </div>

          <nav className="hidden md:flex space-x-8">
            <a
              href="#mission"
              className="text-gray-700 hover:text-green-500 font-medium"
            >
              Notre mission
            </a>
            <a
              href="#activites"
              className="text-gray-700 hover:text-green-500 font-medium"
            >
              Activités
            </a>
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

export default Header;
