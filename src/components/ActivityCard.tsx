import React from 'react';
import { Activity } from '@/lib/api';
import { 
  ClockIcon, 
  MapPinIcon, 
  UserGroupIcon, 
  ShieldCheckIcon,
  StarIcon,
  AcademicCapIcon
} from '@heroicons/react/24/outline';

interface ActivityCardProps {
  activity: Activity;
  onSelect?: (activity: Activity) => void;
  showStats?: boolean;
  className?: string;
}

const categoryColors = {
  agri: 'bg-green-100 text-green-800',
  transfo: 'bg-yellow-100 text-yellow-800',
  artisanat: 'bg-blue-100 text-blue-800',
  nature: 'bg-emerald-100 text-emerald-800',
  social: 'bg-purple-100 text-purple-800',
};

const categoryNames = {
  agri: 'Agriculture',
  transfo: 'Transformation',
  artisanat: 'Artisanat',
  nature: 'Environnement',
  social: 'Animation',
};

const safetyLevelLabels = {
  1: 'Sécurisé',
  2: 'Attention requise',
  3: 'Supervision nécessaire',
};

export default function ActivityCard({ 
  activity, 
  onSelect, 
  showStats = false,
  className = '' 
}: ActivityCardProps) {
  const categoryColor = categoryColors[activity.category as keyof typeof categoryColors] || 'bg-gray-100 text-gray-800';
  const categoryName = categoryNames[activity.category as keyof typeof categoryNames] || activity.category;

  return (
    <div 
      className={`bg-white rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer ${className}`}
      onClick={() => onSelect?.(activity)}
    >
      {/* Header with category */}
      <div className="p-4 border-b border-gray-100">
        <div className="flex items-start justify-between">
          <h3 className="font-semibold text-lg text-gray-900 mb-2">
            {activity.title}
          </h3>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${categoryColor}`}>
            {categoryName}
          </span>
        </div>
        
        <p className="text-gray-600 text-sm line-clamp-2">
          {activity.summary}
        </p>
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Metadata */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="flex items-center text-sm text-gray-600">
            <ClockIcon className="h-4 w-4 mr-1" />
            {activity.duration_min} min
          </div>
          
          <div className="flex items-center text-sm text-gray-600">
            <UserGroupIcon className="h-4 w-4 mr-1" />
            Max {activity.max_participants}
          </div>
          
          {activity.location && (
            <div className="flex items-center text-sm text-gray-600">
              <MapPinIcon className="h-4 w-4 mr-1" />
              {activity.location}
            </div>
          )}
          
          <div className="flex items-center text-sm text-gray-600">
            <ShieldCheckIcon className="h-4 w-4 mr-1" />
            {safetyLevelLabels[activity.safety_level as keyof typeof safetyLevelLabels]}
          </div>
        </div>

        {/* Skills */}
        {activity.skill_tags && activity.skill_tags.length > 0 && (
          <div className="mb-4">
            <div className="flex items-center text-sm text-gray-600 mb-2">
              <AcademicCapIcon className="h-4 w-4 mr-1" />
              Compétences
            </div>
            <div className="flex flex-wrap gap-1">
              {activity.skill_tags.slice(0, 3).map((skill) => (
                <span 
                  key={skill}
                  className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                >
                  {skill}
                </span>
              ))}
              {activity.skill_tags.length > 3 && (
                <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                  +{activity.skill_tags.length - 3}
                </span>
              )}
            </div>
          </div>
        )}

        {/* Stats (if enabled) */}
        {showStats && (
          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-gray-100">
            {activity.participant_count !== undefined && (
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">
                  {activity.participant_count}
                </div>
                <div className="text-xs text-gray-600">Participants</div>
              </div>
            )}
            
            {activity.average_rating !== undefined && activity.average_rating > 0 && (
              <div className="text-center">
                <div className="flex items-center justify-center">
                  <StarIcon className="h-4 w-4 text-yellow-400 mr-1" />
                  <span className="text-lg font-semibold text-gray-900">
                    {activity.average_rating.toFixed(1)}
                  </span>
                </div>
                <div className="text-xs text-gray-600">Note moyenne</div>
              </div>
            )}
            
            {activity.completion_rate !== undefined && (
              <div className="text-center">
                <div className="text-lg font-semibold text-gray-900">
                  {activity.completion_rate.toFixed(0)}%
                </div>
                <div className="text-xs text-gray-600">Complétées</div>
              </div>
            )}
          </div>
        )}

        {/* Difficulty indicator */}
        <div className="mt-4 flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-sm text-gray-600 mr-2">Difficulté:</span>
            <div className="flex">
              {[1, 2, 3, 4, 5].map((level) => (
                <div
                  key={level}
                  className={`w-2 h-2 rounded-full mr-1 ${
                    level <= activity.difficulty_level 
                      ? 'bg-vida-green' 
                      : 'bg-gray-200'
                  }`}
                />
              ))}
            </div>
          </div>
          
          {activity.is_featured && (
            <span className="px-2 py-1 bg-vida-warm text-white rounded text-xs font-medium">
              Recommandée
            </span>
          )}
        </div>
      </div>
    </div>
  );
}