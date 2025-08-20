/**
 * Achievement Card Component
 * Displays individual achievements with progress and unlock status
 */

import React from 'react';
import { 
  Achievement, 
  UserAchievement, 
  AchievementRarity 
} from '@/lib/gamification/types';
import { 
  LockClosedIcon, 
  CheckCircleIcon,
  StarIcon,
  GiftIcon
} from '@heroicons/react/24/outline';

interface AchievementCardProps {
  achievement: Achievement;
  userAchievement?: UserAchievement;
  progress?: number;
  className?: string;
  onView?: (achievement: Achievement) => void;
}

const AchievementCard: React.FC<AchievementCardProps> = ({
  achievement,
  userAchievement,
  progress = 0,
  className = '',
  onView
}) => {
  const isUnlocked = userAchievement?.isCompleted || false;
  const isSecret = achievement.isSecret && !isUnlocked;

  // Rarity styling
  const getRarityStyles = (rarity: AchievementRarity) => {
    switch (rarity) {
      case 'common':
        return {
          border: 'border-gray-300',
          bg: 'bg-gray-50',
          badge: 'bg-gray-100 text-gray-800',
          glow: ''
        };
      case 'rare':
        return {
          border: 'border-blue-300',
          bg: 'bg-blue-50',
          badge: 'bg-blue-100 text-blue-800',
          glow: 'shadow-blue-100'
        };
      case 'epic':
        return {
          border: 'border-purple-300',
          bg: 'bg-purple-50',
          badge: 'bg-purple-100 text-purple-800',
          glow: 'shadow-purple-100'
        };
      case 'legendary':
        return {
          border: 'border-yellow-300',
          bg: 'bg-yellow-50',
          badge: 'bg-yellow-100 text-yellow-800',
          glow: 'shadow-yellow-100'
        };
    }
  };

  const rarityStyles = getRarityStyles(achievement.rarity);

  // Progress calculation
  const progressPercentage = Math.min(100, Math.max(0, progress * 100));

  // Handle click
  const handleClick = () => {
    if (onView && !isSecret) {
      onView(achievement);
    }
  };

  return (
    <div
      className={`
        relative rounded-lg border-2 p-4 transition-all duration-200 cursor-pointer
        ${rarityStyles.border} ${rarityStyles.bg} ${rarityStyles.glow}
        ${isUnlocked ? 'shadow-lg' : 'opacity-75'}
        ${isSecret ? 'opacity-50' : ''}
        hover:shadow-lg hover:scale-105
        ${className}
      `}
      onClick={handleClick}
    >
      {/* Rarity Badge */}
      <div className="absolute top-2 right-2">
        <span className={`
          inline-flex items-center px-2 py-1 rounded-full text-xs font-medium
          ${rarityStyles.badge}
        `}>
          {achievement.rarity}
        </span>
      </div>

      {/* Achievement Icon and Status */}
      <div className="flex items-start gap-3 mb-3">
        <div className="relative">
          <div className={`
            w-12 h-12 rounded-full flex items-center justify-center text-2xl
            ${isUnlocked ? 'bg-white' : 'bg-gray-200'}
            ${isSecret ? 'blur-sm' : ''}
          `}>
            {isSecret ? '❓' : achievement.icon}
          </div>
          
          {/* Status indicator */}
          {isUnlocked && (
            <div className="absolute -top-1 -right-1 w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
              <CheckCircleIcon className="w-4 h-4 text-white" />
            </div>
          )}
          
          {!isUnlocked && !isSecret && (
            <div className="absolute -top-1 -right-1 w-6 h-6 bg-gray-400 rounded-full flex items-center justify-center">
              <LockClosedIcon className="w-4 h-4 text-white" />
            </div>
          )}
        </div>

        <div className="flex-1 min-w-0">
          <h3 className={`
            font-semibold text-gray-900 mb-1
            ${isSecret ? 'blur-sm' : ''}
          `}>
            {isSecret ? 'Succès secret' : achievement.title}
          </h3>
          
          <p className={`
            text-sm text-gray-600 mb-2
            ${isSecret ? 'blur-sm' : ''}
          `}>
            {isSecret ? 'Continuez à explorer pour le découvrir !' : achievement.description}
          </p>

          {/* Category Tag */}
          <div className="flex items-center gap-2 mb-2">
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
              {achievement.category}
            </span>
            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-700">
              {achievement.type.replace('_', ' ')}
            </span>
          </div>
        </div>
      </div>

      {/* Progress Bar (only for incomplete achievements) */}
      {!isUnlocked && !isSecret && progressPercentage > 0 && (
        <div className="mb-3">
          <div className="flex justify-between items-center mb-1">
            <span className="text-xs text-gray-600">Progression</span>
            <span className="text-xs font-medium text-gray-900">
              {progressPercentage.toFixed(0)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-green-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>
      )}

      {/* Reward Information */}
      {!isSecret && (
        <div className="flex items-center gap-2 text-sm">
          <GiftIcon className="w-4 h-4 text-purple-500" />
          <span className="text-gray-700">
            {achievement.reward.description}
          </span>
          {achievement.reward.type === 'experience' && (
            <div className="flex items-center gap-1">
              <StarIcon className="w-4 h-4 text-yellow-500" />
              <span className="font-medium text-yellow-600">
                +{achievement.reward.value}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Unlock Date (for completed achievements) */}
      {isUnlocked && userAchievement && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <p className="text-xs text-gray-500">
            Débloqué le {new Date(userAchievement.unlockedAt).toLocaleDateString('fr-FR', {
              day: 'numeric',
              month: 'long',
              year: 'numeric'
            })}
          </p>
        </div>
      )}

      {/* Requirements (for incomplete achievements) */}
      {!isUnlocked && !isSecret && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <h4 className="text-xs font-medium text-gray-700 mb-2">Conditions :</h4>
          <ul className="space-y-1">
            {achievement.requirements.map((req, index) => (
              <li key={index} className="text-xs text-gray-600 flex items-start gap-2">
                <span className="text-gray-400">•</span>
                <span>
                  {getRequirementText(req.type, req.target)}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Special Effects for Legendary */}
      {achievement.rarity === 'legendary' && isUnlocked && (
        <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-yellow-200 via-transparent to-yellow-200 opacity-20 pointer-events-none animate-pulse" />
      )}
    </div>
  );
};

// Helper function to format requirement text
const getRequirementText = (type: string, target: string | number): string => {
  switch (type) {
    case 'complete_activities':
      return `Complétez ${target} activité${typeof target === 'number' && target > 1 ? 's' : ''}`;
    case 'category_activities':
      return `Complétez ${target} activité${typeof target === 'number' && target > 1 ? 's' : ''} dans cette catégorie`;
    case 'consecutive_days':
      return `Maintenez une série de ${target} jour${typeof target === 'number' && target > 1 ? 's' : ''}`;
    case 'total_time':
      const hours = typeof target === 'number' ? Math.floor(target / 60) : 0;
      const minutes = typeof target === 'number' ? target % 60 : 0;
      return `Accumulez ${hours}h${minutes > 0 ? `${minutes}m` : ''} d'activité`;
    case 'master_skill':
      return `Maîtrisez la compétence "${target}"`;
    case 'safety_level':
      return `Maintenez un niveau de sécurité élevé`;
    default:
      return 'Condition spéciale';
  }
};

export default AchievementCard;