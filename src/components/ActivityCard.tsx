/**
 * Activity card component
 */
import React from 'react';
import { ClockIcon, UserGroupIcon } from '@heroicons/react/24/outline';
import { Activity } from '@/types';

interface ActivityCardProps {
  activity: Activity;
  onDetailsClick?: () => void;
  onLearnMoreClick?: () => void;
  className?: string;
}

/**
 * Card component for displaying activity information
 * @param props Component props
 * @returns JSX element
 */
const ActivityCard: React.FC<ActivityCardProps> = ({
  activity,
  onDetailsClick,
  onLearnMoreClick,
  className = '',
}) => {
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
      case 1:
        return 'bg-green-100 text-green-800';
      case 2:
        return 'bg-yellow-100 text-yellow-800';
      case 3:
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSafetyText = (level: number) => {
    switch (level) {
      case 1:
        return 'Facile';
      case 2:
        return 'Attention';
      case 3:
        return 'Expert';
      default:
        return 'Non défini';
    }
  };

  return (
    <div
      className={`bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow ${className}`}
    >
      <div className="mb-4">
        <h3 className="text-lg font-bold text-gray-900 mb-2">
          {activity.title}
        </h3>
        <p className="text-gray-600 text-sm mb-3">{activity.summary}</p>
      </div>

      <div className="flex items-center justify-between text-sm text-gray-600 mb-4">
        <div className="flex items-center">
          <ClockIcon className="w-4 h-4 mr-1" />
          {formatDuration(activity.duration_min)}
        </div>
        <div
          className={`px-2 py-1 rounded-full text-xs font-medium ${getSafetyColor(activity.safety_level)}`}
        >
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

      <button
        onClick={onLearnMoreClick}
        className="w-full bg-green-500 text-white py-2 rounded-lg font-medium hover:bg-green-600 transition-colors"
      >
        En savoir plus
      </button>
    </div>
  );
};

export default ActivityCard;
