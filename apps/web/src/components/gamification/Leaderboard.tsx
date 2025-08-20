import React from 'react'
import { cn } from '@/lib/utils'
import { LeaderboardEntry } from '@/types'
import { formatPoints } from '@/lib/utils'

interface LeaderboardProps {
  entries: LeaderboardEntry[]
  currentUserId?: number
  period?: 'weekly' | 'monthly' | 'all_time'
  showRank?: boolean
  maxEntries?: number
  className?: string
}

export function Leaderboard({
  entries,
  currentUserId,
  period = 'monthly',
  showRank = true,
  maxEntries,
  className
}: LeaderboardProps) {
  const displayEntries = maxEntries ? entries.slice(0, maxEntries) : entries
  
  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return '🥇'
      case 2:
        return '🥈'
      case 3:
        return '🥉'
      default:
        return null
    }
  }

  const getRankColor = (rank: number) => {
    switch (rank) {
      case 1:
        return 'text-yellow-600 bg-yellow-50 border-yellow-200'
      case 2:
        return 'text-gray-600 bg-gray-50 border-gray-200'
      case 3:
        return 'text-orange-600 bg-orange-50 border-orange-200'
      default:
        return 'text-gray-700 bg-white border-gray-200'
    }
  }

  const periodLabels = {
    weekly: 'Semaine',
    monthly: 'Mois',
    all_time: 'Tous temps'
  }

  return (
    <div className={cn('bg-white rounded-lg border', className)}>
      <div className="p-4 border-b">
        <h3 className="font-semibold text-gray-900 flex items-center gap-2">
          🏆 Classement - {periodLabels[period]}
        </h3>
        <p className="text-sm text-gray-600 mt-1">
          Top {displayEntries.length} des meilleurs participants
        </p>
      </div>

      <div className="divide-y divide-gray-100">
        {displayEntries.map((entry, index) => (
          <div
            key={entry.user_id}
            className={cn(
              'p-4 transition-colors',
              entry.user_id === currentUserId && 'bg-blue-50 border-l-4 border-l-blue-500',
              'hover:bg-gray-50'
            )}
          >
            <div className="flex items-center gap-4">
              {/* Rank */}
              {showRank && (
                <div className={cn(
                  'w-8 h-8 rounded-full border-2 flex items-center justify-center font-bold text-sm',
                  getRankColor(entry.rank)
                )}>
                  {getRankIcon(entry.rank) || entry.rank}
                </div>
              )}

              {/* User Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h4 className="font-medium text-gray-900 truncate">
                    {entry.full_name || entry.username}
                  </h4>
                  {entry.user_id === currentUserId && (
                    <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                      Vous
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-600">
                  @{entry.username}
                </p>
              </div>

              {/* Stats */}
              <div className="text-right space-y-1">
                <div className="font-bold text-lg text-gray-900">
                  {formatPoints(entry.total_points)}
                </div>
                <div className="text-xs text-gray-500">
                  Niveau {entry.level}
                </div>
              </div>

              {/* Additional stats */}
              <div className="text-right space-y-1 text-xs text-gray-500 hidden sm:block">
                <div>🏆 {entry.achievements_count}</div>
                <div>🎖️ {entry.badges_count}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {maxEntries && entries.length > maxEntries && (
        <div className="p-4 text-center border-t">
          <button className="text-sm text-blue-600 hover:text-blue-800 font-medium">
            Voir le classement complet
          </button>
        </div>
      )}
    </div>
  )
}

// Compact leaderboard for sidebars/widgets
interface CompactLeaderboardProps {
  entries: LeaderboardEntry[]
  currentUserId?: number
  maxEntries?: number
  className?: string
}

export function CompactLeaderboard({
  entries,
  currentUserId,
  maxEntries = 5,
  className
}: CompactLeaderboardProps) {
  const displayEntries = entries.slice(0, maxEntries)

  return (
    <div className={cn('space-y-2', className)}>
      {displayEntries.map((entry, index) => (
        <div
          key={entry.user_id}
          className={cn(
            'flex items-center gap-3 p-2 rounded-lg',
            entry.user_id === currentUserId ? 'bg-blue-50' : 'hover:bg-gray-50'
          )}
        >
          <div className={cn(
            'w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold',
            entry.rank <= 3 ? getRankColor(entry.rank) : 'bg-gray-100 text-gray-600'
          )}>
            {entry.rank}
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="font-medium text-sm text-gray-900 truncate">
              {entry.full_name || entry.username}
            </div>
            <div className="text-xs text-gray-500">
              {formatPoints(entry.total_points)} pts
            </div>
          </div>

          {entry.user_id === currentUserId && (
            <div className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
              Vous
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

// Personal rank widget
interface PersonalRankProps {
  userStats?: {
    rank?: number
    total_points: number
    level: number
  }
  totalParticipants?: number
  className?: string
}

export function PersonalRank({
  userStats,
  totalParticipants,
  className
}: PersonalRankProps) {
  if (!userStats) {
    return (
      <div className={cn('bg-white rounded-lg border p-4', className)}>
        <div className="animate-pulse space-y-2">
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          <div className="h-8 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    )
  }

  const { rank, total_points, level } = userStats
  const percentile = totalParticipants && rank 
    ? Math.round(((totalParticipants - rank + 1) / totalParticipants) * 100)
    : null

  return (
    <div className={cn('bg-white rounded-lg border p-4', className)}>
      <h3 className="font-semibold text-gray-900 mb-3">Votre classement</h3>
      
      <div className="space-y-3">
        {rank && (
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              #{rank}
            </div>
            {percentile && (
              <div className="text-sm text-gray-600">
                Top {percentile}% des participants
              </div>
            )}
          </div>
        )}

        <div className="grid grid-cols-2 gap-4 text-center">
          <div>
            <div className="text-lg font-bold text-yellow-600">
              {formatPoints(total_points)}
            </div>
            <div className="text-xs text-gray-600">Points</div>
          </div>
          <div>
            <div className="text-lg font-bold text-purple-600">
              {level}
            </div>
            <div className="text-xs text-gray-600">Niveau</div>
          </div>
        </div>
      </div>
    </div>
  )
}