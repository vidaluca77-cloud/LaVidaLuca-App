import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'La Vida Luca | Réseau de fermes pédagogiques',
  description: 'Formation des jeunes & agriculture vivante - Le cœur avant l\'argent',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body>{children}</body>
    </html>
  )
}
