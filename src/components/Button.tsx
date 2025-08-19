/**
 * Button component for La Vida Luca App
 */
import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  className?: string;
  type?: 'button' | 'submit' | 'reset';
}

/**
 * Reusable button component with different variants and sizes
 * @param props Component props
 * @returns JSX element
 */
const Button: React.FC<ButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  disabled = false,
  className = '',
  type = 'button',
}) => {
  const baseClasses =
    'font-medium rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';

  const variantClasses = {
    primary: 'bg-green-500 text-white hover:bg-green-600 focus:ring-green-500',
    secondary:
      'bg-gray-300 text-gray-700 hover:bg-gray-400 focus:ring-gray-500',
    outline:
      'bg-white text-green-500 border-2 border-green-500 hover:bg-green-50 focus:ring-green-500',
  };

  const sizeClasses = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3',
    lg: 'px-8 py-4',
  };

  const disabledClasses = disabled ? 'opacity-50 cursor-not-allowed' : '';

  const finalClasses = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabledClasses} ${className}`;

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={finalClasses}
    >
      {children}
    </button>
  );
};

export default Button;
