'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { Activity } from '../../types';
import { activityService } from '../../lib/services';
import {
  ClockIcon,
  ShieldCheckIcon,
  UserGroupIcon,
  MagnifyingGlassIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

export default function CataloguePage() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('Toutes');

  const categoryLabels: Record<string, string> = {
    'Toutes': 'Toutes',
    'agri': 'Agriculture',
    'transfo': 'Transformation',
    'artisanat': 'Artisanat',
    'nature': 'Environnement',
    'social': 'Animation sociale',
  };

  // Charger les données
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        const [activitiesData, categoriesData] = await Promise.all([
          activityService.getActivities(),
          activityService.getCategories(),
        ]);
        setActivities(activitiesData);
        setCategories(['Toutes', ...categoriesData]);
      } catch (error: any) {
        console.error('Erreur lors du chargement:', error);
        toast.error('Erreur lors du chargement des activités');
      } finally {
        setIsLoading(false);
      }
    };

    loadData();
  }, []);

  // Filtrer les activités
  const filteredActivities = useMemo(() => {
    return activities.filter((activity) => {
      const matchesCategory = selectedCategory === 'Toutes' || activity.category === selectedCategory;
      const matchesSearch = searchQuery === '' || 
        activity.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        activity.summary?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        activity.skill_tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
      
      return matchesCategory && matchesSearch;
    });
  }, [activities, selectedCategory, searchQuery]);

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

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement des activités...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Catalogue des Activités</h1>
        <p className="opacity-80">
          Découvrez toutes les activités proposées dans le cadre du projet La Vida Luca
        </p>
      </header>

      {/* Filtres */}
      <div className="space-y-4">
        {/* Barre de recherche */}
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Rechercher une activité..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
          />
        </div>

        {/* Filtres par catégorie */}
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                selectedCategory === category
                  ? 'bg-green-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {categoryLabels[category] || category}
            </button>
          ))}
        </div>
      </div>

      {/* Résultats */}
      <div className="flex justify-between items-center">
        <p className="text-gray-600">
          {filteredActivities.length} activité{filteredActivities.length > 1 ? 's' : ''} trouvée{filteredActivities.length > 1 ? 's' : ''}
        </p>
      </div>

      {/* Liste des activités */}
      {filteredActivities.length === 0 ? (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🔍</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Aucune activité trouvée
          </h2>
          <p className="text-gray-600">
            Essayez de modifier vos critères de recherche ou votre sélection de catégorie.
          </p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredActivities.map((activity) => (
            <div
              key={activity.id}
              className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center">
                  <span className="text-2xl mr-3">
                    {getCategoryIcon(activity.category)}
                  </span>
                  <div>
                    <h3 className="font-bold text-gray-900 text-lg">
                      {activity.title}
                    </h3>
                    <p className="text-sm text-gray-600">
                      {categoryLabels[activity.category] || activity.category}
                    </p>
                  </div>
                </div>
              </div>

              <p className="text-gray-700 mb-4 text-sm">
                {activity.summary}
              </p>

              {/* Métadonnées */}
              <div className="space-y-2 mb-4">
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center text-gray-600">
                    <ClockIcon className="h-4 w-4 mr-1" />
                    {activity.duration_min} min
                  </div>
                  <div className="flex items-center">
                    <ShieldCheckIcon className="h-4 w-4 mr-1" />
                    <span
                      className={`px-2 py-1 rounded-full text-xs ${getSafetyLevelColor(
                        activity.safety_level
                      )}`}
                    >
                      {getSafetyLevelText(activity.safety_level)}
                    </span>
                  </div>
                </div>

                {activity.skill_tags.length > 0 && (
                  <div className="flex items-start text-sm text-gray-600">
                    <UserGroupIcon className="h-4 w-4 mr-1 mt-0.5 flex-shrink-0" />
                    <span className="line-clamp-2">
                      {activity.skill_tags.join(', ')}
                    </span>
                  </div>
                )}
              </div>

              {/* Matériel requis */}
              {activity.materials.length > 0 && (
                <div className="mb-4">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">
                    Matériel requis :
                  </h4>
                  <div className="flex flex-wrap gap-1">
                    {activity.materials.slice(0, 3).map((material, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded"
                      >
                        {material}
                      </span>
                    ))}
                    {activity.materials.length > 3 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-500 text-xs rounded">
                        +{activity.materials.length - 3}
                      </span>
                    )}
                  </div>
                </div>
              )}

              {/* Saisonnalité */}
              {activity.seasonality.length > 0 && (
                <div className="text-xs text-gray-500">
                  Saisonnier: {activity.seasonality.join(', ')}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="text-center">
        <a
          href="/auth/register"
          className="inline-block bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors"
        >
          Créer un compte pour des recommandations personnalisées
        </a>
      </div>
    </div>
  );
}
