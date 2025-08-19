// src/app/layout.tsx
import type { Metadata, Viewport } from "next";
import "./globals.css";
import { AuthProvider } from "@/contexts/AuthContext";
import Navigation from "@/components/Navigation";

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
      <body className="min-h-screen bg-white text-neutral-900 antialiased font-sans">
        <AuthProvider>
          <Navigation />
          <main className="mx-auto max-w-6xl px-4 py-10">{children}</main>
          <footer className="border-t">
            <div className="mx-auto max-w-6xl px-4 py-8 text-sm opacity-70">
              © {new Date().getFullYear()} La Vida Luca — Tous droits réservés
            </div>
          </footer>
        </AuthProvider>
      </body>
    </html>
  );
}
