'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { recommendationService } from '../../lib/services';
import { Recommendation } from '../../types';
import { useRouter } from 'next/navigation';
import { 
  StarIcon, 
  ClockIcon, 
  ShieldCheckIcon, 
  UserGroupIcon,
  ArrowPathIcon,
  BookOpenIcon 
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

export default function RecommendationsPage() {
  const { isAuthenticated, isLoading: authLoading, profile } = useAuth();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isRegenerating, setIsRegenerating] = useState(false);
  const router = useRouter();

  // Redirection si non authentifié
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, authLoading, router]);

  // Charger les recommandations
  useEffect(() => {
    if (isAuthenticated) {
      loadRecommendations();
    }
  }, [isAuthenticated]);

  const loadRecommendations = async () => {
    try {
      setIsLoading(true);
      const data = await recommendationService.getRecommendations({ limit: 10 });
      setRecommendations(data.recommendations);
    } catch (error: any) {
      console.error('Erreur lors du chargement des recommandations:', error);
      toast.error('Erreur lors du chargement des recommandations');
    } finally {
      setIsLoading(false);
    }
  };

  const regenerateRecommendations = async () => {
    try {
      setIsRegenerating(true);
      const data = await recommendationService.regenerateRecommendations(10);
      setRecommendations(data.recommendations);
      toast.success('Recommandations mises à jour !');
    } catch (error: any) {
      console.error('Erreur lors de la régénération:', error);
      toast.error('Erreur lors de la mise à jour');
    } finally {
      setIsRegenerating(false);
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'agri':
        return '🌱';
      case 'transfo':
        return '🧀';
      case 'artisanat':
        return '🔨';
      case 'nature':
        return '🌿';
      case 'social':
        return '👥';
      default:
        return '📋';
    }
  };

  const getCategoryName = (category: string) => {
    const names: Record<string, string> = {
      agri: 'Agriculture',
      transfo: 'Transformation',
      artisanat: 'Artisanat',
      nature: 'Environnement',
      social: 'Animation sociale',
    };
    return names[category] || category;
  };

  const getSafetyLevelColor = (level: number) => {
    switch (level) {
      case 1:
        return 'text-green-600 bg-green-100';
      case 2:
        return 'text-yellow-600 bg-yellow-100';
      case 3:
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  const getSafetyLevelText = (level: number) => {
    switch (level) {
      case 1:
        return 'Sécurisé';
      case 2:
        return 'Attention requise';
      case 3:
        return 'Supervision nécessaire';
      default:
        return 'Non défini';
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement de vos recommandations...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirection en cours
  }

  // Si pas de profil, rediriger vers la création de profil
  if (!profile) {
    return (
      <div className="max-w-2xl mx-auto py-12 px-4 text-center">
        <BookOpenIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Créez votre profil pour recevoir des recommandations
        </h1>
        <p className="text-gray-600 mb-6">
          Pour recevoir des recommandations personnalisées, vous devez d'abord compléter votre profil.
        </p>
        <button
          onClick={() => router.push('/profile')}
          className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors"
        >
          Compléter mon profil
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Vos recommandations personnalisées
          </h1>
          <p className="text-gray-600 mt-2">
            Activités sélectionnées spécialement pour votre profil
          </p>
        </div>
        <button
          onClick={regenerateRecommendations}
          disabled={isRegenerating}
          className="flex items-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <ArrowPathIcon className={`h-5 w-5 mr-2 ${isRegenerating ? 'animate-spin' : ''}`} />
          {isRegenerating ? 'Actualisation...' : 'Actualiser'}
        </button>
      </div>

      {recommendations.length === 0 ? (
        <div className="text-center py-12">
          <StarIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Aucune recommandation pour le moment
          </h2>
          <p className="text-gray-600 mb-6">
            Complétez votre profil pour recevoir des recommandations personnalisées.
          </p>
          <button
            onClick={() => router.push('/profile')}
            className="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors"
          >
            Mettre à jour mon profil
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {recommendations.map((recommendation, index) => (
            <div
              key={recommendation.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <div className="flex items-center mb-2">
                      <span className="text-2xl mr-3">
                        {getCategoryIcon(recommendation.activity.category)}
                      </span>
                      <div>
                        <h3 className="text-xl font-bold text-gray-900">
                          {recommendation.activity.title}
                        </h3>
                        <p className="text-sm text-gray-600">
                          {getCategoryName(recommendation.activity.category)}
                        </p>
                      </div>
                    </div>
                    <p className="text-gray-700 mb-4">
                      {recommendation.activity.summary}
                    </p>
                  </div>
                  <div className="ml-4 text-center">
                    <div className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                      {Math.round(recommendation.score)}% compatibilité
                    </div>
                  </div>
                </div>

                {/* Métadonnées de l'activité */}
                <div className="flex flex-wrap gap-4 mb-4 text-sm text-gray-600">
                  <div className="flex items-center">
                    <ClockIcon className="h-4 w-4 mr-1" />
                    {recommendation.activity.duration_min} min
                  </div>
                  <div className="flex items-center">
                    <ShieldCheckIcon className="h-4 w-4 mr-1" />
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${getSafetyLevelColor(
                        recommendation.activity.safety_level
                      )}`}
                    >
                      {getSafetyLevelText(recommendation.activity.safety_level)}
                    </span>
                  </div>
                  {recommendation.activity.skill_tags.length > 0 && (
                    <div className="flex items-center">
                      <UserGroupIcon className="h-4 w-4 mr-1" />
                      Compétences: {recommendation.activity.skill_tags.join(', ')}
                    </div>
                  )}
                </div>

                {/* Raisons de la recommandation */}
                <div className="mb-4">
                  <h4 className="font-medium text-gray-900 mb-2">
                    Pourquoi cette activité vous correspond :
                  </h4>
                  <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                    {recommendation.reasons.map((reason, idx) => (
                      <li key={idx}>{reason}</li>
                    ))}
                  </ul>
                </div>

                {/* Explication IA */}
                {recommendation.ai_explanation && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h4 className="font-medium text-blue-900 mb-2">
                      💡 Conseil personnalisé :
                    </h4>
                    <p className="text-blue-800 text-sm">
                      {recommendation.ai_explanation}
                    </p>
                  </div>
                )}

                {/* Matériel nécessaire */}
                {recommendation.activity.materials.length > 0 && (
                  <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                    <h4 className="font-medium text-gray-900 mb-2">
                      Matériel requis :
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {recommendation.activity.materials.map((material, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-1 bg-white text-gray-700 text-xs rounded border"
                        >
                          {material}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-8 text-center">
        <button
          onClick={() => router.push('/catalogue')}
          className="text-green-600 hover:text-green-700 font-medium"
        >
          Voir toutes les activités disponibles →
        </button>
      </div>
    </div>
  );
}