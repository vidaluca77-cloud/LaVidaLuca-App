'use client';

import React from 'react';
import { ClockIcon, ShieldCheckIcon, TagIcon } from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle, Badge, Button } from '@/components/ui';
import { Activity } from '@/types';
import { cn } from '@/lib/utils';

interface ActivityCardProps {
  activity: Activity;
  onBook?: (activity: Activity) => void;
  onViewDetails?: (activity: Activity) => void;
  showBookButton?: boolean;
  className?: string;
}

const categoryColors = {
  agri: 'bg-vida-100 text-vida-800',
  transfo: 'bg-vida-warm-100 text-vida-warm-800',
  artisanat: 'bg-vida-earth-100 text-vida-earth-800',
  nature: 'bg-vida-sky-100 text-vida-sky-800',
  social: 'bg-purple-100 text-purple-800'
};

const categoryNames = {
  agri: 'Agriculture',
  transfo: 'Transformation',
  artisanat: 'Artisanat',
  nature: 'Nature',
  social: 'Social'
};

const safetyLevels = {
  1: { color: 'bg-green-100 text-green-800', text: 'Facile' },
  2: { color: 'bg-yellow-100 text-yellow-800', text: 'Attention' },
  3: { color: 'bg-red-100 text-red-800', text: 'Expert' }
};

export function ActivityCard({ 
  activity, 
  onBook, 
  onViewDetails, 
  showBookButton = true, 
  className 
}: ActivityCardProps) {
  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return mins > 0 ? `${hours}h${mins}min` : `${hours}h`;
    }
    return `${mins}min`;
  };

  const safetyLevel = safetyLevels[activity.safety_level as keyof typeof safetyLevels] || safetyLevels[1];

  return (
    <Card className={cn('h-full flex flex-col transition-shadow hover:shadow-md', className)}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between mb-2">
          <Badge className={categoryColors[activity.category]}>
            {categoryNames[activity.category]}
          </Badge>
          <Badge variant="outline" className={safetyLevel.color}>
            <ShieldCheckIcon className="w-3 h-3 mr-1" />
            {safetyLevel.text}
          </Badge>
        </div>
        <CardTitle className="text-lg leading-tight">
          {activity.title}
        </CardTitle>
      </CardHeader>

      <CardContent className="flex flex-col flex-1">
        <p className="text-gray-600 text-sm mb-4 flex-1">
          {activity.summary}
        </p>

        {/* Duration */}
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <ClockIcon className="w-4 h-4 mr-1" />
          <span>{formatDuration(activity.duration_min)}</span>
        </div>

        {/* Skills */}
        {activity.skill_tags.length > 0 && (
          <div className="mb-4">
            <div className="flex items-center text-xs text-gray-500 mb-1">
              <TagIcon className="w-3 h-3 mr-1" />
              <span>Compétences :</span>
            </div>
            <div className="flex flex-wrap gap-1">
              {activity.skill_tags.slice(0, 3).map((skill, index) => (
                <Badge key={index} variant="outline" size="sm">
                  {skill}
                </Badge>
              ))}
              {activity.skill_tags.length > 3 && (
                <Badge variant="outline" size="sm">
                  +{activity.skill_tags.length - 3}
                </Badge>
              )}
            </div>
          </div>
        )}

        {/* Materials */}
        {activity.materials.length > 0 && (
          <div className="mb-4">
            <h4 className="text-xs font-medium text-gray-500 mb-1">Matériel :</h4>
            <p className="text-xs text-gray-600">
              {activity.materials.join(', ')}
            </p>
          </div>
        )}

        {/* Seasonality */}
        {activity.seasonality.length > 0 && !activity.seasonality.includes('toutes') && (
          <div className="mb-4">
            <h4 className="text-xs font-medium text-gray-500 mb-1">Saison :</h4>
            <div className="flex flex-wrap gap-1">
              {activity.seasonality.map((season, index) => (
                <Badge key={index} variant="outline" size="sm">
                  {season}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Action buttons */}
        <div className="flex gap-2 mt-auto pt-4">
          {onViewDetails && (
            <Button
              variant="outline"
              size="sm"
              className="flex-1"
              onClick={() => onViewDetails(activity)}
            >
              Détails
            </Button>
          )}
          {showBookButton && onBook && (
            <Button
              variant="primary"
              size="sm"
              className="flex-1"
              onClick={() => onBook(activity)}
            >
              Réserver
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}