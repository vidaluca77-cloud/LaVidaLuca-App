import { ReactNode } from 'react';

interface HeaderProps {
  onNavigate?: {
    home: () => void;
    onboarding: () => void;
    catalog: () => void;
  };
  simple?: boolean;
}

/**
 * Application Header component
 */
export const Header = ({ onNavigate, simple = false }: HeaderProps) => {
  if (simple) {
    return (
      <div className='text-center mb-8'>
        <button
          onClick={onNavigate?.home}
          className='inline-flex items-center space-x-2 text-green-500 hover:text-green-600 mb-4'
        >
          <div className='w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center'>
            <span className='text-white font-bold text-sm'>VL</span>
          </div>
          <span className='font-bold text-xl'>La Vida Luca</span>
        </button>
      </div>
    );
  }

  return (
    <header className='bg-white/90 backdrop-blur-sm border-b border-gray-100'>
      <div className='max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'>
        <div className='flex justify-between items-center h-16'>
          <button
            onClick={onNavigate?.home}
            className='flex items-center space-x-2 hover:opacity-80 transition-opacity'
          >
            <div className='w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center'>
              <span className='text-white font-bold text-sm'>VL</span>
            </div>
            <span className='font-bold text-xl text-gray-900'>
              La Vida Luca
            </span>
          </button>

          <nav className='hidden md:flex space-x-8'>
            <a
              href='#mission'
              className='text-gray-700 hover:text-green-500 font-medium'
            >
              Notre mission
            </a>
            <button
              onClick={onNavigate?.catalog}
              className='text-gray-700 hover:text-green-500 font-medium'
            >
              Activités
            </button>
            <a
              href='#contact'
              className='text-gray-700 hover:text-green-500 font-medium'
            >
              Contact
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
};

interface FooterProps {
  simple?: boolean;
}

/**
 * Application Footer component
 */
export const Footer = ({ simple = false }: FooterProps) => {
  if (simple) {
    return null;
  }

  return (
    <footer className='border-t'>
      <div className='mx-auto max-w-6xl px-4 py-8 text-sm opacity-70'>
        © {new Date().getFullYear()} La Vida Luca — Tous droits réservés
      </div>
    </footer>
  );
};

interface PageLayoutProps {
  children: ReactNode;
  header?: HeaderProps;
  footer?: FooterProps;
}

/**
 * Main Page Layout component
 */
export const PageLayout = ({
  children,
  header = {},
  footer = {},
}: PageLayoutProps) => {
  return (
    <div className='min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50'>
      <Header {...header} />
      <main className='mx-auto max-w-6xl px-4 py-10'>{children}</main>
      <Footer {...footer} />
    </div>
  );
};
