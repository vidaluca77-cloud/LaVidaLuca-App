// Gamification types for La Vida Luca App

export interface Achievement {
  id: string;
  name: string;
  description: string;
  icon: string;
  category: 'learning' | 'participation' | 'sharing' | 'leadership' | 'innovation';
  points: number;
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary';
  unlockedAt?: Date;
  progress?: number;
  maxProgress?: number;
}

export interface Badge {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  achievementId: string;
  earnedAt?: Date;
}

export interface UserLevel {
  level: number;
  name: string;
  minPoints: number;
  maxPoints: number;
  color: string;
  icon: string;
  benefits: string[];
}

export interface UserStats {
  totalPoints: number;
  currentLevel: UserLevel;
  nextLevel?: UserLevel;
  pointsToNextLevel: number;
  achievements: Achievement[];
  badges: Badge[];
  streak: {
    current: number;
    best: number;
    lastActivity: Date;
  };
  activitiesCompleted: number;
  averageRating: number;
  contributionsShared: number;
}

export interface GamificationAction {
  type: 'activity_complete' | 'daily_login' | 'share_knowledge' | 'help_peer' | 'innovative_solution' | 'leadership';
  points: number;
  description: string;
  metadata?: Record<string, any>;
}

export interface Leaderboard {
  period: 'daily' | 'weekly' | 'monthly' | 'all-time';
  users: LeaderboardEntry[];
}

export interface LeaderboardEntry {
  userId: string;
  username: string;
  avatar?: string;
  points: number;
  level: UserLevel;
  rank: number;
  change: 'up' | 'down' | 'same' | 'new';
}