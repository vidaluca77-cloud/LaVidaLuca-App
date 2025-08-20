/**
 * Recommendations Page
 * Personalized recommendations based on user progress and gamification
 */

'use client';

import React, { useState } from 'react';
import { useGamification, useActivityTracking } from '@/components/layout/GamificationProvider';
import { 
  LightBulbIcon,
  TrophyIcon,
  StarIcon,
  FireIcon,
  MapIcon,
  ClockIcon,
  CheckCircleIcon,
  ArrowRightIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';
import { PersonalizedRecommendation, RecommendationType } from '@/lib/gamification/types';

const RecommendationsPage: React.FC = () => {
  const { recommendations, userProgress, isLoading, error } = useGamification();
  const { trackRecommendationViewed } = useActivityTracking();
  const [viewedRecommendations, setViewedRecommendations] = useState<Set<string>>(new Set());

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement des recommandations...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">Erreur lors du chargement</p>
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

  const handleRecommendationClick = async (recommendation: PersonalizedRecommendation) => {
    if (!viewedRecommendations.has(recommendation.id)) {
      setViewedRecommendations(prev => new Set(prev).add(recommendation.id));
      await trackRecommendationViewed(recommendation.id);
    }
  };

  // Group recommendations by type
  const groupedRecommendations = recommendations.reduce((acc, rec) => {
    if (!acc[rec.type]) {
      acc[rec.type] = [];
    }
    acc[rec.type].push(rec);
    return acc;
  }, {} as Record<RecommendationType, PersonalizedRecommendation[]>);

  // Get type metadata
  const getTypeMetadata = (type: RecommendationType) => {
    switch (type) {
      case 'next_activity':
        return {
          title: 'Prochaines activités',
          description: 'Activités recommandées pour votre niveau',
          icon: ArrowRightIcon,
          color: 'blue',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
          iconColor: 'text-blue-600'
        };
      case 'skill_development':
        return {
          title: 'Développement de compétences',
          description: 'Améliorez vos compétences existantes',
          icon: StarIcon,
          color: 'purple',
          bgColor: 'bg-purple-50',
          borderColor: 'border-purple-200',
          iconColor: 'text-purple-600'
        };
      case 'achievement_opportunity':
        return {
          title: 'Opportunités de succès',
          description: 'Succès que vous pouvez débloquer bientôt',
          icon: TrophyIcon,
          color: 'yellow',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
          iconColor: 'text-yellow-600'
        };
      case 'streak_maintenance':
        return {
          title: 'Maintien de série',
          description: 'Gardez votre motivation et votre régularité',
          icon: FireIcon,
          color: 'orange',
          bgColor: 'bg-orange-50',
          borderColor: 'border-orange-200',
          iconColor: 'text-orange-600'
        };
      case 'category_exploration':
        return {
          title: 'Exploration de catégories',
          description: 'Découvrez de nouveaux domaines',
          icon: MapIcon,
          color: 'green',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
          iconColor: 'text-green-600'
        };
      default:
        return {
          title: 'Recommandations',
          description: 'Suggestions personnalisées',
          icon: LightBulbIcon,
          color: 'gray',
          bgColor: 'bg-gray-50',
          borderColor: 'border-gray-200',
          iconColor: 'text-gray-600'
        };
    }
  };

  // Priority indicator
  const getPriorityBadge = (priority: number) => {
    if (priority >= 90) {
      return { label: 'Très important', color: 'bg-red-100 text-red-800' };
    } else if (priority >= 80) {
      return { label: 'Important', color: 'bg-orange-100 text-orange-800' };
    } else if (priority >= 70) {
      return { label: 'Recommandé', color: 'bg-yellow-100 text-yellow-800' };
    } else {
      return { label: 'Suggéré', color: 'bg-gray-100 text-gray-800' };
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm border p-6 mb-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 bg-gradient-to-r from-green-400 to-blue-500 rounded-lg flex items-center justify-center">
              <SparklesIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Recommandations personnalisées</h1>
              <p className="text-gray-600">
                Suggestions adaptées à votre profil et vos objectifs
              </p>
            </div>
          </div>

          {userProgress && (
            <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center p-3 bg-blue-50 rounded-lg">
                <p className="text-lg font-bold text-blue-600">{userProgress.level.level}</p>
                <p className="text-xs text-gray-600">Niveau</p>
              </div>
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <p className="text-lg font-bold text-green-600">{userProgress.stats.totalActivities}</p>
                <p className="text-xs text-gray-600">Activités</p>
              </div>
              <div className="text-center p-3 bg-purple-50 rounded-lg">
                <p className="text-lg font-bold text-purple-600">{userProgress.skills.length}</p>
                <p className="text-xs text-gray-600">Compétences</p>
              </div>
              <div className="text-center p-3 bg-orange-50 rounded-lg">
                <p className="text-lg font-bold text-orange-600">{userProgress.currentStreak}</p>
                <p className="text-xs text-gray-600">Série</p>
              </div>
            </div>
          )}
        </div>

        {/* Recommendations */}
        {recommendations.length === 0 ? (
          <div className="bg-white rounded-lg shadow-sm border p-12 text-center">
            <LightBulbIcon className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Aucune recommandation disponible
            </h3>
            <p className="text-gray-600">
              Complétez quelques activités pour recevoir des suggestions personnalisées !
            </p>
          </div>
        ) : (
          <div className="space-y-8">
            {Object.entries(groupedRecommendations).map(([type, recs]) => {
              const metadata = getTypeMetadata(type as RecommendationType);
              const Icon = metadata.icon;

              return (
                <div key={type} className="bg-white rounded-lg shadow-sm border overflow-hidden">
                  {/* Section Header */}
                  <div className={`${metadata.bgColor} ${metadata.borderColor} border-b px-6 py-4`}>
                    <div className="flex items-center gap-3">
                      <Icon className={`w-6 h-6 ${metadata.iconColor}`} />
                      <div>
                        <h2 className="text-lg font-semibold text-gray-900">{metadata.title}</h2>
                        <p className="text-sm text-gray-600">{metadata.description}</p>
                      </div>
                    </div>
                  </div>

                  {/* Recommendations List */}
                  <div className="p-6">
                    <div className="space-y-4">
                      {recs.map((recommendation) => {
                        const priorityBadge = getPriorityBadge(recommendation.priority);
                        const isViewed = viewedRecommendations.has(recommendation.id);

                        return (
                          <div
                            key={recommendation.id}
                            className={`
                              p-4 rounded-lg border-2 cursor-pointer transition-all
                              ${isViewed 
                                ? 'border-gray-200 bg-gray-50' 
                                : 'border-green-200 bg-green-50 hover:border-green-300'
                              }
                            `}
                            onClick={() => handleRecommendationClick(recommendation)}
                          >
                            <div className="flex items-start justify-between gap-4">
                              <div className="flex-1">
                                <div className="flex items-center gap-2 mb-2">
                                  <h3 className="font-medium text-gray-900">
                                    {recommendation.title}
                                  </h3>
                                  <span className={`
                                    inline-flex items-center px-2 py-1 rounded-full text-xs font-medium
                                    ${priorityBadge.color}
                                  `}>
                                    {priorityBadge.label}
                                  </span>
                                  {isViewed && (
                                    <CheckCircleIcon className="w-4 h-4 text-green-500" />
                                  )}
                                </div>
                                
                                <p className="text-gray-700 mb-2">
                                  {recommendation.description}
                                </p>
                                
                                <div className="flex items-center gap-2 text-sm">
                                  <LightBulbIcon className="w-4 h-4 text-blue-500" />
                                  <span className="text-blue-600 font-medium">Pourquoi ?</span>
                                  <span className="text-gray-600">{recommendation.reason}</span>
                                </div>

                                {/* Additional Data */}
                                {recommendation.data && (
                                  <div className="mt-3 flex flex-wrap gap-2">
                                    {recommendation.data.category && (
                                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                                        {recommendation.data.category}
                                      </span>
                                    )}
                                    {recommendation.data.skillId && (
                                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-purple-100 text-purple-800">
                                        {recommendation.data.skillId}
                                      </span>
                                    )}
                                    {recommendation.data.minLevel && (
                                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                                        Niveau {recommendation.data.minLevel}+
                                      </span>
                                    )}
                                  </div>
                                )}
                              </div>

                              <div className="flex items-center gap-2">
                                <div className="text-right">
                                  <p className="text-sm font-medium text-gray-900">
                                    Priorité {recommendation.priority}
                                  </p>
                                  {recommendation.expiresAt && (
                                    <p className="text-xs text-gray-500 flex items-center gap-1">
                                      <ClockIcon className="w-3 h-3" />
                                      Expire le {new Date(recommendation.expiresAt).toLocaleDateString('fr-FR')}
                                    </p>
                                  )}
                                </div>
                                <ArrowRightIcon className="w-5 h-5 text-gray-400" />
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Call to Action */}
        {recommendations.length > 0 && (
          <div className="bg-gradient-to-r from-green-500 to-blue-600 rounded-lg p-6 text-white text-center mt-8">
            <h3 className="text-xl font-bold mb-2">Prêt à passer à l'action ?</h3>
            <p className="mb-4">
              Explorez le catalogue d'activités pour mettre en pratique ces recommandations
            </p>
            <a
              href="/catalogue"
              className="inline-flex items-center gap-2 bg-white text-green-600 px-6 py-3 rounded-lg font-medium hover:bg-gray-100 transition-colors"
            >
              <MapIcon className="w-5 h-5" />
              Voir les activités
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default RecommendationsPage;