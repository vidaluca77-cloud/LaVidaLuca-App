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
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
