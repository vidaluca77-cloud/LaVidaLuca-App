import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
}

/**
 * Reusable Card component
 */
export const Card = ({
  children,
  className = '',
  hover = false,
}: CardProps) => {
  const baseClasses =
    'bg-white rounded-xl shadow-sm border border-gray-100 p-6';
  const hoverClasses = hover ? 'hover:shadow-md transition-shadow' : '';
  const classes = `${baseClasses} ${hoverClasses} ${className}`.trim();

  return <div className={classes}>{children}</div>;
};

interface BadgeProps {
  children: ReactNode;
  variant?: 'green' | 'yellow' | 'red' | 'gray' | 'blue';
  size?: 'sm' | 'md';
}

/**
 * Reusable Badge component
 */
export const Badge = ({
  children,
  variant = 'gray',
  size = 'md',
}: BadgeProps) => {
  const baseClasses = 'rounded-full font-medium';

  const variantClasses = {
    green: 'bg-green-100 text-green-800',
    yellow: 'bg-yellow-100 text-yellow-800',
    red: 'bg-red-100 text-red-800',
    gray: 'bg-gray-100 text-gray-800',
    blue: 'bg-blue-100 text-blue-800',
  };

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
  };

  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`;

  return <span className={classes}>{children}</span>;
};
