import React from 'react'
import { cn } from '@/lib/utils'
import { Badge as BadgeType } from '@/types'

interface BadgeProps {
  badge: BadgeType
  size?: 'sm' | 'md' | 'lg'
  showDetails?: boolean
  earned?: boolean
  className?: string
  onClick?: () => void
}

const sizeVariants = {
  sm: 'w-8 h-8',
  md: 'w-12 h-12',
  lg: 'w-16 h-16'
}

const rarityColors = {
  common: 'from-gray-400 to-gray-600',
  rare: 'from-blue-400 to-blue-600',
  epic: 'from-purple-400 to-purple-600',
  legendary: 'from-yellow-400 to-yellow-600'
}

const rarityBorders = {
  common: 'border-gray-300',
  rare: 'border-blue-300',
  epic: 'border-purple-300',
  legendary: 'border-yellow-300'
}

export function BadgeComponent({
  badge,
  size = 'md',
  showDetails = false,
  earned = false,
  className,
  onClick
}: BadgeProps) {
  const isEarned = earned || !!badge.earned_at

  return (
    <div
      className={cn(
        'relative group cursor-pointer',
        onClick && 'hover:scale-105 transition-transform',
        className
      )}
      onClick={onClick}
    >
      {/* Badge Icon */}
      <div
        className={cn(
          'rounded-full border-2 flex items-center justify-center relative overflow-hidden',
          sizeVariants[size],
          isEarned 
            ? `bg-gradient-to-br ${rarityColors[badge.rarity]} ${rarityBorders[badge.rarity]}` 
            : 'bg-gray-100 border-gray-300 opacity-50'
        )}
      >
        {badge.icon ? (
          <img
            src={badge.icon}
            alt={badge.name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="text-white font-bold text-sm">
            {badge.name.charAt(0).toUpperCase()}
          </div>
        )}
        
        {/* Shine effect for earned badges */}
        {isEarned && (
          <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        )}
      </div>

      {/* Rarity indicator */}
      <div className={cn(
        'absolute -top-1 -right-1 w-3 h-3 rounded-full border border-white',
        isEarned ? rarityColors[badge.rarity] : 'bg-gray-300',
        size === 'sm' && 'w-2 h-2',
        size === 'lg' && 'w-4 h-4'
      )} />

      {/* Tooltip/Details */}
      {showDetails && (
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10 whitespace-nowrap">
          <div className="font-medium">{badge.name}</div>
          {badge.description && (
            <div className="text-gray-300 text-xs mt-1">
              {badge.description}
            </div>
          )}
          <div className="text-xs text-gray-400 mt-1 capitalize">
            {badge.rarity}
          </div>
          {badge.earned_at && (
            <div className="text-xs text-green-400 mt-1">
              Obtenu le {new Date(badge.earned_at).toLocaleDateString('fr-FR')}
            </div>
          )}
          {/* Arrow */}
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 border-4 border-transparent border-t-gray-900" />
        </div>
      )}
    </div>
  )
}

// Badge grid component for displaying multiple badges
interface BadgeGridProps {
  badges: BadgeType[]
  maxDisplay?: number
  size?: 'sm' | 'md' | 'lg'
  showDetails?: boolean
  onBadgeClick?: (badge: BadgeType) => void
  className?: string
}

export function BadgeGrid({
  badges,
  maxDisplay,
  size = 'md',
  showDetails = true,
  onBadgeClick,
  className
}: BadgeGridProps) {
  const displayBadges = maxDisplay ? badges.slice(0, maxDisplay) : badges
  const remainingCount = maxDisplay && badges.length > maxDisplay 
    ? badges.length - maxDisplay 
    : 0

  return (
    <div className={cn('flex flex-wrap gap-2', className)}>
      {displayBadges.map((badge) => (
        <BadgeComponent
          key={badge.id}
          badge={badge}
          size={size}
          showDetails={showDetails}
          onClick={() => onBadgeClick?.(badge)}
        />
      ))}
      
      {remainingCount > 0 && (
        <div
          className={cn(
            'rounded-full border-2 border-gray-300 bg-gray-100 flex items-center justify-center text-gray-600 font-medium',
            sizeVariants[size]
          )}
        >
          +{remainingCount}
        </div>
      )}
    </div>
  )
}

// Badge showcase component with rarity grouping
interface BadgeShowcaseProps {
  badges: BadgeType[]
  title?: string
  className?: string
}

export function BadgeShowcase({ badges, title, className }: BadgeShowcaseProps) {
  const badgesByRarity = badges.reduce((acc, badge) => {
    if (!acc[badge.rarity]) {
      acc[badge.rarity] = []
    }
    acc[badge.rarity].push(badge)
    return acc
  }, {} as Record<string, BadgeType[]>)

  const rarityOrder: Array<keyof typeof rarityColors> = ['legendary', 'epic', 'rare', 'common']

  return (
    <div className={cn('space-y-6', className)}>
      {title && (
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
      )}
      
      {rarityOrder.map((rarity) => {
        const rarityBadges = badgesByRarity[rarity]
        if (!rarityBadges || rarityBadges.length === 0) return null

        return (
          <div key={rarity} className="space-y-3">
            <h4 className="text-sm font-medium text-gray-700 capitalize flex items-center gap-2">
              <div className={cn(
                'w-3 h-3 rounded-full bg-gradient-to-br',
                rarityColors[rarity]
              )} />
              {rarity} ({rarityBadges.length})
            </h4>
            <BadgeGrid badges={rarityBadges} size="md" />
          </div>
        )
      })}
    </div>
  )
}