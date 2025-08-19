/**
 * Mission card component
 */
import React from 'react';

interface MissionCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  className?: string;
}

/**
 * Card component for displaying mission information
 * @param props Component props
 * @returns JSX element
 */
const MissionCard: React.FC<MissionCardProps> = ({
  icon,
  title,
  description,
  className = '',
}) => {
  return (
    <div className={`text-center p-8 ${className}`}>
      <div className="w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-4">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
};

export default MissionCard;
