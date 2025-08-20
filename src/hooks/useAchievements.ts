/**
 * useAchievements Hook
 * Custom hook for managing achievements and gamification state
 */

import { useState, useEffect, useCallback } from 'react';
import {
  Achievement,
  UserProgress,
  GamificationEvent,
  GamificationNotification,
  PersonalizedRecommendation,
  GamificationConfig
} from '@/lib/gamification/types';
import { GamificationEngine } from '@/lib/gamification/engine';
import { NotificationManager } from '@/lib/gamification/NotificationManager';
import { getAllAchievements } from '@/lib/gamification/achievements';

interface UseAchievementsResult {
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

const STORAGE_KEYS = {
  USER_PROGRESS: 'gamification_user_progress',
  NOTIFICATIONS: 'gamification_notifications'
};

export const useAchievements = (userId: string = 'default'): UseAchievementsResult => {
  // State
  const [userProgress, setUserProgress] = useState<UserProgress | null>(null);
  const [notifications, setNotifications] = useState<GamificationNotification[]>([]);
  const [recommendations, setRecommendations] = useState<PersonalizedRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Instances
  const [engine] = useState(() => new GamificationEngine());
  const [notificationManager] = useState(() => new NotificationManager());

  // Load initial data
  useEffect(() => {
    loadUserData();
  }, [userId]);

  // Setup notification listener
  useEffect(() => {
    const handleNewNotification = (notification: GamificationNotification) => {
      setNotifications(prev => [notification, ...prev]);
    };

    notificationManager.addListener(handleNewNotification);
    return () => notificationManager.removeListener(handleNewNotification);
  }, [notificationManager]);

  // Save data when it changes
  useEffect(() => {
    if (userProgress) {
      saveUserProgress(userProgress);
    }
  }, [userProgress]);

  useEffect(() => {
    if (notifications.length > 0) {
      saveNotifications(notifications);
    }
  }, [notifications]);

  // Load user data from storage
  const loadUserData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // Load user progress
      const savedProgress = localStorage.getItem(STORAGE_KEYS.USER_PROGRESS);
      let progress: UserProgress;

      if (savedProgress) {
        progress = JSON.parse(savedProgress);
        // Convert date strings back to Date objects
        if (progress.lastActivity) {
          progress.lastActivity = new Date(progress.lastActivity);
        }
        progress.achievements.forEach(achievement => {
          achievement.unlockedAt = new Date(achievement.unlockedAt);
        });
        progress.skills.forEach(skill => {
          if (skill.lastActivity) {
            skill.lastActivity = new Date(skill.lastActivity);
          }
        });
      } else {
        // Initialize new user
        progress = engine.initializeUserProgress(userId);
      }

      setUserProgress(progress);

      // Load notifications
      const savedNotifications = localStorage.getItem(STORAGE_KEYS.NOTIFICATIONS);
      if (savedNotifications) {
        const notifs = JSON.parse(savedNotifications) as GamificationNotification[];
        notifs.forEach(notif => {
          notif.timestamp = new Date(notif.timestamp);
        });
        setNotifications(notifs);
        notificationManager.importNotifications(savedNotifications);
      }

      // Generate recommendations
      if (progress) {
        const newRecommendations = engine.generateRecommendations(progress);
        setRecommendations(newRecommendations);
      }
    } catch (err) {
      setError('Failed to load user data');
      console.error('Error loading user data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Save user progress to storage
  const saveUserProgress = (progress: UserProgress) => {
    try {
      localStorage.setItem(STORAGE_KEYS.USER_PROGRESS, JSON.stringify(progress));
    } catch (err) {
      console.error('Error saving user progress:', err);
    }
  };

  // Save notifications to storage
  const saveNotifications = (notifs: GamificationNotification[]) => {
    try {
      localStorage.setItem(STORAGE_KEYS.NOTIFICATIONS, JSON.stringify(notifs));
    } catch (err) {
      console.error('Error saving notifications:', err);
    }
  };

  // Track gamification event
  const trackEvent = useCallback(async (eventData: Omit<GamificationEvent, 'timestamp'>) => {
    if (!userProgress) return;

    try {
      const event: GamificationEvent = {
        ...eventData,
        timestamp: new Date()
      };

      const result = engine.processEvent(event, userProgress);
      
      // Update user progress
      setUserProgress(result.updatedProgress);

      // Handle new achievements
      for (const achievement of result.newAchievements) {
        notificationManager.notifyAchievementUnlocked(achievement);
      }

      // Handle level up
      if (result.levelUp) {
        const oldLevel = userProgress.level.level;
        notificationManager.notifyLevelUp(oldLevel, result.updatedProgress.level);
      }

      // Handle streak milestones
      if (event.type === 'activity_completed' && result.updatedProgress.currentStreak > userProgress.currentStreak) {
        const streak = result.updatedProgress.currentStreak;
        if (streak % 7 === 0 || streak === 3 || streak === 5) {
          notificationManager.notifyStreakMilestone(streak);
        }
      }

      // Refresh recommendations
      const newRecommendations = engine.generateRecommendations(result.updatedProgress);
      setRecommendations(newRecommendations);

    } catch (err) {
      setError('Failed to process event');
      console.error('Error processing event:', err);
    }
  }, [userProgress, engine, notificationManager]);

  // Manually unlock achievement (for testing or admin)
  const unlockAchievement = useCallback((achievementId: string) => {
    if (!userProgress) return;

    const achievement = getAllAchievements().find(a => a.id === achievementId);
    if (!achievement) return;

    const updatedAchievements = [...userProgress.achievements];
    const existingIndex = updatedAchievements.findIndex(a => a.achievementId === achievementId);

    if (existingIndex === -1) {
      updatedAchievements.push({
        achievementId,
        unlockedAt: new Date(),
        isCompleted: true
      });

      const updatedProgress = {
        ...userProgress,
        achievements: updatedAchievements,
        totalXP: userProgress.totalXP + achievement.reward.value
      };

      updatedProgress.level = engine.calculateLevel(updatedProgress.totalXP);
      setUserProgress(updatedProgress);

      notificationManager.notifyAchievementUnlocked(achievement);
    }
  }, [userProgress, engine, notificationManager]);

  // Mark notification as read
  const markNotificationAsRead = useCallback((notificationId: string) => {
    setNotifications(prev => 
      prev.map(notif => 
        notif.id === notificationId 
          ? { ...notif, isRead: true }
          : notif
      )
    );
    notificationManager.markAsRead(notificationId);
  }, [notificationManager]);

  // Mark all notifications as read
  const markAllNotificationsAsRead = useCallback(() => {
    setNotifications(prev => 
      prev.map(notif => ({ ...notif, isRead: true }))
    );
    notificationManager.markAllAsRead();
  }, [notificationManager]);

  // Update user progress manually
  const updateUserProgress = useCallback((updates: Partial<UserProgress>) => {
    if (!userProgress) return;

    const updatedProgress = { ...userProgress, ...updates };
    setUserProgress(updatedProgress);

    // Refresh recommendations
    const newRecommendations = engine.generateRecommendations(updatedProgress);
    setRecommendations(newRecommendations);
  }, [userProgress, engine]);

  // Refresh recommendations
  const refreshRecommendations = useCallback(() => {
    if (!userProgress) return;

    const newRecommendations = engine.generateRecommendations(userProgress);
    setRecommendations(newRecommendations);
  }, [userProgress, engine]);

  // Utility functions
  const getUnreadNotificationsCount = useCallback(() => {
    return notifications.filter(n => !n.isRead).length;
  }, [notifications]);

  const getAchievementProgress = useCallback((achievementId: string) => {
    if (!userProgress) return 0;

    const achievement = getAllAchievements().find(a => a.id === achievementId);
    if (!achievement) return 0;

    // Check if already unlocked
    const userAchievement = userProgress.achievements.find(a => a.achievementId === achievementId);
    if (userAchievement?.isCompleted) return 1;

    // Calculate progress based on requirements
    for (const requirement of achievement.requirements) {
      switch (requirement.type) {
        case 'complete_activities':
          return Math.min(1, userProgress.stats.totalActivities / (requirement.target as number));
        case 'category_activities':
          const categoryCount = userProgress.stats.activitiesByCategory[achievement.category] || 0;
          return Math.min(1, categoryCount / (requirement.target as number));
        case 'consecutive_days':
          return Math.min(1, userProgress.currentStreak / (requirement.target as number));
        case 'total_time':
          return Math.min(1, userProgress.stats.totalTimeSpent / (requirement.target as number));
        default:
          return 0;
      }
    }

    return 0;
  }, [userProgress]);

  const canUnlockAchievement = useCallback((achievementId: string) => {
    return getAchievementProgress(achievementId) >= 1;
  }, [getAchievementProgress]);

  const getUserLevel = useCallback(() => {
    return userProgress?.level.level || 1;
  }, [userProgress]);

  const getTotalXP = useCallback(() => {
    return userProgress?.totalXP || 0;
  }, [userProgress]);

  return {
    // State
    userProgress,
    achievements: getAllAchievements(),
    notifications,
    recommendations,
    isLoading,
    error,

    // Actions
    trackEvent,
    unlockAchievement,
    markNotificationAsRead,
    markAllNotificationsAsRead,
    updateUserProgress,
    refreshRecommendations,

    // Utilities
    getUnreadNotificationsCount,
    getAchievementProgress,
    canUnlockAchievement,
    getUserLevel,
    getTotalXP
  };
};