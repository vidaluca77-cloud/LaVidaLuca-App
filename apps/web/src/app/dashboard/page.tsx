'use client'

import React from 'react'
import { useAuth } from '@/contexts/AuthContext'
import { useGamification } from '@/hooks/useGamification'
import { UserLevel } from '@/components/gamification/UserLevel'
import { AchievementGrid, AchievementSummary } from '@/components/gamification/Achievement'
import { BadgeGrid } from '@/components/gamification/Badge'
import { Leaderboard, PersonalRank } from '@/components/gamification/Leaderboard'
import { DashboardCard, QuickActions, RecentActivity } from '@/components/layout/Dashboard'
import { formatPoints } from '@/lib/utils'

export default function DashboardPage() {
  const { user, isAuthenticated, isLoading: authLoading } = useAuth()
  const {
    stats,
    achievements,
    badges,
    leaderboard,
    isLoading: gamificationLoading,
    claimAchievement,
    getCompletedAchievements,
    getEarnedBadges,
    calculateLevelProgress
  } = useGamification()

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Accès restreint
          </h1>
          <p className="text-gray-600 mb-8">
            Vous devez être connecté pour accéder au tableau de bord.
          </p>
          <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
            Se connecter
          </button>
        </div>
      </div>
    )
  }

  const isLoading = gamificationLoading
  const completedAchievements = getCompletedAchievements()
  const earnedBadges = getEarnedBadges()
  const levelProgress = stats ? calculateLevelProgress() : { progress: 0, nextLevelXP: 100 }

  // Mock quick actions
  const quickActions = [
    {
      id: 'new-activity',
      label: 'Nouvelle activité',
      description: 'Créer une nouvelle activité pratique',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
      ),
      onClick: () => alert('Créer une activité')
    },
    {
      id: 'browse-activities',
      label: 'Explorer',
      description: 'Découvrir les activités disponibles',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      ),
      onClick: () => alert('Explorer les activités')
    },
    {
      id: 'ai-guide',
      label: 'Guide IA',
      description: 'Obtenir des conseils personnalisés',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
      ),
      onClick: () => alert('Guide IA')
    },
    {
      id: 'community',
      label: 'Communauté',
      description: 'Rejoindre les discussions',
      icon: (
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      ),
      onClick: () => alert('Communauté')
    }
  ]

  // Mock recent activity
  const recentActivity = [
    {
      id: '1',
      title: 'Succès obtenu: Premier pas',
      description: 'Vous avez complété votre première activité!',
      timestamp: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
      type: 'achievement' as const
    },
    {
      id: '2',
      title: 'Activité terminée: Introduction à l\'agriculture bio',
      description: 'Note: 4.5/5 - Excellent travail!',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
      type: 'activity' as const
    },
    {
      id: '3',
      title: 'Badge gagné: Étudiant assidu',
      description: 'Pour votre participation régulière',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
      type: 'badge' as const
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Tableau de bord
              </h1>
              <p className="text-gray-600">
                Bonjour {user?.full_name || user?.username}! 👋
              </p>
            </div>
            <div className="flex items-center gap-4">
              <button className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                Nouvelle activité
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <div key={i} className="bg-white rounded-lg border p-4 animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-full"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-8">
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <DashboardCard
                title="Points totaux"
                value={formatPoints(stats?.total_points || 0)}
                description="Points gagnés"
                color="yellow"
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                }
              />
              
              <DashboardCard
                title="Niveau"
                value={stats?.level || 1}
                description={`${levelProgress.progress.toFixed(0)}% vers le suivant`}
                color="blue"
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                }
              />
              
              <DashboardCard
                title="Succès"
                value={`${completedAchievements.length}/${achievements.length}`}
                description="Succès débloqués"
                color="green"
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
                  </svg>
                }
              />
              
              <DashboardCard
                title="Badges"
                value={earnedBadges.length}
                description="Badges gagnés"
                color="purple"
                icon={
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                  </svg>
                }
              />
            </div>

            {/* Quick Actions */}
            <QuickActions actions={quickActions} />

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Left Column */}
              <div className="lg:col-span-2 space-y-8">
                {/* User Level */}
                {stats && (
                  <UserLevel
                    level={stats.level}
                    experiencePoints={stats.experience_points}
                    totalPoints={stats.total_points}
                    variant="compact"
                  />
                )}

                {/* Recent Achievements */}
                <div>
                  <h2 className="text-lg font-semibold text-gray-900 mb-4">
                    Succès récents
                  </h2>
                  <AchievementGrid
                    achievements={achievements.slice(0, 6)}
                    onClaim={claimAchievement}
                    filter="completed"
                  />
                </div>

                {/* Badges */}
                <div>
                  <h2 className="text-lg font-semibold text-gray-900 mb-4">
                    Badges gagnés
                  </h2>
                  <div className="bg-white rounded-lg border p-4">
                    <BadgeGrid badges={earnedBadges} maxDisplay={12} />
                  </div>
                </div>
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                {/* Personal Rank */}
                <PersonalRank userStats={stats} />

                {/* Leaderboard */}
                <Leaderboard
                  entries={leaderboard.slice(0, 5)}
                  currentUserId={user?.id}
                  maxEntries={5}
                />

                {/* Achievement Summary */}
                <AchievementSummary achievements={achievements} />

                {/* Recent Activity */}
                <RecentActivity activities={recentActivity} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}