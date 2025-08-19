import React from 'react';
import { Activity } from '../utils/types';
import { ClockIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';

interface ActivityCardProps {
  activity: Activity;
  onSelect?: (activity: Activity) => void;
  showSelectButton?: boolean;
}

const ActivityCard: React.FC<ActivityCardProps> = ({ 
  activity, 
  onSelect, 
  showSelectButton = false 
}) => {
  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'agri': return 'bg-vida-green';
      case 'transfo': return 'bg-vida-warm';
      case 'artisanat': return 'bg-vida-earth';
      case 'nature': return 'bg-green-500';
      case 'social': return 'bg-vida-sky';
      default: return 'bg-gray-500';
    }
  };

  const getSafetyColor = (level: number) => {
    if (level <= 2) return 'text-green-600';
    if (level <= 3) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between mb-2">
        <h3 className="font-semibold text-lg">{activity.title}</h3>
        <span className={`px-2 py-1 rounded text-xs text-white ${getCategoryColor(activity.category)}`}>
          {activity.category}
        </span>
      </div>
      
      <p className="text-gray-600 text-sm mb-3">{activity.summary}</p>
      
      <div className="flex items-center gap-4 text-xs text-gray-500 mb-3">
        <div className="flex items-center gap-1">
          <ClockIcon className="w-4 h-4" />
          <span>{activity.duration_min} min</span>
        </div>
        <div className="flex items-center gap-1">
          <ShieldCheckIcon className={`w-4 h-4 ${getSafetyColor(activity.safety_level)}`} />
          <span>Niveau {activity.safety_level}</span>
        </div>
      </div>
      
      {activity.skill_tags.length > 0 && (
        <div className="mb-3">
          <div className="flex flex-wrap gap-1">
            {activity.skill_tags.slice(0, 3).map((skill) => (
              <span key={skill} className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs">
                {skill}
              </span>
            ))}
            {activity.skill_tags.length > 3 && (
              <span className="text-gray-400 text-xs">
                +{activity.skill_tags.length - 3}
              </span>
            )}
          </div>
        </div>
      )}
      
      {activity.materials.length > 0 && (
        <div className="text-xs text-gray-500 mb-3">
          <strong>Matériel :</strong> {activity.materials.join(', ')}
        </div>
      )}
      
      {showSelectButton && onSelect && (
        <button 
          onClick={() => onSelect(activity)}
          className="w-full bg-vida-green text-white py-2 px-4 rounded hover:bg-green-600 transition-colors"
        >
          Sélectionner cette activité
        </button>
      )}
    </div>
  );
};

export default ActivityCard;