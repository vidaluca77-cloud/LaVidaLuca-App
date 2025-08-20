import React from 'react';
import { motion } from 'framer-motion';
import { UserStats } from '../../types/gamification';

interface UserProgressBarProps {
  userStats: UserStats;
  showLevel?: boolean;
  className?: string;
}

export default function UserProgressBar({ userStats, showLevel = true, className = '' }: UserProgressBarProps) {
  const progressPercentage = userStats.nextLevel 
    ? ((userStats.totalPoints - userStats.currentLevel.minPoints) / 
       (userStats.nextLevel.minPoints - userStats.currentLevel.minPoints)) * 100
    : 100;

  return (
    <div className={`bg-white rounded-lg shadow-sm border p-4 ${className}`}>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{userStats.currentLevel.icon}</span>
          {showLevel && (
            <div>
              <h3 className="font-semibold text-gray-900">{userStats.currentLevel.name}</h3>
              <p className="text-sm text-gray-600">Niveau {userStats.currentLevel.level}</p>
            </div>
          )}
        </div>
        <div className="text-right">
          <p className="font-bold text-lg" style={{ color: userStats.currentLevel.color }}>
            {userStats.totalPoints.toLocaleString()} pts
          </p>
          {userStats.nextLevel && (
            <p className="text-sm text-gray-600">
              {userStats.pointsToNextLevel} pts pour le niveau suivant
            </p>
          )}
        </div>
      </div>
      
      {userStats.nextLevel && (
        <div className="relative">
          <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
            <motion.div
              className="h-full rounded-full"
              style={{ backgroundColor: userStats.currentLevel.color }}
              initial={{ width: 0 }}
              animate={{ width: `${progressPercentage}%` }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
          </div>
          <div className="flex justify-between mt-1 text-xs text-gray-600">
            <span>{userStats.currentLevel.name}</span>
            <span>{userStats.nextLevel.name}</span>
          </div>
        </div>
      )}
    </div>
  );
}