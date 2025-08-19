import React from 'react';
import { Recommendation } from '@/lib/api';
import ActivityCard from './ActivityCard';
import { SparklesIcon, LightBulbIcon } from '@heroicons/react/24/outline';

interface RecommendationCardProps {
  recommendation: Recommendation;
  onSelect?: (activity: any) => void;
  className?: string;
}

export default function RecommendationCard({ 
  recommendation, 
  onSelect,
  className = '' 
}: RecommendationCardProps) {
  const { activity, score, reasons, confidence } = recommendation;

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  const getConfidenceLevel = (confidence?: number) => {
    if (!confidence) return '';
    if (confidence >= 0.8) return 'Très recommandé';
    if (confidence >= 0.6) return 'Recommandé';
    return 'Suggestion';
  };

  return (
    <div className={`relative ${className}`}>
      {/* Recommendation Badge */}
      <div className="absolute -top-2 -right-2 z-10">
        <div className={`px-3 py-1 rounded-full text-xs font-medium flex items-center ${getScoreColor(score)}`}>
          <SparklesIcon className="h-3 w-3 mr-1" />
          {score.toFixed(0)}% match
        </div>
      </div>

      {/* Activity Card */}
      <ActivityCard 
        activity={activity}
        onSelect={onSelect}
        showStats={true}
        className="border-vida-green/20 hover:border-vida-green/40"
      />

      {/* Recommendation Details */}
      <div className="mt-3 p-3 bg-gradient-to-r from-vida-green/5 to-vida-sky/5 rounded-lg border border-vida-green/10">
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center">
            <LightBulbIcon className="h-4 w-4 text-vida-green mr-1" />
            <span className="text-sm font-medium text-gray-900">
              Pourquoi cette activité ?
            </span>
          </div>
          
          {confidence && (
            <span className="text-xs text-vida-green font-medium">
              {getConfidenceLevel(confidence)}
            </span>
          )}
        </div>

        <ul className="space-y-1">
          {reasons.slice(0, 3).map((reason, index) => (
            <li key={index} className="text-sm text-gray-700 flex items-start">
              <span className="text-vida-green mr-2">•</span>
              {reason}
            </li>
          ))}
          {reasons.length > 3 && (
            <li className="text-sm text-gray-500 italic">
              +{reasons.length - 3} autres raisons...
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}