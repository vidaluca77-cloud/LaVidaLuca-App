/**
 * Achievement Notification Component
 * Displays floating notifications for achievements and gamification events
 */

import React, { useState, useEffect } from 'react';
import { 
  GamificationNotification,
  NotificationType 
} from '@/lib/gamification/types';
import { 
  XMarkIcon,
  BellIcon,
  TrophyIcon,
  StarIcon,
  FireIcon,
  LightBulbIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline';
import { 
  StarIcon as StarSolidIcon,
  TrophyIcon as TrophySolidIcon 
} from '@heroicons/react/24/solid';

interface AchievementNotificationProps {
  notification: GamificationNotification;
  onClose: (id: string) => void;
  onView?: (notification: GamificationNotification) => void;
  autoHide?: boolean;
  autoHideDelay?: number;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'center';
}

const AchievementNotification: React.FC<AchievementNotificationProps> = ({
  notification,
  onClose,
  onView,
  autoHide = true,
  autoHideDelay = 5000,
  position = 'top-right'
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [isExiting, setIsExiting] = useState(false);

  useEffect(() => {
    // Animate in
    setIsVisible(true);

    // Auto hide if enabled
    if (autoHide) {
      const timer = setTimeout(() => {
        handleClose();
      }, autoHideDelay);

      return () => clearTimeout(timer);
    }
  }, [autoHide, autoHideDelay]);

  const handleClose = () => {
    setIsExiting(true);
    setTimeout(() => {
      onClose(notification.id);
    }, 300); // Animation duration
  };

  const handleClick = () => {
    if (onView) {
      onView(notification);
    }
  };

  // Get notification styling based on type and priority
  const getNotificationStyles = () => {
    const baseStyles = "border-2 shadow-lg backdrop-blur-sm";
    
    switch (notification.type) {
      case 'achievement_unlocked':
        return {
          bg: 'bg-gradient-to-r from-yellow-50 to-orange-50',
          border: 'border-yellow-300',
          text: 'text-yellow-800',
          accent: 'text-yellow-600',
          icon: TrophySolidIcon,
          iconColor: 'text-yellow-500'
        };
      case 'level_up':
        return {
          bg: 'bg-gradient-to-r from-purple-50 to-pink-50',
          border: 'border-purple-300',
          text: 'text-purple-800',
          accent: 'text-purple-600',
          icon: StarSolidIcon,
          iconColor: 'text-purple-500'
        };
      case 'streak_milestone':
        return {
          bg: 'bg-gradient-to-r from-red-50 to-orange-50',
          border: 'border-red-300',
          text: 'text-red-800',
          accent: 'text-red-600',
          icon: FireIcon,
          iconColor: 'text-red-500'
        };
      case 'skill_progress':
        return {
          bg: 'bg-gradient-to-r from-blue-50 to-indigo-50',
          border: 'border-blue-300',
          text: 'text-blue-800',
          accent: 'text-blue-600',
          icon: StarIcon,
          iconColor: 'text-blue-500'
        };
      case 'new_recommendation':
        return {
          bg: 'bg-gradient-to-r from-green-50 to-emerald-50',
          border: 'border-green-300',
          text: 'text-green-800',
          accent: 'text-green-600',
          icon: LightBulbIcon,
          iconColor: 'text-green-500'
        };
      case 'challenge_completed':
        return {
          bg: 'bg-gradient-to-r from-indigo-50 to-purple-50',
          border: 'border-indigo-300',
          text: 'text-indigo-800',
          accent: 'text-indigo-600',
          icon: CheckCircleIcon,
          iconColor: 'text-indigo-500'
        };
      default:
        return {
          bg: 'bg-gradient-to-r from-gray-50 to-slate-50',
          border: 'border-gray-300',
          text: 'text-gray-800',
          accent: 'text-gray-600',
          icon: BellIcon,
          iconColor: 'text-gray-500'
        };
    }
  };

  // Get position classes
  const getPositionClasses = () => {
    switch (position) {
      case 'top-left':
        return 'top-4 left-4';
      case 'top-right':
        return 'top-4 right-4';
      case 'bottom-left':
        return 'bottom-4 left-4';
      case 'bottom-right':
        return 'bottom-4 right-4';
      case 'center':
        return 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2';
      default:
        return 'top-4 right-4';
    }
  };

  // Get animation classes
  const getAnimationClasses = () => {
    const enterClasses = isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0';
    const exitClasses = isExiting ? 'translate-x-full opacity-0' : '';
    
    if (position.includes('left')) {
      return isVisible 
        ? (isExiting ? '-translate-x-full opacity-0' : 'translate-x-0 opacity-100')
        : '-translate-x-full opacity-0';
    }
    
    return `${enterClasses} ${exitClasses}`;
  };

  const styles = getNotificationStyles();
  const IconComponent = styles.icon;

  return (
    <div
      className={`
        fixed z-50 w-80 max-w-sm transition-all duration-300 ease-in-out
        ${getPositionClasses()}
        ${getAnimationClasses()}
      `}
    >
      <div
        className={`
          rounded-lg p-4 ${styles.bg} ${styles.border}
          cursor-pointer hover:shadow-xl transition-shadow
        `}
        onClick={handleClick}
      >
        {/* Header */}
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-3">
            {/* Icon or Emoji */}
            <div className="flex-shrink-0">
              {notification.icon ? (
                <span className="text-2xl">{notification.icon}</span>
              ) : (
                <IconComponent className={`w-6 h-6 ${styles.iconColor}`} />
              )}
            </div>
            
            {/* Title */}
            <h3 className={`font-bold text-sm ${styles.text}`}>
              {notification.title}
            </h3>
          </div>

          {/* Close Button */}
          <button
            onClick={(e) => {
              e.stopPropagation();
              handleClose();
            }}
            className={`
              p-1 rounded-full hover:bg-white/50 transition-colors
              ${styles.accent}
            `}
          >
            <XMarkIcon className="w-4 h-4" />
          </button>
        </div>

        {/* Message */}
        <p className={`text-sm mb-3 ${styles.accent}`}>
          {notification.message}
        </p>

        {/* Achievement Data (if available) */}
        {notification.type === 'achievement_unlocked' && notification.data?.achievement && (
          <div className="flex items-center gap-2 mb-2">
            <div className={`
              inline-flex items-center px-2 py-1 rounded-full text-xs font-medium
              ${getRarityBadgeStyles(notification.data.achievement.rarity)}
            `}>
              {notification.data.achievement.rarity}
            </div>
            <span className="text-xs text-gray-600">
              +{notification.data.achievement.reward.value} XP
            </span>
          </div>
        )}

        {/* Level Up Data (if available) */}
        {notification.type === 'level_up' && notification.data?.newLevel && (
          <div className="flex items-center gap-2 mb-2">
            <div className="flex items-center gap-1">
              {[...Array(5)].map((_, i) => (
                <StarSolidIcon 
                  key={i} 
                  className={`w-3 h-3 ${
                    i < Math.min(notification.data.newLevel.level, 5) 
                      ? 'text-yellow-400' 
                      : 'text-gray-300'
                  }`} 
                />
              ))}
            </div>
            <span className="text-xs text-gray-600">
              {notification.data.newLevel.title}
            </span>
          </div>
        )}

        {/* Timestamp */}
        <p className="text-xs text-gray-500">
          {new Date(notification.timestamp).toLocaleTimeString('fr-FR', {
            hour: '2-digit',
            minute: '2-digit'
          })}
        </p>

        {/* Priority Indicator */}
        {notification.priority === 'high' && (
          <div className="absolute top-2 left-2 w-2 h-2 bg-red-500 rounded-full animate-pulse" />
        )}

        {/* Special Effects */}
        {notification.type === 'achievement_unlocked' && notification.data?.achievement?.rarity === 'legendary' && (
          <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-yellow-200 via-transparent to-orange-200 opacity-20 pointer-events-none animate-pulse" />
        )}
      </div>
    </div>
  );
};

// Helper function for rarity badge styles
const getRarityBadgeStyles = (rarity: string) => {
  switch (rarity) {
    case 'common':
      return 'bg-gray-100 text-gray-800';
    case 'rare':
      return 'bg-blue-100 text-blue-800';
    case 'epic':
      return 'bg-purple-100 text-purple-800';
    case 'legendary':
      return 'bg-yellow-100 text-yellow-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

// Container component for managing multiple notifications
interface NotificationContainerProps {
  notifications: GamificationNotification[];
  onClose: (id: string) => void;
  onView?: (notification: GamificationNotification) => void;
  maxNotifications?: number;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left';
}

export const NotificationContainer: React.FC<NotificationContainerProps> = ({
  notifications,
  onClose,
  onView,
  maxNotifications = 3,
  position = 'top-right'
}) => {
  // Show only recent notifications (last N)
  const displayedNotifications = notifications
    .filter(n => !n.isRead)
    .slice(0, maxNotifications);

  return (
    <>
      {displayedNotifications.map((notification, index) => (
        <AchievementNotification
          key={notification.id}
          notification={notification}
          onClose={onClose}
          onView={onView}
          position={position}
        />
      ))}
    </>
  );
};

export default AchievementNotification;