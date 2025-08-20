'use client'

import { useState, useEffect } from 'react'
import { Achievement, UserStats, LeaderboardEntry, Badge } from '@/types'
import { api } from '@/lib/api'

export function useGamification() {
  const [stats, setStats] = useState<UserStats | null>(null)
  const [achievements, setAchievements] = useState<Achievement[]>([])
  const [badges, setBadges] = useState<Badge[]>([])
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Load initial data
  useEffect(() => {
    loadGamificationData()
  }, [])

  const loadGamificationData = async () => {
    try {
      setIsLoading(true)
      setError(null)

      const [statsData, achievementsData, badgesData, leaderboardData] = await Promise.all([
        api.getUserStats(),
        api.getAchievements(),
        api.getBadges(),
        api.getLeaderboard()
      ])

      setStats(statsData)
      setAchievements(achievementsData)
      setBadges(badgesData)
      setLeaderboard(leaderboardData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors du chargement')
      console.error('Failed to load gamification data:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const claimAchievement = async (achievementId: number) => {
    try {
      const result = await api.claimAchievement(achievementId)
      
      // Update achievements list
      setAchievements(prev => 
        prev.map(achievement => 
          achievement.id === achievementId 
            ? { ...achievement, completed_at: new Date().toISOString() }
            : achievement
        )
      )

      // Refresh stats to reflect new points
      const updatedStats = await api.getUserStats()
      setStats(updatedStats)

      return result
    } catch (err) {
      console.error('Failed to claim achievement:', err)
      throw err
    }
  }

  const refreshStats = async () => {
    try {
      const updatedStats = await api.getUserStats()
      setStats(updatedStats)
    } catch (err) {
      console.error('Failed to refresh stats:', err)
    }
  }

  const getCompletedAchievements = () => {
    return achievements.filter(achievement => achievement.is_completed)
  }

  const getUncompletedAchievements = () => {
    return achievements.filter(achievement => !achievement.is_completed)
  }

  const getEarnedBadges = () => {
    return badges.filter(badge => badge.earned_at)
  }

  const getAvailableBadges = () => {
    return badges.filter(badge => !badge.earned_at)
  }

  const calculateLevelProgress = () => {
    if (!stats) return { progress: 0, nextLevelXP: 100 }
    
    // Simple level calculation - in a real app this would match backend logic
    const levelThresholds = [0, 100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000]
    const currentLevel = stats.level
    const currentXP = stats.experience_points
    
    const currentLevelXP = levelThresholds[currentLevel - 1] || 0
    const nextLevelXP = levelThresholds[currentLevel] || levelThresholds[levelThresholds.length - 1]
    
    const progress = ((currentXP - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100
    
    return {
      progress: Math.max(0, Math.min(100, progress)),
      nextLevelXP: nextLevelXP - currentXP
    }
  }

  return {
    stats,
    achievements,
    badges,
    leaderboard,
    isLoading,
    error,
    claimAchievement,
    refreshStats,
    loadGamificationData,
    getCompletedAchievements,
    getUncompletedAchievements,
    getEarnedBadges,
    getAvailableBadges,
    calculateLevelProgress
  }
}

export function useAchievements(category?: string) {
  const [achievements, setAchievements] = useState<Achievement[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadAchievements()
  }, [category])

  const loadAchievements = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await api.getAchievements({ category })
      setAchievements(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors du chargement')
    } finally {
      setIsLoading(false)
    }
  }

  return {
    achievements,
    isLoading,
    error,
    refetch: loadAchievements
  }
}

export function useLeaderboard(period: 'weekly' | 'monthly' | 'all_time' = 'monthly', limit: number = 10) {
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadLeaderboard()
  }, [period, limit])

  const loadLeaderboard = async () => {
    try {
      setIsLoading(true)
      setError(null)
      const data = await api.getLeaderboard(period, limit)
      setLeaderboard(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors du chargement')
    } finally {
      setIsLoading(false)
    }
  }

  return {
    leaderboard,
    isLoading,
    error,
    refetch: loadLeaderboard
  }
}