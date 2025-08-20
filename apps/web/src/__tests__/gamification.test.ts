import { renderHook, act } from '@testing-library/react';
import useGamificationStore from '../store/gamification';

// Mock framer-motion to avoid issues in tests
jest.mock('framer-motion', () => ({
  motion: {
    div: 'div',
  },
}));

describe('Gamification Store', () => {
  beforeEach(() => {
    // Reset store before each test
    useGamificationStore.getState().reset();
  });

  it('should initialize with null user stats', () => {
    const { result } = renderHook(() => useGamificationStore());
    
    expect(result.current.userStats).toBeNull();
    expect(result.current.leaderboard).toBeNull();
    expect(result.current.isLoading).toBe(false);
    expect(result.current.error).toBeNull();
  });

  it('should load user stats', async () => {
    const { result } = renderHook(() => useGamificationStore());
    
    await act(async () => {
      await result.current.loadUserStats();
    });

    expect(result.current.userStats).not.toBeNull();
    expect(result.current.userStats?.totalPoints).toBe(350);
    expect(result.current.userStats?.currentLevel.name).toBe('Cultivateur');
  });

  it('should update user stats when action is performed', async () => {
    const { result } = renderHook(() => useGamificationStore());
    
    // First load user stats
    await act(async () => {
      await result.current.loadUserStats();
    });

    const initialPoints = result.current.userStats?.totalPoints || 0;

    // Perform an action
    await act(async () => {
      await result.current.updateUserStats({
        type: 'activity_complete',
        points: 50,
        description: 'Test activity completed'
      });
    });

    expect(result.current.userStats?.totalPoints).toBe(initialPoints + 50);
  });

  it('should calculate correct level for points', () => {
    const { result } = renderHook(() => useGamificationStore());
    
    const level1 = result.current.calculateLevel(50);
    const level2 = result.current.calculateLevel(150);
    const level3 = result.current.calculateLevel(350);

    expect(level1.name).toBe('Apprenti Rural');
    expect(level2.name).toBe('Fermier Débutant');
    expect(level3.name).toBe('Cultivateur');
  });

  it('should load leaderboard', async () => {
    const { result } = renderHook(() => useGamificationStore());
    
    await act(async () => {
      await result.current.loadLeaderboard('weekly');
    });

    expect(result.current.leaderboard).not.toBeNull();
    expect(result.current.leaderboard?.period).toBe('weekly');
    expect(result.current.leaderboard?.users.length).toBeGreaterThan(0);
  });

  it('should unlock achievement', async () => {
    const { result } = renderHook(() => useGamificationStore());
    
    // First load user stats
    await act(async () => {
      await result.current.loadUserStats();
    });

    const initialAchievements = result.current.userStats?.achievements.length || 0;

    // Unlock a new achievement (knowledge_sharer is not in the initial set)
    await act(async () => {
      await result.current.unlockAchievement('knowledge_sharer');
    });

    expect(result.current.userStats?.achievements.length).toBe(initialAchievements + 1);
    expect(result.current.userStats?.achievements.some(a => a.id === 'knowledge_sharer')).toBe(true);
  });

  it('should not unlock the same achievement twice', async () => {
    const { result } = renderHook(() => useGamificationStore());
    
    await act(async () => {
      await result.current.loadUserStats();
    });

    const initialAchievements = result.current.userStats?.achievements.length || 0;

    // Try to unlock an achievement that's already unlocked
    await act(async () => {
      await result.current.unlockAchievement('first_activity');
    });

    expect(result.current.userStats?.achievements.length).toBe(initialAchievements);
  });
});