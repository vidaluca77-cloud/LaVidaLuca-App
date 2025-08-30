import '../src/app/globals.css'

export const metadata = {
  title: 'La Vida Luca - Formation en MFR et Agriculture Nouvelle',
  description: 'Plateforme collaborative dédiée à la formation des jeunes en Maisons Familiales Rurales et au développement de nouvelles pratiques agricoles.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
      </head>
      <body className="gradient-bg min-h-screen">
        {children}
      </body>
    </html>
  )
}
