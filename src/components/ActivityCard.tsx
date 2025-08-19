import React from 'react';
import { Activity } from '@/types';
import { Card, CardContent, Button } from '@/components/ui';
import { ClockIcon, UserGroupIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';
import { cn } from '@/utils/cn';

interface ActivityCardProps {
  activity: Activity;
  onBooking?: (activity: Activity) => void;
  onLearnMore?: (activity: Activity) => void;
  showBookingButton?: boolean;
  className?: string;
}

const categoryColors = {
  agri: 'bg-vida-green-100 text-vida-green-800',
  transfo: 'bg-vida-warm-100 text-vida-warm-800',
  artisanat: 'bg-vida-earth-100 text-vida-earth-800',
  nature: 'bg-vida-sky-100 text-vida-sky-800',
  social: 'bg-purple-100 text-purple-800',
};

const categoryNames = {
  agri: 'Agriculture',
  transfo: 'Transformation', 
  artisanat: 'Artisanat',
  nature: 'Environnement',
  social: 'Animation'
};

const safetyLevelColors = {
  1: 'text-green-600',
  2: 'text-yellow-600',
  3: 'text-red-600',
};

export const ActivityCard: React.FC<ActivityCardProps> = ({
  activity,
  onBooking,
  onLearnMore,
  showBookingButton = true,
  className,
}) => {
  const handleBooking = () => {
    if (onBooking) {
      onBooking(activity);
    }
  };

  const handleLearnMore = () => {
    if (onLearnMore) {
      onLearnMore(activity);
    }
  };

  return (
    <Card className={cn('h-full flex flex-col transition-shadow hover:shadow-vida', className)}>
      <CardContent className="flex-1 flex flex-col">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 text-lg leading-tight mb-2">
              {activity.title}
            </h3>
            <span className={cn(
              'inline-block px-2 py-1 rounded-full text-xs font-medium',
              categoryColors[activity.category]
            )}>
              {categoryNames[activity.category]}
            </span>
          </div>
        </div>

        {/* Summary */}
        <p className="text-gray-600 text-sm mb-4 flex-1">
          {activity.summary}
        </p>

        {/* Activity Details */}
        <div className="space-y-3 mb-4">
          {/* Duration and Safety */}
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center text-gray-500">
              <ClockIcon className="h-4 w-4 mr-1" />
              <span>{activity.duration_min} min</span>
            </div>
            <div className="flex items-center">
              <ShieldCheckIcon className={cn(
                'h-4 w-4 mr-1',
                safetyLevelColors[activity.safety_level as keyof typeof safetyLevelColors]
              )} />
              <span className={cn(
                'text-sm',
                safetyLevelColors[activity.safety_level as keyof typeof safetyLevelColors]
              )}>
                Niveau {activity.safety_level}
              </span>
            </div>
          </div>

          {/* Participants info (if available) */}
          {activity.maxParticipants && (
            <div className="flex items-center text-sm text-gray-500">
              <UserGroupIcon className="h-4 w-4 mr-1" />
              <span>
                {activity.currentParticipants || 0}/{activity.maxParticipants} participants
              </span>
            </div>
          )}

          {/* Skills */}
          {activity.skill_tags.length > 0 && (
            <div>
              <h4 className="text-xs font-medium text-gray-500 mb-1">Compétences :</h4>
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

          {/* Materials */}
          {activity.materials.length > 0 && (
            <div>
              <h4 className="text-xs font-medium text-gray-500 mb-1">Matériel :</h4>
              <p className="text-xs text-gray-600">
                {activity.materials.join(', ')}
              </p>
            </div>
          )}

          {/* Seasonality */}
          {activity.seasonality.length > 0 && !activity.seasonality.includes('toutes') && (
            <div>
              <h4 className="text-xs font-medium text-gray-500 mb-1">Saison :</h4>
              <p className="text-xs text-gray-600 capitalize">
                {activity.seasonality.join(', ')}
              </p>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2 mt-auto">
          <Button
            variant="outline"
            size="sm"
            onClick={handleLearnMore}
            className="flex-1"
          >
            En savoir plus
          </Button>
          {showBookingButton && (
            <Button
              variant="primary"
              size="sm"
              onClick={handleBooking}
              className="flex-1"
              disabled={activity.maxParticipants && 
                       (activity.currentParticipants || 0) >= activity.maxParticipants}
            >
              {activity.maxParticipants && 
               (activity.currentParticipants || 0) >= activity.maxParticipants
                ? 'Complet'
                : 'Réserver'
              }
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
};