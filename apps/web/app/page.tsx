export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="container py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-earth-500 rounded-lg"></div>
            <span className="text-xl font-display font-semibold text-gradient">La Vida Luca</span>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <a href="/activites" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Activités
            </a>
            <a href="/proposer-aide" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Contribuer
            </a>
            <a href="/test-ia" className="btn btn-primary">
              Assistant IA
            </a>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="container">
        <section className="py-20 text-center">
          <div className="max-w-4xl mx-auto">
            <h1 className="text-gradient mb-6 leading-tight">
              Le cœur avant l'économie
            </h1>
            
            <p className="text-xl text-neutral-600 mb-4 max-w-3xl mx-auto leading-relaxed">
              La Vida Luca — former les jeunes en MFR, développer une agriculture vivante 
              et redonner un avenir au monde rural.
            </p>

            <p className="text-lg text-neutral-500 mb-12 max-w-2xl mx-auto">
              Une plateforme collaborative dédiée à l'innovation pédagogique et au développement 
              de pratiques agricoles respectueuses de l'environnement.
            </p>

            {/* Call to Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16">
              <a href="/activites" className="btn btn-primary text-base px-8 py-3">
                🌱 Explorer les activités
              </a>
              <a href="/proposer-aide" className="btn btn-secondary text-base px-8 py-3">
                🤝 Proposer mon aide
              </a>
              <a href="/test-ia" className="btn btn-success text-base px-8 py-3">
                🤖 Tester l'assistant IA
              </a>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="py-16">
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-green-100 to-green-200 rounded-xl flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl">🎓</span>
              </div>
              <h3 className="text-xl font-display font-semibold mb-4 text-neutral-800">
                Formation MFR
              </h3>
              <p className="text-neutral-600 leading-relaxed">
                Accompagnement pédagogique innovant pour les jeunes en Maisons Familiales Rurales 
                avec des activités pratiques et formatrices.
              </p>
            </div>

            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-earth-100 to-earth-200 rounded-xl flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl">🌾</span>
              </div>
              <h3 className="text-xl font-display font-semibold mb-4 text-neutral-800">
                Agriculture Vivante
              </h3>
              <p className="text-neutral-600 leading-relaxed">
                Développement de pratiques agricoles durables et respectueuses de l'environnement 
                pour un avenir plus vert.
              </p>
            </div>

            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-xl flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl">🤝</span>
              </div>
              <h3 className="text-xl font-display font-semibold mb-4 text-neutral-800">
                Collaboration
              </h3>
              <p className="text-neutral-600 leading-relaxed">
                Une communauté engagée qui partage connaissances, ressources et expériences 
                pour enrichir l'apprentissage.
              </p>
            </div>
          </div>
        </section>

        {/* Stats Section */}
        <section className="py-16">
          <div className="card max-w-4xl mx-auto">
            <div className="grid md:grid-cols-3 gap-8 text-center">
              <div>
                <div className="text-3xl font-display font-bold text-primary-600 mb-2">30+</div>
                <div className="text-neutral-600">Activités disponibles</div>
              </div>
              <div>
                <div className="text-3xl font-display font-bold text-green-600 mb-2">5</div>
                <div className="text-neutral-600">Domaines d'expertise</div>
              </div>
              <div>
                <div className="text-3xl font-display font-bold text-earth-500 mb-2">100%</div>
                <div className="text-neutral-600">Engagement qualité</div>
              </div>
            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="container py-12 mt-20">
        <div className="border-t border-neutral-200 pt-8 text-center">
          <p className="text-neutral-500 text-sm">
            © 2024 La Vida Luca - Plateforme collaborative pour la formation et l'agriculture nouvelle
          </p>
        </div>
      </footer>
    </div>
  );
}