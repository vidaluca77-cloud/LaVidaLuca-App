'use client'

import Link from 'next/link'
import { useAuth } from '@/contexts/AuthContext'
import { UserLevel, LevelIcon } from '@/components/gamification/UserLevel'
import { BadgeGrid } from '@/components/gamification/Badge'
import { CompactLeaderboard } from '@/components/gamification/Leaderboard'

export default function Home() {
  const { user, isAuthenticated } = useAuth()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">
                La Vida Luca
              </h1>
              <span className="ml-2 text-sm text-gray-500">
                MFR Platform
              </span>
            </div>
            
            <div className="flex items-center gap-4">
              {isAuthenticated ? (
                <>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-600">
                      Bonjour, {user?.full_name || user?.username}
                    </span>
                    <LevelIcon level={3} size="sm" />
                  </div>
                  <Link
                    href="/dashboard"
                    className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors"
                  >
                    Tableau de bord
                  </Link>
                </>
              ) : (
                <>
                  <button className="text-gray-600 hover:text-gray-900 font-medium">
                    Se connecter
                  </button>
                  <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                    S'inscrire
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 via-blue-700 to-purple-700 text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-7xl mx-auto px-4 py-20">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Apprenez, Partagez, Grandissez
            </h1>
            <p className="text-xl md:text-2xl text-blue-100 mb-8 max-w-3xl mx-auto">
              La plateforme collaborative des Maisons Familiales Rurales pour l'apprentissage 
              pratique et l'échange de connaissances agricoles.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/dashboard"
                className="bg-white text-blue-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors"
              >
                Commencer maintenant
              </Link>
              <button className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-medium py-3 px-8 rounded-lg transition-colors">
                En savoir plus
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Une expérience d'apprentissage gamifiée
            </h2>
            <p className="text-gray-600 max-w-2xl mx-auto">
              Découvrez une nouvelle façon d'apprendre avec un système de points, 
              de badges et de classements qui motivent et récompensent vos progrès.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1: Gamification */}
            <div className="bg-white rounded-xl border p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🏆</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Système de récompenses
              </h3>
              <p className="text-gray-600 mb-4">
                Gagnez des points, débloquez des succès et collectionnez des badges 
                en complétant vos activités d'apprentissage.
              </p>
              <div className="space-y-2">
                <div className="flex items-center justify-center gap-2">
                  <span className="text-sm text-gray-500">Exemple:</span>
                  <LevelIcon level={5} size="sm" showTitle />
                </div>
              </div>
            </div>

            {/* Feature 2: AI Guidance */}
            <div className="bg-white rounded-xl border p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤖</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Conseils IA personnalisés
              </h3>
              <p className="text-gray-600 mb-4">
                Obtenez des suggestions d'activités et des conseils adaptés à votre 
                niveau et à vos intérêts grâce à l'intelligence artificielle.
              </p>
              <div className="bg-gray-50 rounded-lg p-3">
                <p className="text-sm text-gray-600 italic">
                  "Basé sur vos progrès, je recommande l'activité 'Gestion durable des sols'..."
                </p>
              </div>
            </div>

            {/* Feature 3: Community */}
            <div className="bg-white rounded-xl border p-8 text-center hover:shadow-lg transition-shadow">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">👥</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Communauté collaborative
              </h3>
              <p className="text-gray-600 mb-4">
                Partagez vos expériences, apprenez des autres et participez 
                à une communauté dynamique d'apprenants.
              </p>
              <div className="space-y-2">
                <div className="text-sm text-gray-500">Classement communautaire</div>
                <div className="bg-gray-50 rounded-lg p-2">
                  <div className="flex items-center justify-between text-xs">
                    <span>Top 3 cette semaine</span>
                    <span className="text-blue-600">Voir plus</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Demo Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Aperçu de la plateforme
            </h2>
            <p className="text-gray-600">
              Découvrez les fonctionnalités principales de La Vida Luca
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            {/* Demo Content */}
            <div className="space-y-6">
              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="font-semibold text-gray-900 mb-4">
                  Système de progression
                </h3>
                <UserLevel
                  level={4}
                  experiencePoints={750}
                  totalPoints={1250}
                  variant="compact"
                />
              </div>

              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="font-semibold text-gray-900 mb-4">
                  Collection de badges
                </h3>
                <BadgeGrid
                  badges={[
                    {
                      id: 1,
                      name: "Premier pas",
                      description: "Première activité complétée",
                      icon: "",
                      rarity: "common",
                      is_active: true,
                      created_at: new Date().toISOString(),
                      earned_at: new Date().toISOString()
                    },
                    {
                      id: 2,
                      name: "Explorateur",
                      description: "10 activités explorées",
                      icon: "",
                      rarity: "rare",
                      is_active: true,
                      created_at: new Date().toISOString(),
                      earned_at: new Date().toISOString()
                    },
                    {
                      id: 3,
                      name: "Mentor",
                      description: "A aidé 5 autres apprenants",
                      icon: "",
                      rarity: "epic",
                      is_active: true,
                      created_at: new Date().toISOString(),
                      earned_at: new Date().toISOString()
                    }
                  ]}
                  size="md"
                  maxDisplay={3}
                />
              </div>
            </div>

            {/* Demo Stats */}
            <div className="space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-blue-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-blue-600">500+</div>
                  <div className="text-sm text-blue-800">Activités</div>
                </div>
                <div className="bg-green-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-green-600">1,200</div>
                  <div className="text-sm text-green-800">Apprenants</div>
                </div>
                <div className="bg-yellow-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-yellow-600">50+</div>
                  <div className="text-sm text-yellow-800">Badges</div>
                </div>
                <div className="bg-purple-50 rounded-lg p-4 text-center">
                  <div className="text-2xl font-bold text-purple-600">100+</div>
                  <div className="text-sm text-purple-800">Succès</div>
                </div>
              </div>

              <div className="bg-gray-50 rounded-xl p-6">
                <h3 className="font-semibold text-gray-900 mb-4">
                  Classement hebdomadaire
                </h3>
                <CompactLeaderboard
                  entries={[
                    {
                      user_id: 1,
                      username: "marie_agri",
                      full_name: "Marie Dubois",
                      total_points: 2450,
                      level: 6,
                      achievements_count: 15,
                      badges_count: 8,
                      rank: 1
                    },
                    {
                      user_id: 2,
                      username: "pierre_eco",
                      full_name: "Pierre Martin",
                      total_points: 2100,
                      level: 5,
                      achievements_count: 12,
                      badges_count: 6,
                      rank: 2
                    },
                    {
                      user_id: 3,
                      username: "sophie_bio",
                      full_name: "Sophie Bernard",
                      total_points: 1850,
                      level: 5,
                      achievements_count: 11,
                      badges_count: 7,
                      rank: 3
                    }
                  ]}
                  maxEntries={3}
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600 text-white">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">
            Prêt à commencer votre parcours d'apprentissage ?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Rejoignez des milliers d'apprenants qui développent leurs compétences 
            agricoles avec La Vida Luca.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/dashboard"
              className="bg-white text-blue-600 hover:bg-gray-100 font-medium py-3 px-8 rounded-lg transition-colors"
            >
              Commencer maintenant
            </Link>
            <button className="border-2 border-white text-white hover:bg-white hover:text-blue-600 font-medium py-3 px-8 rounded-lg transition-colors">
              Demander une démo
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="font-bold text-lg mb-4">La Vida Luca</h3>
              <p className="text-gray-400">
                Plateforme collaborative pour l'apprentissage agricole et rural.
              </p>
            </div>
            
            <div>
              <h4 className="font-medium mb-4">Fonctionnalités</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Activités interactives</li>
                <li>Système de gamification</li>
                <li>Conseils IA</li>
                <li>Communauté</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Centre d'aide</li>
                <li>Documentation</li>
                <li>Contact</li>
                <li>FAQ</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium mb-4">Légal</h4>
              <ul className="space-y-2 text-gray-400">
                <li>Conditions d'utilisation</li>
                <li>Politique de confidentialité</li>
                <li>Mentions légales</li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 La Vida Luca. Tous droits réservés.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
