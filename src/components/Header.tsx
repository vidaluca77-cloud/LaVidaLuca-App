'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();

  const isActive = (path: string) => {
    return pathname === path ? 'opacity-100 font-medium' : 'opacity-80 hover:opacity-100';
  };

  return (
    <header className="border-b">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
        <Link href="/" className="font-semibold text-lg">
          La Vida Luca
        </Link>
        <nav className="flex gap-6 text-sm">
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
        </nav>
      </div>
    </header>
  );
}