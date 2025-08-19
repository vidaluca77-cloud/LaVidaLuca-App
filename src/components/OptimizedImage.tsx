'use client';

import { useLazyLoading } from '@/hooks/useLazyLoading';
import { useState } from 'react';

interface OptimizedImageProps {
  src: string;
  alt: string;
  width?: number;
  height?: number;
  className?: string;
  priority?: boolean;
}

export const OptimizedImage = ({ 
  src, 
  alt, 
  width, 
  height, 
  className = '', 
  priority = false 
}: OptimizedImageProps) => {
  const { ref, isVisible } = useLazyLoading();
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);

  const shouldLoad = priority || isVisible;

  return (
    <div 
      ref={ref} 
      className={`relative overflow-hidden ${className}`}
      style={{ width, height }}
    >
      {shouldLoad && !hasError && (
        <img
          src={src}
          alt={alt}
          width={width}
          height={height}
          className={`transition-opacity duration-300 ${
            isLoaded ? 'opacity-100' : 'opacity-0'
          }`}
          onLoad={() => setIsLoaded(true)}
          onError={() => setHasError(true)}
          loading={priority ? 'eager' : 'lazy'}
        />
      )}
      
      {!isLoaded && !hasError && shouldLoad && (
        <div className="absolute inset-0 bg-gray-200 dark:bg-gray-700 animate-pulse" />
      )}
      
      {hasError && (
        <div className="absolute inset-0 bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
          <span className="text-gray-500 dark:text-gray-400 text-sm">
            Image non disponible
          </span>
        </div>
      )}
    </div>
  );
};