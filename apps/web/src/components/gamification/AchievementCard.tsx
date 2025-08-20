import React from 'react';
import { motion } from 'framer-motion';
import { Achievement } from '../../types/gamification';

interface AchievementCardProps {
  achievement: Achievement;
  isUnlocked?: boolean;
  onClick?: () => void;
}

const rarityColors = {
  common: '#6B7280',
  uncommon: '#84CC16', 
  rare: '#3B82F6',
  epic: '#8B5CF6',
  legendary: '#F59E0B'
};

const rarityGradients = {
  common: 'from-gray-400 to-gray-600',
  uncommon: 'from-green-400 to-green-600',
  rare: 'from-blue-400 to-blue-600', 
  epic: 'from-purple-400 to-purple-600',
  legendary: 'from-yellow-400 to-yellow-600'
};

export default function AchievementCard({ achievement, isUnlocked = false, onClick }: AchievementCardProps) {
  const progressPercentage = achievement.maxProgress && achievement.progress 
    ? (achievement.progress / achievement.maxProgress) * 100 
    : 0;

  return (
    <motion.div
      className={`
        relative overflow-hidden rounded-xl border-2 p-4 cursor-pointer transition-all duration-300
        ${isUnlocked 
          ? `border-${achievement.rarity} shadow-lg bg-gradient-to-br ${rarityGradients[achievement.rarity]} text-white` 
          : 'border-gray-300 bg-gray-100 text-gray-500 opacity-60'
        }
      `}
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.98 }}
      onClick={onClick}
      style={isUnlocked ? { borderColor: rarityColors[achievement.rarity] } : {}}
    >
      {/* Rarity indicator */}
      <div className={`absolute top-2 right-2 px-2 py-1 rounded-full text-xs font-medium ${
        isUnlocked ? 'bg-white/20' : 'bg-gray-300'
      }`}>
        {achievement.rarity}
      </div>

      {/* Icon and basic info */}
      <div className="flex items-start gap-3 mb-3">
        <span className={`text-4xl ${isUnlocked ? 'filter-none' : 'grayscale'}`}>
          {achievement.icon}
        </span>
        <div className="flex-1">
          <h3 className={`font-bold text-lg leading-tight ${isUnlocked ? 'text-white' : 'text-gray-700'}`}>
            {achievement.name}
          </h3>
          <p className={`text-sm mt-1 ${isUnlocked ? 'text-white/90' : 'text-gray-600'}`}>
            {achievement.description}
          </p>
        </div>
      </div>

      {/* Progress bar (if applicable) */}
      {achievement.maxProgress && (
        <div className="mb-3">
          <div className="flex justify-between text-xs mb-1">
            <span>Progression</span>
            <span>{achievement.progress || 0}/{achievement.maxProgress}</span>
          </div>
          <div className={`h-2 rounded-full overflow-hidden ${isUnlocked ? 'bg-white/20' : 'bg-gray-300'}`}>
            <motion.div
              className={`h-full ${isUnlocked ? 'bg-white' : 'bg-gray-400'}`}
              initial={{ width: 0 }}
              animate={{ width: `${progressPercentage}%` }}
              transition={{ duration: 0.8, ease: "easeOut" }}
            />
          </div>
        </div>
      )}

      {/* Points and category */}
      <div className="flex justify-between items-center">
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${
          isUnlocked ? 'bg-white/20' : 'bg-gray-300'
        }`}>
          {achievement.category}
        </span>
        <span className={`font-bold ${isUnlocked ? 'text-white' : 'text-gray-600'}`}>
          +{achievement.points} pts
        </span>
      </div>

      {/* Unlock date */}
      {isUnlocked && achievement.unlockedAt && (
        <div className="mt-2 text-xs text-white/80">
          Débloqué le {achievement.unlockedAt.toLocaleDateString('fr-FR')}
        </div>
      )}

      {/* Shimmer effect for unlocked achievements */}
      {isUnlocked && (
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent"
          initial={{ x: '-100%' }}
          animate={{ x: '100%' }}
          transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
        />
      )}
    </motion.div>
  );
}