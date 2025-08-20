/**
 * Level Progress Component
 * Displays user level information and progress to next level
 */

import React from 'react';
import { UserLevel } from '@/lib/gamification/types';
import { 
  StarIcon, 
  TrophyIcon,
  SparklesIcon,
  ChevronUpIcon
} from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon } from '@heroicons/react/24/solid';

interface LevelProgressProps {
  userLevel: UserLevel;
  totalXP: number;
  className?: string;
  showBenefits?: boolean;
  compact?: boolean;
}

const LevelProgress: React.FC<LevelProgressProps> = ({
  userLevel,
  totalXP,
  className = '',
  showBenefits = true,
  compact = false
}) => {
  const progressPercentage = (userLevel.currentXP / userLevel.requiredXP) * 100;
  
  // Level milestone indicators
  const getLevelMilestones = () => {
    const milestones = [5, 10, 15, 20];
    return milestones.map(milestone => ({
      level: milestone,
      isPassed: userLevel.level >= milestone,
      isNext: userLevel.level < milestone && userLevel.level >= milestone - 5
    }));
  };

  // Level tier (for styling)
  const getLevelTier = (level: number) => {
    if (level >= 20) return 'legendary';
    if (level >= 15) return 'master';
    if (level >= 10) return 'expert';
    if (level >= 5) return 'intermediate';
    return 'beginner';
  };

  const tier = getLevelTier(userLevel.level);

  // Tier colors
  const getTierColors = (tier: string) => {
    switch (tier) {
      case 'legendary':
        return {
          bg: 'bg-gradient-to-r from-yellow-50 to-orange-50',
          border: 'border-yellow-300',
          text: 'text-yellow-800',
          accent: 'text-yellow-600',
          progress: 'bg-gradient-to-r from-yellow-400 to-orange-500'
        };
      case 'master':
        return {
          bg: 'bg-gradient-to-r from-purple-50 to-pink-50',
          border: 'border-purple-300',
          text: 'text-purple-800',
          accent: 'text-purple-600',
          progress: 'bg-gradient-to-r from-purple-400 to-pink-500'
        };
      case 'expert':
        return {
          bg: 'bg-gradient-to-r from-blue-50 to-indigo-50',
          border: 'border-blue-300',
          text: 'text-blue-800',
          accent: 'text-blue-600',
          progress: 'bg-gradient-to-r from-blue-400 to-indigo-500'
        };
      case 'intermediate':
        return {
          bg: 'bg-gradient-to-r from-green-50 to-emerald-50',
          border: 'border-green-300',
          text: 'text-green-800',
          accent: 'text-green-600',
          progress: 'bg-gradient-to-r from-green-400 to-emerald-500'
        };
      default:
        return {
          bg: 'bg-gradient-to-r from-gray-50 to-slate-50',
          border: 'border-gray-300',
          text: 'text-gray-800',
          accent: 'text-gray-600',
          progress: 'bg-gradient-to-r from-gray-400 to-slate-500'
        };
    }
  };

  const colors = getTierColors(tier);

  if (compact) {
    return (
      <div className={`
        flex items-center gap-3 p-3 rounded-lg border-2 ${colors.bg} ${colors.border} ${className}
      `}>
        <div className="flex items-center gap-2">
          <div className={`
            w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm
            ${colors.progress}
          `}>
            {userLevel.level}
          </div>
          <div>
            <p className={`font-medium text-sm ${colors.text}`}>
              {userLevel.title}
            </p>
            <p className="text-xs text-gray-600">
              {userLevel.currentXP}/{userLevel.requiredXP} XP
            </p>
          </div>
        </div>
        
        <div className="flex-1">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${colors.progress}`}
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`
      p-6 rounded-lg border-2 ${colors.bg} ${colors.border} ${className}
    `}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className={`
            w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg
            ${colors.progress} shadow-lg
          `}>
            {userLevel.level}
          </div>
          <div>
            <h3 className={`text-lg font-bold ${colors.text}`}>
              {userLevel.title}
            </h3>
            <p className={`text-sm ${colors.accent}`}>
              Niveau {userLevel.level}
            </p>
          </div>
        </div>
        
        <div className="text-right">
          <p className="text-sm text-gray-600">XP Total</p>
          <p className={`font-bold text-lg ${colors.accent}`}>
            {totalXP.toLocaleString()}
          </p>
        </div>
      </div>

      {/* Progress to Next Level */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            Progression vers le niveau {userLevel.level + 1}
          </span>
          <span className={`text-sm font-bold ${colors.accent}`}>
            {userLevel.currentXP}/{userLevel.requiredXP} XP
          </span>
        </div>
        
        <div className="relative">
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${colors.progress}`}
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-xs font-medium text-white drop-shadow">
              {progressPercentage.toFixed(0)}%
            </span>
          </div>
        </div>
        
        <p className="text-xs text-gray-600 mt-1">
          Encore {userLevel.requiredXP - userLevel.currentXP} XP pour le niveau suivant
        </p>
      </div>

      {/* Level Milestones */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-2">Jalons</h4>
        <div className="flex gap-2">
          {getLevelMilestones().map((milestone) => (
            <div
              key={milestone.level}
              className={`
                flex items-center justify-center w-8 h-8 rounded-full border-2 text-xs font-bold
                ${milestone.isPassed 
                  ? `${colors.progress} text-white border-transparent` 
                  : milestone.isNext
                    ? `border-yellow-400 text-yellow-600 bg-yellow-50`
                    : 'border-gray-300 text-gray-400 bg-gray-50'
                }
              `}
            >
              {milestone.isPassed ? (
                <StarSolidIcon className="w-4 h-4" />
              ) : (
                milestone.level
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Benefits */}
      {showBenefits && userLevel.benefits.length > 0 && (
        <div>
          <h4 className="text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
            <TrophyIcon className="w-4 h-4" />
            Avantages de votre niveau
          </h4>
          <ul className="space-y-1">
            {userLevel.benefits.map((benefit, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                <SparklesIcon className="w-4 h-4 text-yellow-500 flex-shrink-0 mt-0.5" />
                <span>{benefit}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Next Level Preview */}
      {userLevel.level < 20 && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Prochain niveau :</span>
            <div className="flex items-center gap-2">
              <ChevronUpIcon className="w-4 h-4 text-gray-400" />
              <span className={`font-medium ${colors.accent}`}>
                Niveau {userLevel.level + 1}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Special Effects for High Levels */}
      {tier === 'legendary' && (
        <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-yellow-200 via-transparent to-orange-200 opacity-20 pointer-events-none animate-pulse" />
      )}
    </div>
  );
};

export default LevelProgress;