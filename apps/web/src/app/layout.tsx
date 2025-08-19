import type { Metadata } from "next";
import "./globals.css";

// Use system fonts as fallback since Google Fonts may not be accessible
const fontClass = 'font-sans';

export const metadata: Metadata = {
  title: "La Vida Luca",
  description: "Réseau de fermes autonomes & pédagogiques",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${fontClass} antialiased`}>
        {children}
      </body>
    </html>
  );
}
