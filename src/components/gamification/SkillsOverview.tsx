/**
 * Skills Overview Component
 * Displays user skills with progress and levels
 */

import React from 'react';
import { SkillProgress } from '@/lib/gamification/types';
import { 
  AcademicCapIcon,
  ChartBarIcon,
  TrophyIcon,
  ClockIcon,
  StarIcon
} from '@heroicons/react/24/outline';
import { StarIcon as StarSolidIcon } from '@heroicons/react/24/solid';

interface SkillsOverviewProps {
  skills: SkillProgress[];
  className?: string;
  maxSkillsDisplay?: number;
  showDetails?: boolean;
}

// Skill metadata for display
const SKILL_METADATA = {
  elevage: { name: 'Élevage', icon: '🐑', color: 'text-green-600', bg: 'bg-green-50' },
  jardinage: { name: 'Jardinage', icon: '🌱', color: 'text-green-600', bg: 'bg-green-50' },
  hygiene: { name: 'Hygiène', icon: '🧼', color: 'text-blue-600', bg: 'bg-blue-50' },
  precision: { name: 'Précision', icon: '🎯', color: 'text-purple-600', bg: 'bg-purple-50' },
  bois: { name: 'Travail du bois', icon: '🪵', color: 'text-orange-600', bg: 'bg-orange-50' },
  securite: { name: 'Sécurité', icon: '🛡️', color: 'text-red-600', bg: 'bg-red-50' },
  accueil: { name: 'Accueil', icon: '👋', color: 'text-pink-600', bg: 'bg-pink-50' },
  organisation: { name: 'Organisation', icon: '📋', color: 'text-indigo-600', bg: 'bg-indigo-50' },
  contact: { name: 'Contact', icon: '💬', color: 'text-cyan-600', bg: 'bg-cyan-50' },
  responsabilite: { name: 'Responsabilité', icon: '🎓', color: 'text-gray-600', bg: 'bg-gray-50' },
  pedagogie: { name: 'Pédagogie', icon: '📚', color: 'text-yellow-600', bg: 'bg-yellow-50' },
  compter_simple: { name: 'Calcul simple', icon: '🔢', color: 'text-blue-600', bg: 'bg-blue-50' },
  equipe: { name: 'Travail d\'équipe', icon: '👥', color: 'text-teal-600', bg: 'bg-teal-50' },
  conservation: { name: 'Conservation', icon: '🥫', color: 'text-orange-600', bg: 'bg-orange-50' }
};

const SkillsOverview: React.FC<SkillsOverviewProps> = ({
  skills,
  className = '',
  maxSkillsDisplay = 6,
  showDetails = true
}) => {
  // Sort skills by level and experience
  const sortedSkills = [...skills].sort((a, b) => {
    if (a.level !== b.level) {
      return b.level - a.level;
    }
    return b.experience - a.experience;
  });

  // Get top skills to display
  const displayedSkills = sortedSkills.slice(0, maxSkillsDisplay);
  const remainingSkills = sortedSkills.length - maxSkillsDisplay;

  // Calculate skill level from experience (every 100 XP = 1 level)
  const calculateSkillLevel = (experience: number) => {
    return Math.floor(experience / 100) + 1;
  };

  // Calculate progress to next level
  const calculateProgress = (experience: number) => {
    const currentLevelXP = experience % 100;
    return (currentLevelXP / 100) * 100;
  };

  // Get skill metadata or default
  const getSkillMetadata = (skillId: string) => {
    return SKILL_METADATA[skillId as keyof typeof SKILL_METADATA] || {
      name: skillId.charAt(0).toUpperCase() + skillId.slice(1),
      icon: '🔧',
      color: 'text-gray-600',
      bg: 'bg-gray-50'
    };
  };

  // Render skill stars (max 5)
  const renderSkillStars = (level: number) => {
    const maxStars = 5;
    const filledStars = Math.min(level, maxStars);
    const emptyStars = maxStars - filledStars;

    return (
      <div className="flex items-center gap-0.5">
        {[...Array(filledStars)].map((_, i) => (
          <StarSolidIcon key={`filled-${i}`} className="w-3 h-3 text-yellow-400" />
        ))}
        {[...Array(emptyStars)].map((_, i) => (
          <StarIcon key={`empty-${i}`} className="w-3 h-3 text-gray-300" />
        ))}
        {level > maxStars && (
          <span className="text-xs font-bold text-yellow-600 ml-1">
            +{level - maxStars}
          </span>
        )}
      </div>
    );
  };

  if (skills.length === 0) {
    return (
      <div className={`
        p-6 rounded-lg border-2 border-dashed border-gray-300 text-center ${className}
      `}>
        <AcademicCapIcon className="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Aucune compétence développée
        </h3>
        <p className="text-gray-600">
          Commencez des activités pour développer vos compétences !
        </p>
      </div>
    );
  }

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <AcademicCapIcon className="w-5 h-5 text-blue-600" />
          <h3 className="text-lg font-semibold text-gray-900">
            Mes Compétences
          </h3>
        </div>
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <ChartBarIcon className="w-4 h-4" />
          <span>{skills.length} compétence{skills.length > 1 ? 's' : ''}</span>
        </div>
      </div>

      {/* Skills Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {displayedSkills.map((skill) => {
          const metadata = getSkillMetadata(skill.skillId);
          const currentLevel = calculateSkillLevel(skill.experience);
          const progress = calculateProgress(skill.experience);
          const nextLevelXP = 100 - (skill.experience % 100);

          return (
            <div
              key={skill.skillId}
              className={`
                p-4 rounded-lg border-2 border-gray-200 ${metadata.bg}
                hover:border-gray-300 transition-colors
              `}
            >
              {/* Skill Header */}
              <div className="flex items-center gap-3 mb-3">
                <div className="text-2xl">{metadata.icon}</div>
                <div className="flex-1">
                  <h4 className="font-medium text-gray-900">
                    {metadata.name}
                  </h4>
                  <div className="flex items-center gap-2">
                    {renderSkillStars(currentLevel)}
                    <span className={`text-sm font-medium ${metadata.color}`}>
                      Niveau {currentLevel}
                    </span>
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mb-3">
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs text-gray-600">Progression</span>
                  <span className="text-xs font-medium text-gray-900">
                    {skill.experience} XP
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full transition-all duration-300 ${metadata.color.replace('text-', 'bg-')}`}
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  {nextLevelXP} XP pour le niveau {currentLevel + 1}
                </p>
              </div>

              {/* Skill Stats */}
              {showDetails && (
                <div className="grid grid-cols-2 gap-3 text-xs">
                  <div className="flex items-center gap-1">
                    <TrophyIcon className="w-3 h-3 text-gray-400" />
                    <span className="text-gray-600">
                      {skill.totalActivities} activité{skill.totalActivities > 1 ? 's' : ''}
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <ClockIcon className="w-3 h-3 text-gray-400" />
                    <span className="text-gray-600">
                      {skill.lastActivity ? (
                        <>Il y a {Math.floor((Date.now() - new Date(skill.lastActivity).getTime()) / (1000 * 60 * 60 * 24))} j</>
                      ) : (
                        'Jamais pratiqué'
                      )}
                    </span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Show More Skills */}
      {remainingSkills > 0 && (
        <div className="text-center">
          <button className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors">
            <AcademicCapIcon className="w-4 h-4" />
            Voir {remainingSkills} compétence{remainingSkills > 1 ? 's' : ''} de plus
          </button>
        </div>
      )}

      {/* Skills Summary */}
      {skills.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h4 className="font-medium text-gray-900 mb-2">Résumé des compétences</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-blue-600">
                {skills.reduce((acc, skill) => acc + calculateSkillLevel(skill.experience), 0)}
              </p>
              <p className="text-xs text-gray-600">Niveaux totaux</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-green-600">
                {skills.reduce((acc, skill) => acc + skill.experience, 0)}
              </p>
              <p className="text-xs text-gray-600">XP total</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-purple-600">
                {skills.reduce((acc, skill) => acc + skill.totalActivities, 0)}
              </p>
              <p className="text-xs text-gray-600">Activités</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-orange-600">
                {skills.filter(skill => calculateSkillLevel(skill.experience) >= 5).length}
              </p>
              <p className="text-xs text-gray-600">Maîtrisées</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SkillsOverview;