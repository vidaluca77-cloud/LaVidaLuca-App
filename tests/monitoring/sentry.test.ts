import { 
  initSentry, 
  setUser, 
  clearUser, 
  setContext, 
  setTag, 
  setTags, 
  addBreadcrumb, 
  captureException, 
  captureMessage 
} from '../../src/monitoring/sentry';

// Mock Sentry
jest.mock('@sentry/nextjs', () => ({
  init: jest.fn(),
  setUser: jest.fn(),
  setContext: jest.fn(),
  setTag: jest.fn(),
  setTags: jest.fn(),
  addBreadcrumb: jest.fn(),
  captureException: jest.fn(),
  captureMessage: jest.fn(),
  startSpan: jest.fn((config, callback) => callback({ name: config.name, op: config.op })),
}));

describe('Sentry Configuration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('initSentry', () => {
    it('initializes Sentry with comprehensive configuration', () => {
      process.env.NEXT_PUBLIC_SENTRY_DSN = 'https://test@sentry.io/123';
      process.env.NODE_ENV = 'production';
      process.env.NEXT_PUBLIC_APP_VERSION = '1.2.3';

      initSentry();

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.init).toHaveBeenCalledWith({
        dsn: 'https://test@sentry.io/123',
        environment: 'production',
        release: '1.2.3',
        tracesSampleRate: 0.1,
        profilesSampleRate: 0.1,
        replaysSessionSampleRate: 0.1,
        replaysOnErrorSampleRate: 1.0,
        beforeSend: expect.any(Function),
        beforeBreadcrumb: expect.any(Function),
        initialScope: {
          tags: {
            component: "frontend",
            app: "la-vida-luca",
          },
          contexts: {
            app: {
              name: "La Vida Luca",
              version: "1.2.3",
            },
          },
        },
      });
    });

    it('uses different sample rates for development', () => {
      process.env.NODE_ENV = 'development';

      initSentry();

      const Sentry = require('@sentry/nextjs');
      const initCall = Sentry.init.mock.calls[0][0];
      expect(initCall.tracesSampleRate).toBe(1.0);
      expect(initCall.profilesSampleRate).toBe(1.0);
    });

    it('filters out chunk load errors', () => {
      initSentry();

      const Sentry = require('@sentry/nextjs');
      const config = Sentry.init.mock.calls[0][0];
      const beforeSend = config.beforeSend;

      const chunkError = {
        exception: {
          values: [{ type: 'ChunkLoadError' }]
        }
      };

      const hint = { originalException: new Error('Loading chunk failed') };
      hint.originalException.name = 'ChunkLoadError';

      const result = beforeSend(chunkError, hint);
      expect(result).toBeNull();
    });

    it('filters out network errors', () => {
      initSentry();

      const Sentry = require('@sentry/nextjs');
      const config = Sentry.init.mock.calls[0][0];
      const beforeSend = config.beforeSend;

      const event = { exception: { values: [{}] } };
      const hint = { originalException: new Error('NetworkError: Failed to fetch') };

      const result = beforeSend(event, hint);
      expect(result).toBeNull();
    });

    it('allows valid errors through', () => {
      initSentry();

      const Sentry = require('@sentry/nextjs');
      const config = Sentry.init.mock.calls[0][0];
      const beforeSend = config.beforeSend;

      const event = { exception: { values: [{}] } };
      const hint = { originalException: new Error('Valid application error') };

      const result = beforeSend(event, hint);
      expect(result).toBe(event);
    });

    it('enhances navigation breadcrumbs', () => {
      // Mock window object
      Object.defineProperty(global, 'window', {
        value: { navigator: { userAgent: 'test-agent' } },
        writable: true,
      });

      initSentry();

      const Sentry = require('@sentry/nextjs');
      const config = Sentry.init.mock.calls[0][0];
      const beforeBreadcrumb = config.beforeBreadcrumb;

      const breadcrumb = {
        category: 'navigation',
        data: { existing: 'data' }
      };

      const result = beforeBreadcrumb(breadcrumb, {});

      expect(result.data).toEqual({
        existing: 'data',
        timestamp: expect.any(String),
        userAgent: 'test-agent',
      });
    });
  });

  describe('User tracking utilities', () => {
    it('sets user context', () => {
      const user = {
        id: 'user-123',
        email: 'test@example.com',
        username: 'testuser',
        role: 'admin'
      };

      setUser(user);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setUser).toHaveBeenCalledWith({
        id: 'user-123',
        email: 'test@example.com',
        username: 'testuser',
        role: 'admin',
      });
    });

    it('clears user context', () => {
      clearUser();

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setUser).toHaveBeenCalledWith(null);
    });
  });

  describe('Context utilities', () => {
    it('sets custom context', () => {
      const context = { operation: 'test', version: '1.0' };

      setContext('custom', context);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setContext).toHaveBeenCalledWith('custom', context);
    });
  });

  describe('Tag utilities', () => {
    it('sets single tag', () => {
      setTag('environment', 'production');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setTag).toHaveBeenCalledWith('environment', 'production');
    });

    it('sets multiple tags', () => {
      const tags = { environment: 'production', feature: 'monitoring' };

      setTags(tags);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setTags).toHaveBeenCalledWith(tags);
    });
  });

  describe('Breadcrumb utilities', () => {
    it('adds breadcrumb with defaults', () => {
      addBreadcrumb({ message: 'Test breadcrumb' });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        message: 'Test breadcrumb',
        category: 'custom',
        level: 'info',
        data: undefined,
        timestamp: expect.any(Number),
      });
    });

    it('adds breadcrumb with custom properties', () => {
      addBreadcrumb({
        message: 'Custom breadcrumb',
        category: 'user',
        level: 'warning',
        data: { userId: 'user-123' }
      });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        message: 'Custom breadcrumb',
        category: 'user',
        level: 'warning',
        data: { userId: 'user-123' },
        timestamp: expect.any(Number),
      });
    });
  });

  describe('Error capture utilities', () => {
    it('captures exceptions with context', () => {
      const error = new Error('Test error');
      const context = { operation: 'test', userId: 'user-123' };

      captureException(error, context);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureException).toHaveBeenCalledWith(error, {
        contexts: { custom: context },
      });
    });

    it('captures exceptions without context', () => {
      const error = new Error('Test error');

      captureException(error);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureException).toHaveBeenCalledWith(error, {
        contexts: undefined,
      });
    });

    it('captures messages with default level', () => {
      captureMessage('Test message');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureMessage).toHaveBeenCalledWith('Test message', 'info', {
        contexts: undefined,
      });
    });

    it('captures messages with custom level and context', () => {
      const context = { component: 'test' };

      captureMessage('Warning message', 'warning', context);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureMessage).toHaveBeenCalledWith('Warning message', 'warning', {
        contexts: { custom: context },
      });
    });
  });
});