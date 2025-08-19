// Utility functions for activities
export const formatDuration = (minutes: number): string => {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  if (hours > 0) {
    return `${hours}h${mins > 0 ? mins.toString().padStart(2, '0') : ''}`;
  }
  return `${mins}min`;
};

export const getSafetyColor = (level: number): string => {
  switch (level) {
    case 1: return 'bg-green-100 text-green-800';
    case 2: return 'bg-yellow-100 text-yellow-800';
    case 3: return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

export const getSafetyText = (level: number): string => {
  switch (level) {
    case 1: return 'Facile';
    case 2: return 'Attention';
    case 3: return 'Expert';
    default: return 'Non défini';
  }
};