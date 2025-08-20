/**
 * Offline Fallback Component
 * Displayed when content cannot be loaded due to network issues
 */

'use client';

import React from 'react';
import { ExclamationTriangleIcon, ArrowPathIcon, WifiIcon } from '@heroicons/react/24/outline';

interface OfflineFallbackProps {
  title?: string;
  message?: string;
  showRetry?: boolean;
  onRetry?: () => void;
  className?: string;
}

export const OfflineFallback: React.FC<OfflineFallbackProps> = ({
  title = 'Contenu non disponible',
  message = 'Ce contenu n\'est pas disponible hors ligne. Vérifiez votre connexion internet et réessayez.',
  showRetry = true,
  onRetry,
  className = ''
}) => {
  const handleRetry = () => {
    if (onRetry) {
      onRetry();
    } else {
      // Default retry behavior - reload the page
      window.location.reload();
    }
  };

  return (
    <div className={`flex flex-col items-center justify-center p-8 text-center ${className}`}>
      <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
        <WifiIcon className="h-8 w-8 text-gray-400" />
      </div>
      
      <h3 className="text-lg font-medium text-gray-900 mb-2">
        {title}
      </h3>
      
      <p className="text-sm text-gray-600 mb-6 max-w-md">
        {message}
      </p>
      
      {showRetry && (
        <button
          onClick={handleRetry}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
        >
          <ArrowPathIcon className="h-4 w-4 mr-2" />
          Réessayer
        </button>
      )}
      
      <div className="mt-6 text-xs text-gray-500">
        <p>💡 Astuce: Certains contenus peuvent être disponibles hors ligne après votre première visite.</p>
      </div>
    </div>
  );
};

/**
 * Network Error Boundary for offline scenarios
 */
interface OfflineErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<OfflineFallbackProps>;
  title?: string;
  message?: string;
}

interface OfflineErrorBoundaryState {
  hasError: boolean;
  isNetworkError: boolean;
}

export class OfflineErrorBoundary extends React.Component<
  OfflineErrorBoundaryProps,
  OfflineErrorBoundaryState
> {
  constructor(props: OfflineErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, isNetworkError: false };
  }

  static getDerivedStateFromError(error: Error): OfflineErrorBoundaryState {
    // Check if this is a network-related error
    const isNetworkError = 
      error.message.includes('fetch') ||
      error.message.includes('network') ||
      error.message.includes('Failed to load') ||
      !navigator.onLine;

    return { hasError: true, isNetworkError };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('OfflineErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || OfflineFallback;
      
      if (this.state.isNetworkError) {
        return (
          <FallbackComponent
            title={this.props.title}
            message={this.props.message}
            onRetry={() => {
              this.setState({ hasError: false, isNetworkError: false });
            }}
          />
        );
      }
      
      // For non-network errors, show generic error
      return (
        <div className="flex flex-col items-center justify-center p-8 text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mb-4">
            <ExclamationTriangleIcon className="h-8 w-8 text-red-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Une erreur s'est produite
          </h3>
          <p className="text-sm text-gray-600 mb-6 max-w-md">
            Une erreur inattendue s'est produite. Veuillez actualiser la page et réessayer.
          </p>
          <button
            onClick={() => window.location.reload()}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            <ArrowPathIcon className="h-4 w-4 mr-2" />
            Actualiser la page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default OfflineFallback;