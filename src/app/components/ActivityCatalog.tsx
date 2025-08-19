'use client';

import React, { useEffect } from 'react';
import { ClockIcon, UserGroupIcon } from '@heroicons/react/24/outline';
import { useActivities } from '../../lib/hooks';
import { LoadingSpinner } from '../../lib/components/ui/Loading';

const ActivityCatalog = () => {
  const { 
    activities, 
    filteredActivities, 
    selectedCategory, 
    isLoading, 
    loadActivities, 
    selectCategory 
  } = useActivities();

  useEffect(() => {
    if (activities.length === 0) {
      loadActivities();
    }
  }, [activities.length, loadActivities]);

  const categories = [
    { id: 'all', name: 'Toutes', count: activities.length },
    { id: 'agri', name: 'Agriculture', count: activities.filter(a => a.category === 'agri').length },
    { id: 'transfo', name: 'Transformation', count: activities.filter(a => a.category === 'transfo').length },
    { id: 'artisanat', name: 'Artisanat', count: activities.filter(a => a.category === 'artisanat').length },
    { id: 'nature', name: 'Environnement', count: activities.filter(a => a.category === 'nature').length },
    { id: 'social', name: 'Animation', count: activities.filter(a => a.category === 'social').length }
  ];

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h${mins > 0 ? mins.toString().padStart(2, '0') : ''}`;
    }
    return `${mins}min`;
  };

  const getSafetyColor = (level: number) => {
    switch (level) {
      case 1: return 'bg-green-100 text-green-800';
      case 2: return 'bg-yellow-100 text-yellow-800';
      case 3: return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSafetyText = (level: number) => {
    switch (level) {
      case 1: return 'Facile';
      case 2: return 'Attention';
      case 3: return 'Expert';
      default: return 'Non défini';
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-6xl mx-auto p-6 flex items-center justify-center min-h-96">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-gray-600">Chargement du catalogue d'activités...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Catalogue des activités
        </h1>
        <p className="text-gray-600">
          {activities.length} activités pour apprendre et découvrir l'agriculture vivante
        </p>
      </div>

      {/* Filtres par catégorie */}
      <div className="flex flex-wrap justify-center gap-3 mb-8">
        {categories.map(category => (
          <button
            key={category.id}
            onClick={() => selectCategory(category.id)}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              selectedCategory === category.id
                ? 'bg-green-500 text-white'
                : 'bg-white text-gray-700 border border-gray-300 hover:border-green-500'
            }`}
          >
            {category.name} ({category.count})
          </button>
        ))}
      </div>

      {/* Grille des activités */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredActivities.map(activity => (
          <div key={activity.id} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
            <div className="mb-4">
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                {activity.title}
              </h3>
              <p className="text-gray-600 text-sm mb-3">
                {activity.summary}
              </p>
            </div>

            <div className="flex items-center justify-between text-sm text-gray-600 mb-4">
              <div className="flex items-center">
                <ClockIcon className="w-4 h-4 mr-1" />
                {formatDuration(activity.duration_min)}
              </div>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${getSafetyColor(activity.safety_level)}`}>
                {getSafetyText(activity.safety_level)}
              </div>
            </div>

            {activity.skill_tags.length > 0 && (
              <div className="mb-4">
                <div className="flex flex-wrap gap-1">
                  {activity.skill_tags.slice(0, 3).map((skill, index) => (
                    <span 
                      key={index}
                      className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs"
                    >
                      {skill}
                    </span>
                  ))}
                  {activity.skill_tags.length > 3 && (
                    <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">
                      +{activity.skill_tags.length - 3}
                    </span>
                  )}
                </div>
              </div>
            )}

            {activity.materials.length > 0 && (
              <div className="mb-4">
                <h4 className="text-xs font-medium text-gray-500 mb-1">Matériel :</h4>
                <p className="text-xs text-gray-600">
                  {activity.materials.join(', ')}
                </p>
              </div>
            )}

            <button className="w-full bg-green-500 text-white py-2 rounded-lg font-medium hover:bg-green-600 transition-colors">
              En savoir plus
            </button>
          </div>
        ))}
      </div>

      {filteredActivities.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">Aucune activité trouvée pour cette catégorie.</p>
        </div>
      )}
    </div>
  );
};

export default ActivityCatalog;