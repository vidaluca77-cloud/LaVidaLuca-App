import React from 'react'
import { cn } from '@/lib/utils'
import { ProgressBar, CircularProgress } from '@/components/ui/ProgressBar'
import { formatPoints } from '@/lib/utils'

interface UserLevelProps {
  level: number
  experiencePoints: number
  totalPoints: number
  variant?: 'card' | 'compact' | 'minimal'
  showProgress?: boolean
  className?: string
}

// Level thresholds matching backend logic
const LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000]

const getLevelInfo = (level: number, experiencePoints: number) => {
  const currentLevelXP = LEVEL_THRESHOLDS[level - 1] || 0
  const nextLevelXP = LEVEL_THRESHOLDS[level] || LEVEL_THRESHOLDS[LEVEL_THRESHOLDS.length - 1]
  const isMaxLevel = level >= LEVEL_THRESHOLDS.length
  
  const progress = isMaxLevel 
    ? 100 
    : ((experiencePoints - currentLevelXP) / (nextLevelXP - currentLevelXP)) * 100
  
  const pointsToNext = isMaxLevel ? 0 : nextLevelXP - experiencePoints

  return {
    currentLevelXP,
    nextLevelXP,
    isMaxLevel,
    progress: Math.max(0, Math.min(100, progress)),
    pointsToNext
  }
}

const getLevelColor = (level: number) => {
  if (level >= 10) return 'from-purple-500 to-purple-600'
  if (level >= 7) return 'from-blue-500 to-blue-600'
  if (level >= 4) return 'from-green-500 to-green-600'
  if (level >= 2) return 'from-yellow-500 to-yellow-600'
  return 'from-gray-500 to-gray-600'
}

const getLevelTitle = (level: number) => {
  if (level >= 10) return 'Expert'
  if (level >= 7) return 'Avancé'
  if (level >= 4) return 'Intermédiaire'
  if (level >= 2) return 'Apprenti'
  return 'Débutant'
}

export function UserLevel({
  level,
  experiencePoints,
  totalPoints,
  variant = 'card',
  showProgress = true,
  className
}: UserLevelProps) {
  const levelInfo = getLevelInfo(level, experiencePoints)
  const levelColor = getLevelColor(level)
  const levelTitle = getLevelTitle(level)

  if (variant === 'minimal') {
    return (
      <div className={cn('flex items-center gap-2', className)}>
        <div className={cn(
          'w-8 h-8 rounded-full bg-gradient-to-br flex items-center justify-center text-white font-bold text-sm',
          levelColor
        )}>
          {level}
        </div>
        <div>
          <div className="text-sm font-medium text-gray-900">
            Niveau {level}
          </div>
          <div className="text-xs text-gray-500">
            {levelTitle}
          </div>
        </div>
      </div>
    )
  }

  if (variant === 'compact') {
    return (
      <div className={cn('bg-white rounded-lg border p-3', className)}>
        <div className="flex items-center gap-3">
          <div className={cn(
            'w-12 h-12 rounded-full bg-gradient-to-br flex items-center justify-center text-white font-bold',
            levelColor
          )}>
            {level}
          </div>
          
          <div className="flex-1">
            <div className="flex items-center justify-between mb-1">
              <span className="font-medium text-gray-900">
                Niveau {level} - {levelTitle}
              </span>
              <span className="text-sm text-gray-600">
                {formatPoints(totalPoints)} pts
              </span>
            </div>
            
            {showProgress && !levelInfo.isMaxLevel && (
              <ProgressBar
                value={levelInfo.progress}
                max={100}
                color="blue"
                size="sm"
              />
            )}
            
            {levelInfo.isMaxLevel && (
              <div className="text-sm text-purple-600 font-medium">
                Niveau maximum atteint! 🎉
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  // Full card variant
  return (
    <div className={cn('bg-white rounded-lg border p-4', className)}>
      <div className="text-center space-y-4">
        {/* Level badge */}
        <div className="relative inline-block">
          <div className={cn(
            'w-20 h-20 rounded-full bg-gradient-to-br flex items-center justify-center text-white font-bold text-2xl shadow-lg',
            levelColor
          )}>
            {level}
          </div>
          
          {/* Level progress ring */}
          {showProgress && !levelInfo.isMaxLevel && (
            <div className="absolute inset-0">
              <CircularProgress
                value={levelInfo.progress}
                max={100}
                size={80}
                strokeWidth={3}
                color="blue"
              />
            </div>
          )}
        </div>

        {/* Level info */}
        <div>
          <h3 className="text-xl font-bold text-gray-900">
            Niveau {level}
          </h3>
          <p className="text-gray-600">
            {levelTitle}
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4 text-center">
          <div>
            <div className="text-lg font-bold text-blue-600">
              {formatPoints(experiencePoints)}
            </div>
            <div className="text-sm text-gray-600">XP</div>
          </div>
          <div>
            <div className="text-lg font-bold text-yellow-600">
              {formatPoints(totalPoints)}
            </div>
            <div className="text-sm text-gray-600">Points totaux</div>
          </div>
        </div>

        {/* Progress info */}
        {showProgress && (
          <div className="space-y-2">
            {levelInfo.isMaxLevel ? (
              <div className="text-center">
                <div className="text-purple-600 font-medium">
                  🎉 Niveau maximum atteint!
                </div>
                <div className="text-sm text-gray-500">
                  Félicitations pour votre expertise!
                </div>
              </div>
            ) : (
              <>
                <ProgressBar
                  value={levelInfo.progress}
                  max={100}
                  label={`Progression vers le niveau ${level + 1}`}
                  color="blue"
                  showPercentage
                />
                <div className="text-sm text-gray-600">
                  {formatPoints(levelInfo.pointsToNext)} XP restants pour le niveau suivant
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

// Level icon component for use in other components
interface LevelIconProps {
  level: number
  size?: 'sm' | 'md' | 'lg'
  showTitle?: boolean
  className?: string
}

const sizeVariants = {
  sm: 'w-6 h-6 text-xs',
  md: 'w-8 h-8 text-sm',
  lg: 'w-10 h-10 text-base'
}

export function LevelIcon({ level, size = 'md', showTitle = false, className }: LevelIconProps) {
  const levelColor = getLevelColor(level)
  const levelTitle = getLevelTitle(level)

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <div
        className={cn(
          'rounded-full bg-gradient-to-br flex items-center justify-center text-white font-bold',
          levelColor,
          sizeVariants[size]
        )}
        title={`Niveau ${level} - ${levelTitle}`}
      >
        {level}
      </div>
      {showTitle && (
        <span className="text-sm text-gray-600">
          {levelTitle}
        </span>
      )}
    </div>
  )
}

// Level comparison component
interface LevelComparisonProps {
  userLevel: number
  compareLevel: number
  className?: string
}

export function LevelComparison({ userLevel, compareLevel, className }: LevelComparisonProps) {
  const difference = userLevel - compareLevel
  const isHigher = difference > 0
  const isEqual = difference === 0

  return (
    <div className={cn('flex items-center gap-2', className)}>
      <LevelIcon level={userLevel} size="sm" />
      
      {isEqual ? (
        <span className="text-sm text-gray-600">Même niveau</span>
      ) : (
        <>
          <span className={cn(
            'text-sm font-medium',
            isHigher ? 'text-green-600' : 'text-red-600'
          )}>
            {isHigher ? '+' : ''}{difference}
          </span>
          <span className="text-sm text-gray-600">
            {isHigher ? 'niveaux au-dessus' : 'niveaux en-dessous'}
          </span>
        </>
      )}
    </div>
  )
}