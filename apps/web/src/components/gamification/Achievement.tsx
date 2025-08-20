import React, { useState } from 'react'
import { cn } from '@/lib/utils'
import { Achievement as AchievementType } from '@/types'
import { ProgressBar } from '@/components/ui/ProgressBar'

interface AchievementProps {
  achievement: AchievementType
  onClaim?: (achievementId: number) => Promise<void>
  className?: string
}

const categoryColors = {
  agriculture: 'from-green-500 to-green-600',
  engagement: 'from-blue-500 to-blue-600',
  learning: 'from-purple-500 to-purple-600',
  community: 'from-yellow-500 to-yellow-600',
  completion: 'from-red-500 to-red-600'
}

export function AchievementCard({ achievement, onClaim, className }: AchievementProps) {
  const [isClaiming, setIsClaiming] = useState(false)
  
  const isCompleted = achievement.is_completed
  const canClaim = isCompleted && !achievement.completed_at
  const progress = achievement.progress || 0
  const maxProgress = achievement.max_progress || 1
  const progressPercentage = maxProgress > 0 ? (progress / maxProgress) * 100 : 0

  const handleClaim = async () => {
    if (!canClaim || !onClaim) return
    
    setIsClaiming(true)
    try {
      await onClaim(achievement.id)
    } catch (error) {
      console.error('Failed to claim achievement:', error)
    } finally {
      setIsClaiming(false)
    }
  }

  return (
    <div
      className={cn(
        'bg-white rounded-lg border shadow-sm hover:shadow-md transition-all duration-200',
        isCompleted ? 'border-green-200 bg-green-50/30' : 'border-gray-200',
        className
      )}
    >
      <div className="p-4">
        <div className="flex items-start gap-4">
          {/* Achievement Icon */}
          <div
            className={cn(
              'w-12 h-12 rounded-lg flex items-center justify-center text-white font-bold text-lg flex-shrink-0',
              isCompleted
                ? `bg-gradient-to-br ${categoryColors[achievement.category as keyof typeof categoryColors] || 'from-gray-500 to-gray-600'}`
                : 'bg-gray-300'
            )}
          >
            {achievement.icon ? (
              <img
                src={achievement.icon}
                alt={achievement.name}
                className="w-full h-full object-cover rounded-lg"
              />
            ) : (
              achievement.name.charAt(0).toUpperCase()
            )}
          </div>

          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between gap-2">
              <div className="flex-1">
                <h3 className={cn(
                  'font-semibold text-gray-900',
                  isCompleted && 'text-green-800'
                )}>
                  {achievement.name}
                </h3>
                
                {achievement.description && (
                  <p className="text-sm text-gray-600 mt-1 line-clamp-2">
                    {achievement.description}
                  </p>
                )}

                <div className="flex items-center gap-4 mt-2">
                  <span className={cn(
                    'text-xs px-2 py-1 rounded-full font-medium',
                    'bg-gray-100 text-gray-700'
                  )}>
                    {achievement.category}
                  </span>
                  
                  <span className="text-sm font-medium text-yellow-600">
                    {achievement.points} pts
                  </span>
                </div>
              </div>

              {/* Status indicator */}
              {isCompleted && (
                <div className={cn(
                  'w-6 h-6 rounded-full flex items-center justify-center',
                  achievement.completed_at ? 'bg-green-500' : 'bg-yellow-500'
                )}>
                  {achievement.completed_at ? (
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  )}
                </div>
              )}
            </div>

            {/* Progress bar */}
            {!isCompleted && maxProgress > 1 && (
              <div className="mt-3">
                <ProgressBar
                  value={progress}
                  max={maxProgress}
                  label={`Progression: ${progress}/${maxProgress}`}
                  color="blue"
                  size="sm"
                  showPercentage
                />
              </div>
            )}

            {/* Claim button */}
            {canClaim && (
              <div className="mt-3">
                <button
                  onClick={handleClaim}
                  disabled={isClaiming}
                  className={cn(
                    'px-4 py-2 rounded-lg font-medium transition-colors',
                    'bg-green-600 hover:bg-green-700 text-white',
                    'disabled:opacity-50 disabled:cursor-not-allowed'
                  )}
                >
                  {isClaiming ? 'Récupération...' : `Récupérer ${achievement.points} pts`}
                </button>
              </div>
            )}

            {/* Completion timestamp */}
            {achievement.completed_at && (
              <div className="mt-2 text-xs text-gray-500">
                Obtenu le {new Date(achievement.completed_at).toLocaleDateString('fr-FR', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric'
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// Grid component for displaying multiple achievements
interface AchievementGridProps {
  achievements: AchievementType[]
  onClaim?: (achievementId: number) => Promise<void>
  filter?: 'all' | 'completed' | 'in_progress' | 'locked'
  category?: string
  className?: string
}

export function AchievementGrid({
  achievements,
  onClaim,
  filter = 'all',
  category,
  className
}: AchievementGridProps) {
  const filteredAchievements = achievements.filter(achievement => {
    // Category filter
    if (category && achievement.category !== category) return false
    
    // Status filter
    switch (filter) {
      case 'completed':
        return achievement.is_completed
      case 'in_progress':
        return !achievement.is_completed && (achievement.progress || 0) > 0
      case 'locked':
        return !achievement.is_completed && (achievement.progress || 0) === 0
      default:
        return true
    }
  })

  if (filteredAchievements.length === 0) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-400 text-lg mb-2">🏆</div>
        <p className="text-gray-600">Aucun succès à afficher</p>
      </div>
    )
  }

  return (
    <div className={cn('grid gap-4 md:grid-cols-2 lg:grid-cols-3', className)}>
      {filteredAchievements.map(achievement => (
        <AchievementCard
          key={achievement.id}
          achievement={achievement}
          onClaim={onClaim}
        />
      ))}
    </div>
  )
}

// Achievement summary component
interface AchievementSummaryProps {
  achievements: AchievementType[]
  className?: string
}

export function AchievementSummary({ achievements, className }: AchievementSummaryProps) {
  const total = achievements.length
  const completed = achievements.filter(a => a.is_completed).length
  const inProgress = achievements.filter(a => !a.is_completed && (a.progress || 0) > 0).length
  const locked = total - completed - inProgress

  const completionRate = total > 0 ? (completed / total) * 100 : 0

  return (
    <div className={cn('bg-white rounded-lg border p-4', className)}>
      <h3 className="font-semibold text-gray-900 mb-4">Résumé des succès</h3>
      
      <div className="space-y-3">
        <ProgressBar
          value={completed}
          max={total}
          label="Progression globale"
          color="green"
          showPercentage
        />
        
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-green-600">{completed}</div>
            <div className="text-xs text-gray-600">Obtenus</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-blue-600">{inProgress}</div>
            <div className="text-xs text-gray-600">En cours</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-gray-400">{locked}</div>
            <div className="text-xs text-gray-600">Verrouillés</div>
          </div>
        </div>
      </div>
    </div>
  )
}