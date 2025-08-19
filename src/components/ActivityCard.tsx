import { ClockIcon } from '@heroicons/react/24/outline';
import { Activity } from '@/types';
import { formatDuration, getSafetyColor, getSafetyText } from '@/utils/activityHelpers';

interface ActivityCardProps {
  activity: Activity;
  onLearnMore?: (activity: Activity) => void;
}

export default function ActivityCard({ activity, onLearnMore }: ActivityCardProps) {
  const handleLearnMore = () => {
    if (onLearnMore) {
      onLearnMore(activity);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow">
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

      <button 
        onClick={handleLearnMore}
        className="w-full bg-green-500 text-white py-2 rounded-lg font-medium hover:bg-green-600 transition-colors"
      >
        En savoir plus
      </button>
    </div>
  );
}