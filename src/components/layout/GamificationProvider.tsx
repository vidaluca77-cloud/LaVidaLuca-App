/**
 * Gamification Provider
 * Context provider for gamification state and functionality
 */

import React, { createContext, useContext, ReactNode } from 'react';
import { useAchievements } from '@/hooks/useAchievements';
import {
  Achievement,
  UserProgress,
  GamificationEvent,
  GamificationNotification,
  PersonalizedRecommendation
} from '@/lib/gamification/types';

interface GamificationContextType {
  // State
  userProgress: UserProgress | null;
  achievements: Achievement[];
  notifications: GamificationNotification[];
  recommendations: PersonalizedRecommendation[];
  isLoading: boolean;
  error: string | null;

  // Actions
  trackEvent: (event: Omit<GamificationEvent, 'timestamp'>) => Promise<void>;
  unlockAchievement: (achievementId: string) => void;
  markNotificationAsRead: (notificationId: string) => void;
  markAllNotificationsAsRead: () => void;
  updateUserProgress: (updates: Partial<UserProgress>) => void;
  refreshRecommendations: () => void;

  // Utilities
  getUnreadNotificationsCount: () => number;
  getAchievementProgress: (achievementId: string) => number;
  canUnlockAchievement: (achievementId: string) => boolean;
  getUserLevel: () => number;
  getTotalXP: () => number;
}

const GamificationContext = createContext<GamificationContextType | undefined>(undefined);

interface GamificationProviderProps {
  children: ReactNode;
  userId?: string;
}

export const GamificationProvider: React.FC<GamificationProviderProps> = ({
  children,
  userId = 'default'
}) => {
  const gamificationState = useAchievements(userId);

  return (
    <GamificationContext.Provider value={gamificationState}>
      {children}
    </GamificationContext.Provider>
  );
};

// Hook to use gamification context
export const useGamification = (): GamificationContextType => {
  const context = useContext(GamificationContext);
  if (context === undefined) {
    throw new Error('useGamification must be used within a GamificationProvider');
  }
  return context;
};

// Hook for tracking activity completion (most common event)
export const useActivityTracking = () => {
  const { trackEvent } = useGamification();

  const trackActivityCompletion = async (
    activityId: string,
    categoryId: string,
    skillIds: string[] = [],
    duration: number = 60,
    safetyLevel: number = 1
  ) => {
    await trackEvent({
      type: 'activity_completed',
      userId: 'default', // Will be replaced with actual user ID in real app
      data: {
        activityId,
        categoryId,
        duration,
        safetyLevel
      }
    });

    // Track skill practice for each skill
    for (const skillId of skillIds) {
      await trackEvent({
        type: 'skill_practiced',
        userId: 'default',
        data: {
          skillId,
          activityId,
          duration: duration / skillIds.length // Distribute time across skills
        }
      });
    }
  };

  const trackActivityStarted = async (
    activityId: string,
    categoryId: string
  ) => {
    await trackEvent({
      type: 'activity_started',
      userId: 'default',
      data: {
        activityId,
        categoryId
      }
    });
  };

  const trackProfileUpdate = async () => {
    await trackEvent({
      type: 'profile_updated',
      userId: 'default',
      data: {}
    });
  };

  const trackRecommendationViewed = async (recommendationId: string) => {
    await trackEvent({
      type: 'recommendation_viewed',
      userId: 'default',
      data: {
        recommendationId
      }
    });
  };

  const trackAchievementViewed = async (achievementId: string) => {
    await trackEvent({
      type: 'achievement_viewed',
      userId: 'default',
      data: {
        achievementId
      }
    });
  };

  return {
    trackActivityCompletion,
    trackActivityStarted,
    trackProfileUpdate,
    trackRecommendationViewed,
    trackAchievementViewed
  };
};

// Hook for quick access to user stats
export const useUserStats = () => {
  const { userProgress } = useGamification();

  const getCompletedActivitiesCount = () => {
    return userProgress?.stats.totalActivities || 0;
  };

  const getTotalTimeSpent = () => {
    return userProgress?.stats.totalTimeSpent || 0;
  };

  const getCurrentStreak = () => {
    return userProgress?.currentStreak || 0;
  };

  const getMaxStreak = () => {
    return userProgress?.maxStreak || 0;
  };

  const getFavoriteCategory = () => {
    return userProgress?.stats.favoriteCategory || null;
  };

  const getActivitiesByCategory = () => {
    return userProgress?.stats.activitiesByCategory || {};
  };

  const getSkillsCount = () => {
    return userProgress?.skills.length || 0;
  };

  const getMasteredSkillsCount = () => {
    if (!userProgress) return 0;
    return userProgress.skills.filter(skill => {
      const level = Math.floor(skill.experience / 100) + 1;
      return level >= 5; // Consider level 5+ as mastered
    }).length;
  };

  const getAchievementsCount = () => {
    return userProgress?.achievements.filter(a => a.isCompleted).length || 0;
  };

  const getTimeSpentFormatted = () => {
    const totalMinutes = getTotalTimeSpent();
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    
    if (hours > 0) {
      return `${hours}h${minutes > 0 ? ` ${minutes}m` : ''}`;
    }
    return `${minutes}m`;
  };

  return {
    getCompletedActivitiesCount,
    getTotalTimeSpent,
    getCurrentStreak,
    getMaxStreak,
    getFavoriteCategory,
    getActivitiesByCategory,
    getSkillsCount,
    getMasteredSkillsCount,
    getAchievementsCount,
    getTimeSpentFormatted
  };
};

// Hook for achievement-related functionality
export const useAchievementHelpers = () => {
  const { 
    achievements, 
    userProgress, 
    getAchievementProgress,
    canUnlockAchievement,
    unlockAchievement
  } = useGamification();

  const getUnlockedAchievements = () => {
    if (!userProgress) return [];
    const unlockedIds = new Set(userProgress.achievements.map(a => a.achievementId));
    return achievements.filter(a => unlockedIds.has(a.id));
  };

  const getLockedAchievements = () => {
    if (!userProgress) return achievements;
    const unlockedIds = new Set(userProgress.achievements.map(a => a.achievementId));
    return achievements.filter(a => !unlockedIds.has(a.id));
  };

  const getAchievementsByCategory = (category: string) => {
    return achievements.filter(a => a.category === category);
  };

  const getAchievementsByRarity = (rarity: string) => {
    return achievements.filter(a => a.rarity === rarity);
  };

  const getNearCompletionAchievements = (threshold: number = 0.8) => {
    return getLockedAchievements().filter(achievement => {
      const progress = getAchievementProgress(achievement.id);
      return progress >= threshold && progress < 1;
    });
  };

  const getSecretAchievements = () => {
    return achievements.filter(a => a.isSecret);
  };

  const getUnlockedSecretAchievements = () => {
    if (!userProgress) return [];
    const unlockedIds = new Set(userProgress.achievements.map(a => a.achievementId));
    return getSecretAchievements().filter(a => unlockedIds.has(a.id));
  };

  return {
    getUnlockedAchievements,
    getLockedAchievements,
    getAchievementsByCategory,
    getAchievementsByRarity,
    getNearCompletionAchievements,
    getSecretAchievements,
    getUnlockedSecretAchievements,
    unlockAchievement
  };
};

export default GamificationProvider;