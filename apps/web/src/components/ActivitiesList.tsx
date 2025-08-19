'use client'

import React from 'react'
import { useGetActivitiesQuery } from '../lib/api/activitiesApi'

export default function ActivitiesList() {
  const { data: activities, error, isLoading } = useGetActivitiesQuery({
    limit: 10,
    published_only: true
  })

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-8 text-red-600">
        Erreur lors du chargement des activités
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">Activités disponibles</h2>
      
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {activities?.map((activity) => (
          <div key={activity.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-lg font-semibold">{activity.title}</h3>
              <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                {activity.category}
              </span>
            </div>
            
            <p className="text-gray-600 text-sm mb-4">{activity.summary}</p>
            
            <div className="flex justify-between items-center text-sm text-gray-500">
              <span>{activity.duration_min} min</span>
              <span>Niveau {activity.safety_level}/5</span>
            </div>
            
            {activity.skill_tags && activity.skill_tags.length > 0 && (
              <div className="mt-4">
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
          </div>
        ))}
      </div>
      
      {(!activities || activities.length === 0) && (
        <div className="text-center py-8 text-gray-500">
          Aucune activité trouvée
        </div>
      )}
    </div>
  )
}