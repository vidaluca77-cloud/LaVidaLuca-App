import React from 'react';
import { motion } from 'framer-motion';
import { Leaderboard, LeaderboardEntry } from '../../types/gamification';

interface LeaderboardProps {
  leaderboard: Leaderboard;
  currentUserId?: string;
  className?: string;
}

const changeIcons = {
  up: '⬆️',
  down: '⬇️', 
  same: '➡️',
  new: '✨'
};

const changeColors = {
  up: 'text-green-600',
  down: 'text-red-600',
  same: 'text-gray-600', 
  new: 'text-blue-600'
};

export default function LeaderboardComponent({ leaderboard, currentUserId, className = '' }: LeaderboardProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border ${className}`}>
      <div className="p-4 border-b">
        <h2 className="text-xl font-bold text-gray-900">🏆 Classement</h2>
        <p className="text-sm text-gray-600 capitalize">Période: {leaderboard.period}</p>
      </div>
      
      <div className="p-4">
        <div className="space-y-3">
          {leaderboard.users.map((user, index) => (
            <LeaderboardEntryComponent 
              key={user.userId}
              user={user}
              isCurrentUser={user.userId === currentUserId}
              index={index}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

interface LeaderboardEntryComponentProps {
  user: LeaderboardEntry;
  isCurrentUser: boolean;
  index: number;
}

function LeaderboardEntryComponent({ user, isCurrentUser, index }: LeaderboardEntryComponentProps) {
  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1: return '🥇';
      case 2: return '🥈';
      case 3: return '🥉';
      default: return `#${rank}`;
    }
  };

  return (
    <motion.div
      className={`
        flex items-center justify-between p-3 rounded-lg border transition-all duration-200
        ${isCurrentUser 
          ? 'bg-blue-50 border-blue-200 shadow-md' 
          : 'bg-gray-50 border-gray-200 hover:bg-gray-100'
        }
      `}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
      whileHover={{ scale: 1.02 }}
    >
      <div className="flex items-center gap-3">
        {/* Rank */}
        <div className={`
          flex items-center justify-center w-8 h-8 rounded-full font-bold text-sm
          ${user.rank <= 3 ? 'bg-yellow-100 text-yellow-800' : 'bg-gray-200 text-gray-700'}
        `}>
          {typeof getRankIcon(user.rank) === 'string' && getRankIcon(user.rank).includes('#') 
            ? getRankIcon(user.rank)
            : <span className="text-lg">{getRankIcon(user.rank)}</span>
          }
        </div>

        {/* User info */}
        <div className="flex items-center gap-2">
          {user.avatar ? (
            <img 
              src={user.avatar} 
              alt={user.username}
              className="w-8 h-8 rounded-full object-cover"
            />
          ) : (
            <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
              <span className="text-gray-600 font-medium">
                {user.username.charAt(0).toUpperCase()}
              </span>
            </div>
          )}
          
          <div>
            <p className={`font-medium ${isCurrentUser ? 'text-blue-900' : 'text-gray-900'}`}>
              {user.username}
              {isCurrentUser && <span className="text-blue-600 ml-1">(Vous)</span>}
            </p>
            <p className="text-xs text-gray-600">
              {user.level.name} • Niveau {user.level.level}
            </p>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-3 text-right">
        {/* Change indicator */}
        <div className={`flex items-center gap-1 ${changeColors[user.change]}`}>
          <span className="text-sm">{changeIcons[user.change]}</span>
        </div>

        {/* Points */}
        <div>
          <p className="font-bold text-lg" style={{ color: user.level.color }}>
            {user.points.toLocaleString()}
          </p>
          <p className="text-xs text-gray-600">points</p>
        </div>
      </div>
    </motion.div>
  );
}