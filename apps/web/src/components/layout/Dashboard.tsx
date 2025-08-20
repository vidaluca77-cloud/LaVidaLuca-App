import React from 'react'
import { cn } from '@/lib/utils'

interface DashboardCardProps {
  title: string
  value: string | number
  description?: string
  icon?: React.ReactNode
  trend?: {
    value: number
    isPositive: boolean
    period: string
  }
  color?: 'blue' | 'green' | 'yellow' | 'red' | 'purple'
  className?: string
}

const colorVariants = {
  blue: 'text-blue-600 bg-blue-50 border-blue-200',
  green: 'text-green-600 bg-green-50 border-green-200',
  yellow: 'text-yellow-600 bg-yellow-50 border-yellow-200',
  red: 'text-red-600 bg-red-50 border-red-200',
  purple: 'text-purple-600 bg-purple-50 border-purple-200'
}

export function DashboardCard({
  title,
  value,
  description,
  icon,
  trend,
  color = 'blue',
  className
}: DashboardCardProps) {
  return (
    <div className={cn('bg-white rounded-lg border p-4', className)}>
      <div className="flex items-center justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {description && (
            <p className="text-sm text-gray-500 mt-1">{description}</p>
          )}
          {trend && (
            <div className="flex items-center mt-2">
              <span className={cn(
                'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                trend.isPositive ? 'text-green-800 bg-green-100' : 'text-red-800 bg-red-100'
              )}>
                {trend.isPositive ? '↗' : '↘'} {Math.abs(trend.value)}%
              </span>
              <span className="text-xs text-gray-500 ml-2">
                vs {trend.period}
              </span>
            </div>
          )}
        </div>
        {icon && (
          <div className={cn(
            'p-3 rounded-lg border',
            colorVariants[color]
          )}>
            {icon}
          </div>
        )}
      </div>
    </div>
  )
}

interface QuickActionsProps {
  actions: {
    id: string
    label: string
    description?: string
    icon?: React.ReactNode
    onClick: () => void
    disabled?: boolean
  }[]
  className?: string
}

export function QuickActions({ actions, className }: QuickActionsProps) {
  return (
    <div className={cn('grid gap-3 md:grid-cols-2 lg:grid-cols-4', className)}>
      {actions.map((action) => (
        <button
          key={action.id}
          onClick={action.onClick}
          disabled={action.disabled}
          className={cn(
            'p-4 bg-white rounded-lg border text-left transition-all duration-200',
            'hover:shadow-md hover:border-blue-300 hover:-translate-y-1',
            'disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none disabled:hover:shadow-none'
          )}
        >
          <div className="flex items-start gap-3">
            {action.icon && (
              <div className="text-blue-600 flex-shrink-0">
                {action.icon}
              </div>
            )}
            <div className="flex-1 min-w-0">
              <h3 className="font-medium text-gray-900">{action.label}</h3>
              {action.description && (
                <p className="text-sm text-gray-600 mt-1">{action.description}</p>
              )}
            </div>
          </div>
        </button>
      ))}
    </div>
  )
}

interface RecentActivityProps {
  activities: {
    id: string
    title: string
    description?: string
    timestamp: string
    type: 'achievement' | 'activity' | 'badge' | 'level'
    metadata?: any
  }[]
  className?: string
}

export function RecentActivity({ activities, className }: RecentActivityProps) {
  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'achievement':
        return '🏆'
      case 'activity':
        return '📚'
      case 'badge':
        return '🎖️'
      case 'level':
        return '⬆️'
      default:
        return '📋'
    }
  }

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'achievement':
        return 'text-yellow-600 bg-yellow-50'
      case 'activity':
        return 'text-blue-600 bg-blue-50'
      case 'badge':
        return 'text-purple-600 bg-purple-50'
      case 'level':
        return 'text-green-600 bg-green-50'
      default:
        return 'text-gray-600 bg-gray-50'
    }
  }

  return (
    <div className={cn('bg-white rounded-lg border', className)}>
      <div className="p-4 border-b">
        <h3 className="font-semibold text-gray-900">Activité récente</h3>
      </div>
      
      <div className="divide-y divide-gray-100">
        {activities.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <div className="text-4xl mb-2">📭</div>
            <p>Aucune activité récente</p>
          </div>
        ) : (
          activities.map((activity) => (
            <div key={activity.id} className="p-4 hover:bg-gray-50">
              <div className="flex items-start gap-3">
                <div className={cn(
                  'w-8 h-8 rounded-full flex items-center justify-center text-sm',
                  getActivityColor(activity.type)
                )}>
                  {getActivityIcon(activity.type)}
                </div>
                
                <div className="flex-1 min-w-0">
                  <h4 className="font-medium text-gray-900">{activity.title}</h4>
                  {activity.description && (
                    <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
                  )}
                  <p className="text-xs text-gray-500 mt-2">
                    {new Date(activity.timestamp).toLocaleDateString('fr-FR', {
                      day: 'numeric',
                      month: 'long',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}