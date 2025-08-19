import React from 'react';
import { CheckCircleIcon, ExclamationTriangleIcon, InformationCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import { cn } from '@/lib/utils';

export interface MessageProps {
  type: 'success' | 'error' | 'warning' | 'info';
  title?: string;
  children: React.ReactNode;
  className?: string;
  onClose?: () => void;
}

const Message = React.forwardRef<HTMLDivElement, MessageProps>(
  ({ type, title, children, className, onClose, ...props }, ref) => {
    const baseClasses = 'rounded-lg border p-4';
    
    const variants = {
      success: 'bg-green-50 border-green-200 text-green-800',
      error: 'bg-red-50 border-red-200 text-red-800',
      warning: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      info: 'bg-blue-50 border-blue-200 text-blue-800'
    };

    const icons = {
      success: CheckCircleIcon,
      error: XCircleIcon,
      warning: ExclamationTriangleIcon,
      info: InformationCircleIcon
    };

    const Icon = icons[type];

    return (
      <div
        ref={ref}
        className={cn(baseClasses, variants[type], className)}
        {...props}
      >
        <div className="flex items-start">
          <Icon className="w-5 h-5 mt-0.5 mr-3 flex-shrink-0" />
          <div className="flex-1">
            {title && (
              <h3 className="font-medium mb-1">{title}</h3>
            )}
            <div className="text-sm">{children}</div>
          </div>
          {onClose && (
            <button
              onClick={onClose}
              className="ml-3 flex-shrink-0 opacity-70 hover:opacity-100 transition-opacity"
            >
              <XCircleIcon className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
    );
  }
);

Message.displayName = 'Message';

export { Message };