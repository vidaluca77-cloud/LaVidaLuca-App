// src/app/layout.tsx
import type { Metadata, Viewport } from "next";
// import { Inter } from "next/font/google";
import "./globals.css";

// const inter = Inter({ subsets: ["latin"] });

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
      <body className={`min-h-screen bg-white text-neutral-900 antialiased`}>
        <header className="border-b">
          <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
            <a href="/" className="font-semibold">
              La Vida Luca
            </a>
            <nav className="flex gap-6 text-sm">
              <a href="/" className="opacity-80 hover:opacity-100">
                Accueil
              </a>
              <a href="/rejoindre" className="opacity-80 hover:opacity-100">
                Rejoindre
              </a>
              <a href="/contact" className="opacity-80 hover:opacity-100">
                Contact
              </a>
            </nav>
          </div>
        </header>

        <main className="mx-auto max-w-6xl px-4 py-10">{children}</main>

        <footer className="border-t">
          <div className="mx-auto max-w-6xl px-4 py-8 text-sm opacity-70">
            © {new Date().getFullYear()} La Vida Luca — Tous droits réservés
          </div>
        </footer>
      </body>
    </html>
  );
}
