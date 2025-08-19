// src/app/layout.tsx
import type { Metadata, Viewport } from "next";
import "./globals.css";
import { DarkModeToggle } from "@/components/DarkModeToggle";

// Use fallback for Inter font to avoid network dependency issues
const inter = { className: "font-sans" };

export const metadata: Metadata = {
  metadataBase: new URL("https://la-vida-luca.vercel.app"),
  title: {
    default: "La Vida Luca",
    template: "%s | La Vida Luca",
  },
  description:
    "Réseau de fermes autonomes & pédagogiques — formation, insertion et agriculture vivante.",
  applicationName: "La Vida Luca",
  manifest: "/manifest.webmanifest",
  openGraph: {
    title: "La Vida Luca",
    description:
      "Réseau de fermes autonomes & pédagogiques — formation, insertion et agriculture vivante.",
    url: "/",
    siteName: "La Vida Luca",
    type: "website",
    locale: "fr_FR",
  },
  icons: {
    icon: [
      { url: "/icons/icon-192.png", sizes: "192x192", type: "image/png" },
      { url: "/icons/icon-512.png", sizes: "512x512", type: "image/png" },
    ],
    apple: "/icons/icon-192.png",
  },
};

export const viewport: Viewport = {
  themeColor: "#10b981",
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <body
        className={`${inter.className} min-h-screen bg-white dark:bg-gray-900 text-neutral-900 dark:text-neutral-100 antialiased transition-colors`}
      >
        <header className="border-b border-gray-200 dark:border-gray-700">
          <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
            <a href="/" className="font-semibold text-lg">La Vida Luca</a>
            <div className="flex items-center gap-6">
              <nav className="flex gap-6 text-sm">
                <a href="/" className="opacity-80 hover:opacity-100 transition-opacity">Accueil</a>
                <a href="/rejoindre" className="opacity-80 hover:opacity-100 transition-opacity">
                  Rejoindre
                </a>
                <a href="/contact" className="opacity-80 hover:opacity-100 transition-opacity">
                  Contact
                </a>
              </nav>
              <DarkModeToggle />
            </div>
          </div>
        </header>

        <main className="mx-auto max-w-6xl px-4 py-10">{children}</main>

        <footer className="border-t border-gray-200 dark:border-gray-700">
          <div className="mx-auto max-w-6xl px-4 py-8 text-sm opacity-70">
            © {new Date().getFullYear()} La Vida Luca — Tous droits réservés
          </div>
        </footer>
      </body>
    </html>
  );
}
