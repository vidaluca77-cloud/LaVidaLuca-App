/**
 * Tests for Error Boundary component
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import { ErrorBoundary, withErrorBoundary, useErrorHandler } from '../../src/components/ErrorBoundary';

// Mock Sentry
jest.mock('@sentry/nextjs', () => ({
  withScope: jest.fn((callback) => callback({
    setTag: jest.fn(),
    setContext: jest.fn(),
    setLevel: jest.fn(),
  })),
  captureException: jest.fn(),
}));

// Mock logger
jest.mock('@/lib/logger', () => ({
  logger: {
    error: jest.fn(),
  },
}));

// Component that throws an error
const ThrowError = ({ shouldThrow = false }: { shouldThrow?: boolean }) => {
  if (shouldThrow) {
    throw new Error('Test error');
  }
  return <div>No error</div>;
};

describe('ErrorBoundary', () => {
  beforeEach(() => {
    // Suppress console.error for these tests
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders children when there is no error', () => {
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={false} />
      </ErrorBoundary>
    );

    expect(screen.getByText('No error')).toBeInTheDocument();
  });

  it('renders error UI when there is an error', () => {
    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(screen.getByText('Une erreur s\'est produite')).toBeInTheDocument();
    expect(screen.getByText('Actualiser la page')).toBeInTheDocument();
  });

  it('renders custom fallback when provided', () => {
    const customFallback = <div>Custom error message</div>;

    render(
      <ErrorBoundary fallback={customFallback}>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(screen.getByText('Custom error message')).toBeInTheDocument();
  });

  it('calls onError callback when error occurs', () => {
    const onError = jest.fn();

    render(
      <ErrorBoundary onError={onError}>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(onError).toHaveBeenCalledWith(
      expect.any(Error),
      expect.objectContaining({
        componentStack: expect.any(String),
      })
    );
  });

  it('shows error details in development mode', () => {
    const originalEnv = process.env.NODE_ENV;
    process.env.NODE_ENV = 'development';

    render(
      <ErrorBoundary>
        <ThrowError shouldThrow={true} />
      </ErrorBoundary>
    );

    expect(screen.getByText('Détails de l\'erreur (développement uniquement)')).toBeInTheDocument();

    process.env.NODE_ENV = originalEnv;
  });
});

describe('withErrorBoundary', () => {
  const TestComponent = () => <div>Test Component</div>;
  const WrappedComponent = withErrorBoundary(TestComponent);

  it('wraps component with error boundary', () => {
    render(<WrappedComponent />);
    expect(screen.getByText('Test Component')).toBeInTheDocument();
  });

  it('has correct display name', () => {
    expect(WrappedComponent.displayName).toBe('withErrorBoundary(TestComponent)');
  });
});

describe('useErrorHandler', () => {
  const TestComponent = () => {
    const handleError = useErrorHandler();
    
    const triggerError = () => {
      try {
        handleError(new Error('Manual error'), 'Test context');
      } catch (error) {
        // Error will be caught by error boundary
      }
    };

    return <button onClick={triggerError}>Trigger Error</button>;
  };

  it('handles manual errors correctly', () => {
    const { logger } = require('@/lib/logger');
    
    render(
      <ErrorBoundary>
        <TestComponent />
      </ErrorBoundary>
    );

    expect(logger.error).toHaveBeenCalledWith(
      'Manual error reported',
      expect.objectContaining({
        error: 'Manual error',
        info: 'Test context',
        manual: true,
      })
    );
  });
});