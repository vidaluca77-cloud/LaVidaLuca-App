import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { UserStats, UserLevel, Achievement, Badge, GamificationAction, Leaderboard } from '../types/gamification';

// Default levels configuration
const LEVELS: UserLevel[] = [
  { level: 1, name: 'Apprenti Rural', minPoints: 0, maxPoints: 99, color: '#94A3B8', icon: '🌱', benefits: ['Accès aux activités de base'] },
  { level: 2, name: 'Fermier Débutant', minPoints: 100, maxPoints: 249, color: '#84CC16', icon: '🚜', benefits: ['Suggestions IA personnalisées', 'Accès forum'] },
  { level: 3, name: 'Cultivateur', minPoints: 250, maxPoints: 499, color: '#EAB308', icon: '🌾', benefits: ['Mentorat junior', 'Badges exclusifs'] },
  { level: 4, name: 'Maître Artisan', minPoints: 500, maxPoints: 999, color: '#F97316', icon: '🛠️', benefits: ['Création d\'ateliers', 'Certification'] },
  { level: 5, name: 'Expert Innovateur', minPoints: 1000, maxPoints: 1999, color: '#EF4444', icon: '💡', benefits: ['Projets collaboratifs', 'Mentorat senior'] },
  { level: 6, name: 'Leader Communautaire', minPoints: 2000, maxPoints: 4999, color: '#8B5CF6', icon: '👥', benefits: ['Organisation d\'événements', 'Responsabilités communautaires'] },
  { level: 7, name: 'Ambassadeur', minPoints: 5000, maxPoints: 9999, color: '#06B6D4', icon: '🌟', benefits: ['Représentation externe', 'Partenariats'] },
  { level: 8, name: 'Pionnier Visionnaire', minPoints: 10000, maxPoints: Infinity, color: '#DC2626', icon: '🚀', benefits: ['Toutes les fonctionnalités', 'Statut légendaire'] }
];

// Default achievements
const DEFAULT_ACHIEVEMENTS: Achievement[] = [
  {
    id: 'first_activity',
    name: 'Premier Pas',
    description: 'Complétez votre première activité',
    icon: '👶',
    category: 'learning',
    points: 50,
    rarity: 'common',
    maxProgress: 1
  },
  {
    id: 'week_streak',
    name: 'Persévérant',
    description: 'Connectez-vous 7 jours consécutifs',
    icon: '🔥',
    category: 'participation',
    points: 100,
    rarity: 'uncommon',
    maxProgress: 7
  },
  {
    id: 'knowledge_sharer',
    name: 'Partageur de Savoir',
    description: 'Partagez 5 connaissances avec la communauté',
    icon: '📚',
    category: 'sharing',
    points: 150,
    rarity: 'rare',
    maxProgress: 5
  },
  {
    id: 'helper',
    name: 'Bon Samaritain',
    description: 'Aidez 10 membres de la communauté',
    icon: '🤝',
    category: 'leadership',
    points: 200,
    rarity: 'epic',
    maxProgress: 10
  },
  {
    id: 'innovator',
    name: 'Innovateur',
    description: 'Proposez une solution créative adoptée par la communauté',
    icon: '💡',
    category: 'innovation',
    points: 300,
    rarity: 'legendary',
    maxProgress: 1
  }
];

interface GamificationState {
  userStats: UserStats | null;
  leaderboard: Leaderboard | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  loadUserStats: () => Promise<void>;
  updateUserStats: (action: GamificationAction) => Promise<void>;
  loadLeaderboard: (period: 'daily' | 'weekly' | 'monthly' | 'all-time') => Promise<void>;
  calculateLevel: (points: number) => UserLevel;
  unlockAchievement: (achievementId: string) => Promise<void>;
  reset: () => void;
}

const useGamificationStore = create<GamificationState>()(
  devtools(
    (set, get) => ({
      userStats: null,
      leaderboard: null,
      isLoading: false,
      error: null,

      loadUserStats: async () => {
        set({ isLoading: true, error: null });
        
        try {
          // For now, use mock data - replace with API call
          const mockStats: UserStats = {
            totalPoints: 350,
            currentLevel: LEVELS[2], // Cultivateur
            nextLevel: LEVELS[3],
            pointsToNextLevel: 150,
            achievements: DEFAULT_ACHIEVEMENTS.slice(0, 2).map(a => ({ ...a, unlockedAt: new Date() })),
            badges: [],
            streak: {
              current: 5,
              best: 12,
              lastActivity: new Date()
            },
            activitiesCompleted: 8,
            averageRating: 4.3,
            contributionsShared: 3
          };
          
          set({ userStats: mockStats, isLoading: false });
        } catch (error) {
          set({ error: 'Failed to load user stats', isLoading: false });
        }
      },

      updateUserStats: async (action: GamificationAction) => {
        const { userStats } = get();
        if (!userStats) return;

        try {
          const newPoints = userStats.totalPoints + action.points;
          const newLevel = get().calculateLevel(newPoints);
          const nextLevel = LEVELS.find(l => l.level === newLevel.level + 1);
          
          const updatedStats: UserStats = {
            ...userStats,
            totalPoints: newPoints,
            currentLevel: newLevel,
            nextLevel,
            pointsToNextLevel: nextLevel ? nextLevel.minPoints - newPoints : 0
          };

          set({ userStats: updatedStats });
          
          // Here you would typically make an API call to persist the changes
        } catch (error) {
          set({ error: 'Failed to update user stats' });
        }
      },

      loadLeaderboard: async (period) => {
        set({ isLoading: true, error: null });
        
        try {
          // Mock leaderboard data - replace with API call
          const mockLeaderboard: Leaderboard = {
            period,
            users: [
              { userId: '1', username: 'AliceF', points: 1250, level: LEVELS[4], rank: 1, change: 'same' },
              { userId: '2', username: 'BobM', points: 980, level: LEVELS[3], rank: 2, change: 'up' },
              { userId: '3', username: 'CarlaL', points: 875, level: LEVELS[3], rank: 3, change: 'down' },
              { userId: '4', username: 'DavidR', points: 650, level: LEVELS[3], rank: 4, change: 'new' },
              { userId: '5', username: 'EvaK', points: 420, level: LEVELS[2], rank: 5, change: 'same' }
            ]
          };
          
          set({ leaderboard: mockLeaderboard, isLoading: false });
        } catch (error) {
          set({ error: 'Failed to load leaderboard', isLoading: false });
        }
      },

      calculateLevel: (points: number): UserLevel => {
        return LEVELS.find(level => points >= level.minPoints && points <= level.maxPoints) || LEVELS[0];
      },

      unlockAchievement: async (achievementId: string) => {
        const { userStats } = get();
        if (!userStats) return;

        const achievement = DEFAULT_ACHIEVEMENTS.find(a => a.id === achievementId);
        if (!achievement) return;

        if (!userStats.achievements.find(a => a.id === achievementId)) {
          const unlockedAchievement = { ...achievement, unlockedAt: new Date() };
          
          set({
            userStats: {
              ...userStats,
              achievements: [...userStats.achievements, unlockedAchievement],
              totalPoints: userStats.totalPoints + achievement.points
            }
          });
          
          // Here you would typically make an API call to persist the achievement
        }
      },

      reset: () => {
        set({
          userStats: null,
          leaderboard: null,
          isLoading: false,
          error: null
        });
      }
    }),
    {
      name: 'gamification-store'
    }
  )
);

export default useGamificationStore;