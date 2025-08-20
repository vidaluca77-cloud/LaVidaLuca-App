'use client';

import React, { useEffect } from 'react';
import { motion } from 'framer-motion';
import useGamificationStore from '../../src/store/gamification';
import UserProgressBar from '../../src/components/gamification/UserProgressBar';
import AchievementCard from '../../src/components/gamification/AchievementCard';
import Leaderboard from '../../src/components/gamification/Leaderboard';

export default function DashboardPage() {
  const { 
    userStats, 
    leaderboard, 
    isLoading, 
    error,
    loadUserStats, 
    loadLeaderboard,
    updateUserStats 
  } = useGamificationStore();

  useEffect(() => {
    // Initialize the store with mock data immediately 
    const initializeStore = async () => {
      try {
        await loadUserStats();
        await loadLeaderboard('weekly');
      } catch (error) {
        console.error('Failed to initialize store:', error);
      }
    };
    
    initializeStore();
  }, []);

  const handleTestAction = () => {
    updateUserStats({
      type: 'activity_complete',
      points: 50,
      description: 'Activité test terminée'
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-500"></div>
          <p className="mt-4 text-gray-600">Chargement de votre profil...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center text-red-600">
          <p>Erreur: {error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  if (!userStats) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-600">Aucune donnée utilisateur disponible</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-2xl font-bold text-gray-900">
              🌾 Tableau de Bord - La Vida Luca
            </h1>
            <nav className="flex gap-4">
              <a href="/" className="text-gray-600 hover:text-gray-900">Accueil</a>
              <a href="/activites" className="text-gray-600 hover:text-gray-900">Activités</a>
              <a href="/test-ia" className="text-gray-600 hover:text-gray-900">IA</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Bienvenue, Fermier ! 👋
          </h2>
          <p className="text-gray-600">
            Suivez votre progression et découvrez de nouvelles opportunités d'apprentissage
          </p>
        </motion.div>

        {/* Progress Overview */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="mb-8"
        >
          <UserProgressBar userStats={userStats} />
        </motion.div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {[
            { label: 'Activités Terminées', value: userStats.activitiesCompleted, icon: '✅', color: 'text-green-600' },
            { label: 'Série Actuelle', value: `${userStats.streak.current} jours`, icon: '🔥', color: 'text-orange-600' },
            { label: 'Note Moyenne', value: userStats.averageRating.toFixed(1), icon: '⭐', color: 'text-yellow-600' },
            { label: 'Contributions', value: userStats.contributionsShared, icon: '🤝', color: 'text-blue-600' }
          ].map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + index * 0.1 }}
              className="bg-white rounded-lg shadow-sm border p-6 text-center"
            >
              <div className="text-3xl mb-2">{stat.icon}</div>
              <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </motion.div>
          ))}
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Achievements */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
            >
              <h3 className="text-xl font-bold text-gray-900 mb-4">🏆 Vos Succès</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                {userStats.achievements.map((achievement) => (
                  <AchievementCard
                    key={achievement.id}
                    achievement={achievement}
                    isUnlocked={!!achievement.unlockedAt}
                  />
                ))}
              </div>
              
              {/* Test Action Button */}
              <div className="mt-6">
                <button
                  onClick={handleTestAction}
                  className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors duration-200 font-medium"
                >
                  🎯 Terminer une activité test (+50 pts)
                </button>
              </div>
            </motion.div>
          </div>

          {/* Leaderboard */}
          <div className="lg:col-span-1">
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 }}
            >
              {leaderboard && (
                <Leaderboard 
                  leaderboard={leaderboard}
                  currentUserId="current-user-id"
                  className="sticky top-8"
                />
              )}
            </motion.div>
          </div>
        </div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mt-12 bg-white rounded-lg shadow-sm border p-6"
        >
          <h3 className="text-xl font-bold text-gray-900 mb-4">🚀 Actions Rapides</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <a
              href="/activites"
              className="p-4 border border-gray-200 rounded-lg hover:border-green-300 hover:bg-green-50 transition-all duration-200 text-center group"
            >
              <div className="text-2xl mb-2">📚</div>
              <h4 className="font-medium text-gray-900 group-hover:text-green-700">Découvrir les Activités</h4>
              <p className="text-sm text-gray-600 mt-1">Explorez nos 30+ activités agricoles</p>
            </a>
            
            <a
              href="/test-ia"
              className="p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:bg-blue-50 transition-all duration-200 text-center group"
            >
              <div className="text-2xl mb-2">🤖</div>
              <h4 className="font-medium text-gray-900 group-hover:text-blue-700">Conseils IA</h4>
              <p className="text-sm text-gray-600 mt-1">Obtenez des suggestions personnalisées</p>
            </a>
            
            <a
              href="/proposer-aide"
              className="p-4 border border-gray-200 rounded-lg hover:border-purple-300 hover:bg-purple-50 transition-all duration-200 text-center group"
            >
              <div className="text-2xl mb-2">🤝</div>
              <h4 className="font-medium text-gray-900 group-hover:text-purple-700">Proposer de l'Aide</h4>
              <p className="text-sm text-gray-600 mt-1">Aidez la communauté MFR</p>
            </a>
          </div>
        </motion.div>
      </main>
    </div>
  );
}