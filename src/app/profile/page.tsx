/**
 * Profile Page
 * User profile with gamification features, achievements, level progress, and skills
 */

'use client';

import React, { useState } from 'react';
import { useGamification, useUserStats, useAchievementHelpers } from '@/components/layout/GamificationProvider';
import LevelProgress from '@/components/gamification/LevelProgress';
import SkillsOverview from '@/components/gamification/SkillsOverview';
import AchievementCard from '@/components/gamification/AchievementCard';
import { 
  UserIcon,
  TrophyIcon,
  StarIcon,
  FireIcon,
  ClockIcon,
  ChartBarIcon,
  AcademicCapIcon,
  CalendarIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { Achievement } from '@/lib/gamification/types';

const ProfilePage: React.FC = () => {
  const { userProgress, isLoading, error, getAchievementProgress } = useGamification();
  const stats = useUserStats();
  const achievements = useAchievementHelpers();
  const [activeTab, setActiveTab] = useState<'overview' | 'achievements' | 'skills' | 'stats'>('overview');

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du profil...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">Erreur lors du chargement du profil</p>
          <button 
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  if (!userProgress) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <UserIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">Aucun profil trouvé</p>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Vue d\'ensemble', icon: UserIcon },
    { id: 'achievements', label: 'Succès', icon: TrophyIcon },
    { id: 'skills', label: 'Compétences', icon: AcademicCapIcon },
    { id: 'stats', label: 'Statistiques', icon: ChartBarIcon }
  ] as const;

  const unlockedAchievements = achievements.getUnlockedAchievements();
  const nearCompletionAchievements = achievements.getNearCompletionAchievements();

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-gradient-to-r from-green-400 to-blue-500 rounded-full flex items-center justify-center text-white font-bold text-xl">
                {userProgress.level.level}
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Mon Profil</h1>
                <p className="text-lg text-green-600 font-medium">{userProgress.level.title}</p>
                <p className="text-sm text-gray-600">
                  Membre depuis {new Date().toLocaleDateString('fr-FR', { month: 'long', year: 'numeric' })}
                </p>
              </div>
            </div>
            
            {/* Quick Stats */}
            <div className="hidden md:grid grid-cols-3 gap-6 text-center">
              <div>
                <p className="text-2xl font-bold text-green-600">{stats.getCompletedActivitiesCount()}</p>
                <p className="text-sm text-gray-600">Activités</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-purple-600">{stats.getAchievementsCount()}</p>
                <p className="text-sm text-gray-600">Succès</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-blue-600">{stats.getCurrentStreak()}</p>
                <p className="text-sm text-gray-600">Série actuelle</p>
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-sm border mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8 px-6">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`
                      flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm
                      ${activeTab === tab.id
                        ? 'border-green-500 text-green-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                      }
                    `}
                  >
                    <Icon className="w-5 h-5" />
                    {tab.label}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="space-y-8">
          {activeTab === 'overview' && (
            <>
              {/* Level Progress */}
              <LevelProgress 
                userLevel={userProgress.level}
                totalXP={userProgress.totalXP}
                className="bg-white rounded-lg shadow-sm border"
              />

              {/* Recent Achievements */}
              {unlockedAchievements.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    <TrophyIcon className="w-5 h-5 text-yellow-500" />
                    Derniers succès débloqués
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {unlockedAchievements.slice(0, 6).map((achievement) => (
                      <AchievementCard
                        key={achievement.id}
                        achievement={achievement}
                        userAchievement={userProgress.achievements.find(a => a.achievementId === achievement.id)}
                        className="h-full"
                      />
                    ))}
                  </div>
                  {unlockedAchievements.length > 6 && (
                    <div className="mt-4 text-center">
                      <button 
                        onClick={() => setActiveTab('achievements')}
                        className="text-green-600 hover:text-green-700 font-medium"
                      >
                        Voir tous les succès ({unlockedAchievements.length})
                      </button>
                    </div>
                  )}
                </div>
              )}

              {/* Skills Preview */}
              <SkillsOverview 
                skills={userProgress.skills}
                maxSkillsDisplay={4}
                className="bg-white rounded-lg shadow-sm border p-6"
              />

              {/* Achievements Progress */}
              {nearCompletionAchievements.length > 0 && (
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                    <StarIcon className="w-5 h-5 text-yellow-500" />
                    Succès à portée
                  </h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {nearCompletionAchievements.slice(0, 4).map((achievement) => (
                      <AchievementCard
                        key={achievement.id}
                        achievement={achievement}
                        progress={getAchievementProgress(achievement.id)}
                        className="h-full"
                      />
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {activeTab === 'achievements' && (
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-semibold text-gray-900">Tous mes succès</h2>
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <span className="flex items-center gap-1">
                    <CheckCircleIcon className="w-4 h-4 text-green-500" />
                    {unlockedAchievements.length} débloqués
                  </span>
                  <span>{achievements.getLockedAchievements().length} à débloquer</span>
                </div>
              </div>

              {/* Achievement Categories */}
              <div className="mb-6">
                <h3 className="font-medium text-gray-900 mb-3">Succès débloqués</h3>
                {unlockedAchievements.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {unlockedAchievements.map((achievement) => (
                      <AchievementCard
                        key={achievement.id}
                        achievement={achievement}
                        userAchievement={userProgress.achievements.find(a => a.achievementId === achievement.id)}
                      />
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">
                    Aucun succès débloqué pour l'instant
                  </p>
                )}
              </div>

              <div>
                <h3 className="font-medium text-gray-900 mb-3">Prochains objectifs</h3>
                {nearCompletionAchievements.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {nearCompletionAchievements.map((achievement) => (
                      <AchievementCard
                        key={achievement.id}
                        achievement={achievement}
                        progress={getAchievementProgress(achievement.id)}
                      />
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">
                    Continuez vos activités pour débloquer de nouveaux succès !
                  </p>
                )}
              </div>
            </div>
          )}

          {activeTab === 'skills' && (
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <SkillsOverview 
                skills={userProgress.skills}
                showDetails={true}
              />
            </div>
          )}

          {activeTab === 'stats' && (
            <div className="space-y-6">
              {/* General Stats */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Statistiques générales</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                  <div className="text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-lg mx-auto mb-2">
                      <CheckCircleIcon className="w-6 h-6 text-green-600" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{stats.getCompletedActivitiesCount()}</p>
                    <p className="text-sm text-gray-600">Activités terminées</p>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg mx-auto mb-2">
                      <ClockIcon className="w-6 h-6 text-blue-600" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{stats.getTimeSpentFormatted()}</p>
                    <p className="text-sm text-gray-600">Temps total</p>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-orange-100 rounded-lg mx-auto mb-2">
                      <FireIcon className="w-6 h-6 text-orange-600" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{stats.getCurrentStreak()}</p>
                    <p className="text-sm text-gray-600">Série actuelle</p>
                  </div>
                  <div className="text-center">
                    <div className="flex items-center justify-center w-12 h-12 bg-purple-100 rounded-lg mx-auto mb-2">
                      <TrophyIcon className="w-6 h-6 text-purple-600" />
                    </div>
                    <p className="text-2xl font-bold text-gray-900">{stats.getAchievementsCount()}</p>
                    <p className="text-sm text-gray-600">Succès débloqués</p>
                  </div>
                </div>
              </div>

              {/* Category Breakdown */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Activités par catégorie</h2>
                <div className="space-y-4">
                  {Object.entries(stats.getActivitiesByCategory()).map(([category, count]) => {
                    const categoryNames = {
                      agriculture: 'Agriculture',
                      transformation: 'Transformation',
                      artisanat: 'Artisanat',
                      environnement: 'Environnement',
                      social: 'Animation sociale'
                    };
                    
                    const total = stats.getCompletedActivitiesCount();
                    const percentage = total > 0 ? (count / total) * 100 : 0;
                    
                    return (
                      <div key={category}>
                        <div className="flex items-center justify-between mb-1">
                          <span className="text-sm font-medium text-gray-700">
                            {categoryNames[category as keyof typeof categoryNames] || category}
                          </span>
                          <span className="text-sm text-gray-600">{count} activité{count !== 1 ? 's' : ''}</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-green-500 h-2 rounded-full transition-all duration-300"
                            style={{ width: `${percentage}%` }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
                {Object.keys(stats.getActivitiesByCategory()).length === 0 && (
                  <p className="text-gray-500 text-center py-4">
                    Aucune activité terminée pour l'instant
                  </p>
                )}
              </div>

              {/* Streaks */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-6">Historique des séries</h2>
                <div className="grid grid-cols-2 gap-6">
                  <div className="text-center p-4 bg-orange-50 rounded-lg">
                    <FireIcon className="w-8 h-8 text-orange-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-orange-600">{stats.getCurrentStreak()}</p>
                    <p className="text-sm text-gray-600">Série actuelle</p>
                  </div>
                  <div className="text-center p-4 bg-red-50 rounded-lg">
                    <TrophyIcon className="w-8 h-8 text-red-500 mx-auto mb-2" />
                    <p className="text-2xl font-bold text-red-600">{stats.getMaxStreak()}</p>
                    <p className="text-sm text-gray-600">Record personnel</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;