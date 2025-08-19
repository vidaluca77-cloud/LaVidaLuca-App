'use client';

import "./globals.css";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { AuthProvider } from "../hooks/useAuth";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="fr" suppressHydrationWarning>
      <head>
        <title>La Vida Luca</title>
        <meta name="description" content="Réseau de fermes autonomes & pédagogiques — formation, insertion et agriculture vivante." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#22c55e" />
      </head>
      <body className="min-h-screen bg-white text-neutral-900 antialiased font-sans">
        <AuthProvider>
          <Header />
          <main className="mx-auto max-w-6xl px-4 py-10">{children}</main>
          <Footer />
        </AuthProvider>
      </body>
    </html>
  );
}
