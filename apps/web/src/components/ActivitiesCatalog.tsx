'use client'

import React, { useState } from 'react'
import { useGetActivitiesQuery } from '../lib/api/activitiesApi'

interface ActivityFilters {
  category?: string
  difficulty?: string
  search?: string
  published_only?: boolean
}

export default function ActivitiesCatalog() {
  const [filters, setFilters] = useState<ActivityFilters>({
    published_only: true
  })
  const [currentPage, setCurrentPage] = useState(1)
  const [selectedActivity, setSelectedActivity] = useState<any>(null)

  const { data: activities, error, isLoading } = useGetActivitiesQuery({
    ...filters,
    skip: (currentPage - 1) * 12,
    limit: 12
  })

  const categories = [
    { value: '', label: 'Toutes les catégories' },
    { value: 'agri', label: 'Agriculture' },
    { value: 'transfo', label: 'Transformation' },
    { value: 'artisanat', label: 'Artisanat' },
    { value: 'nature', label: 'Nature & Environnement' },
    { value: 'social', label: 'Social & Éducation' }
  ]

  const difficulties = [
    { value: '', label: 'Tous les niveaux' },
    { value: 'beginner', label: 'Débutant' },
    { value: 'intermediate', label: 'Intermédiaire' },
    { value: 'advanced', label: 'Avancé' }
  ]

  const getDifficultyColor = (level: string) => {
    switch (level) {
      case 'beginner': return 'bg-green-100 text-green-800'
      case 'intermediate': return 'bg-yellow-100 text-yellow-800'
      case 'advanced': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getSafetyLevelIcon = (level: number) => {
    const icons = ['🟢', '🟡', '🟠', '🔴', '⚫']
    return icons[Math.min(level - 1, 4)] || '🟢'
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center py-12">
            <div className="text-red-600 text-lg">
              Erreur lors du chargement des activités
            </div>
            <button 
              onClick={() => window.location.reload()}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Réessayer
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Catalogue d'Activités</h1>
          <p className="mt-2 text-gray-600">
            Découvrez notre collection d'activités pédagogiques pour la formation en MFR
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Filtres</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Recherche
              </label>
              <input
                type="text"
                placeholder="Rechercher une activité..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={filters.search || ''}
                onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Catégorie
              </label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={filters.category || ''}
                onChange={(e) => setFilters({ ...filters, category: e.target.value || undefined })}
              >
                {categories.map((cat) => (
                  <option key={cat.value} value={cat.value}>
                    {cat.label}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Niveau
              </label>
              <select
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={filters.difficulty || ''}
                onChange={(e) => setFilters({ ...filters, difficulty: e.target.value || undefined })}
              >
                {difficulties.map((diff) => (
                  <option key={diff.value} value={diff.value}>
                    {diff.label}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        )}

        {/* Activities Grid */}
        {activities && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {activities.map((activity) => (
              <div
                key={activity.id}
                className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer"
                onClick={() => setSelectedActivity(activity)}
              >
                <div className="p-6">
                  {/* Header */}
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-lg font-semibold text-gray-900 line-clamp-2">
                      {activity.title}
                    </h3>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(activity.difficulty_level)}`}>
                      {activity.difficulty_level}
                    </span>
                  </div>

                  {/* Category and Duration */}
                  <div className="flex items-center gap-4 mb-4 text-sm text-gray-600">
                    <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">
                      {activity.category}
                    </span>
                    <span>{activity.duration_minutes} min</span>
                    <span title={`Niveau de sécurité: ${activity.safety_level}/5`}>
                      {getSafetyLevelIcon(activity.safety_level)}
                    </span>
                  </div>

                  {/* Description */}
                  <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                    {activity.description || activity.learning_objectives}
                  </p>

                  {/* Skills Tags */}
                  {activity.skill_tags && activity.skill_tags.length > 0 && (
                    <div className="mb-4">
                      <div className="flex flex-wrap gap-1">
                        {activity.skill_tags.slice(0, 3).map((tag, index) => (
                          <span key={index} className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                            {tag}
                          </span>
                        ))}
                        {activity.skill_tags.length > 3 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded">
                            +{activity.skill_tags.length - 3}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Participants */}
                  {(activity.min_participants || activity.max_participants) && (
                    <div className="text-sm text-gray-600">
                      👥 {activity.min_participants || 1}
                      {activity.max_participants && activity.max_participants !== activity.min_participants 
                        ? `-${activity.max_participants}` 
                        : '+'} participants
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {activities && activities.length === 0 && (
          <div className="text-center py-12">
            <div className="text-gray-500 text-lg">
              Aucune activité trouvée avec ces critères
            </div>
            <button
              onClick={() => setFilters({ published_only: true })}
              className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Réinitialiser les filtres
            </button>
          </div>
        )}
      </div>

      {/* Activity Detail Modal */}
      {selectedActivity && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold text-gray-900">{selectedActivity.title}</h2>
                <button
                  onClick={() => setSelectedActivity(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-6">
                {/* Basic Info */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <h3 className="font-semibold text-gray-900">Catégorie</h3>
                    <p className="text-gray-600">{selectedActivity.category}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Durée</h3>
                    <p className="text-gray-600">{selectedActivity.duration_minutes} minutes</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Niveau</h3>
                    <p className="text-gray-600">{selectedActivity.difficulty_level}</p>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900">Sécurité</h3>
                    <p className="text-gray-600">
                      {getSafetyLevelIcon(selectedActivity.safety_level)} 
                      {selectedActivity.safety_level}/5
                    </p>
                  </div>
                </div>

                {/* Description */}
                {selectedActivity.description && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Description</h3>
                    <p className="text-gray-600">{selectedActivity.description}</p>
                  </div>
                )}

                {/* Learning Objectives */}
                {selectedActivity.learning_objectives && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Objectifs pédagogiques</h3>
                    <p className="text-gray-600">{selectedActivity.learning_objectives}</p>
                  </div>
                )}

                {/* Materials */}
                {selectedActivity.materials && selectedActivity.materials.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Matériel nécessaire</h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedActivity.materials.map((material, index) => (
                        <span key={index} className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
                          {material}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Equipment */}
                {selectedActivity.equipment_needed && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Équipement</h3>
                    <p className="text-gray-600">{selectedActivity.equipment_needed}</p>
                  </div>
                )}

                {/* Skills */}
                {selectedActivity.skill_tags && selectedActivity.skill_tags.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Compétences développées</h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedActivity.skill_tags.map((skill, index) => (
                        <span key={index} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Season Tags */}
                {selectedActivity.season_tags && selectedActivity.season_tags.length > 0 && (
                  <div>
                    <h3 className="font-semibold text-gray-900 mb-2">Saisons recommandées</h3>
                    <div className="flex flex-wrap gap-2">
                      {selectedActivity.season_tags.map((season, index) => (
                        <span key={index} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                          {season}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div className="mt-8 flex gap-4">
                <button
                  onClick={() => setSelectedActivity(null)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50"
                >
                  Fermer
                </button>
                <button className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700">
                  Participer
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}