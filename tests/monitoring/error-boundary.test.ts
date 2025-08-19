import { render, screen } from '@testing-library/react';
import ErrorBoundary, { withErrorBoundary, useErrorHandler } from '../../src/components/ErrorBoundary';
import { renderHook } from '@testing-library/react';

// Mock Sentry
jest.mock('@sentry/nextjs', () => ({
  captureException: jest.fn(),
}));

// Component that throws an error for testing
const ThrowError = ({ shouldThrow }: { shouldThrow: boolean }) => {
  if (shouldThrow) {
    throw new Error('Test error');
  }
  return <div>No error</div>;
};

describe('ErrorBoundary', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Suppress console.error during tests
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
    expect(screen.getByText('Recharger la page')).toBeInTheDocument();
    expect(screen.getByText('Retourner en arrière')).toBeInTheDocument();
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

  it('calls onError callback when provided', () => {
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
});

describe('withErrorBoundary HOC', () => {
  it('wraps component with error boundary', () => {
    const TestComponent = () => <div>Test Component</div>;
    const WrappedComponent = withErrorBoundary(TestComponent);

    render(<WrappedComponent />);

    expect(screen.getByText('Test Component')).toBeInTheDocument();
  });

  it('displays error boundary when wrapped component throws', () => {
    const WrappedComponent = withErrorBoundary(ThrowError);

    render(<WrappedComponent shouldThrow={true} />);

    expect(screen.getByText('Une erreur s\'est produite')).toBeInTheDocument();
  });
});

describe('useErrorHandler hook', () => {
  it('provides error reporting function', () => {
    const { result } = renderHook(() => useErrorHandler());

    expect(typeof result.current.reportError).toBe('function');
  });

  it('reports error with context', () => {
    const { result } = renderHook(() => useErrorHandler());
    const error = new Error('Test error');
    const context = { component: 'test' };

    result.current.reportError(error, context);

    // Verify that Sentry.captureException was called
    const Sentry = require('@sentry/nextjs');
    expect(Sentry.captureException).toHaveBeenCalledWith(error, {
      contexts: { custom: context },
      tags: { source: 'manual_report' },
    });
  });
});