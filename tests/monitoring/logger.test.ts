import { logger, logUtils } from '../../src/monitoring/logger';

// Mock Sentry
jest.mock('@sentry/nextjs', () => ({
  captureMessage: jest.fn(),
  captureException: jest.fn(),
  addBreadcrumb: jest.fn(),
  setContext: jest.fn(),
  setUser: jest.fn(),
  setMeasurement: jest.fn(),
  getCurrentHub: jest.fn(() => ({
    getScope: jest.fn(() => ({
      getTransaction: jest.fn(() => ({ traceId: 'trace-123' })),
    })),
  })),
  flush: jest.fn(() => Promise.resolve(true)),
}));

// Mock performance API
const mockPerformance = {
  now: jest.fn(() => 100),
};

Object.defineProperty(global, 'performance', {
  value: mockPerformance,
  writable: true,
});

// Mock console methods
const mockConsole = {
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  debug: jest.fn(),
};

Object.defineProperty(global, 'console', {
  value: mockConsole,
  writable: true,
});

describe('EnhancedLogger', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockPerformance.now.mockReturnValue(100);
  });

  describe('basic logging methods', () => {
    it('logs debug messages', () => {
      logger.debug('Debug message', { key: 'value' }, 'test-component');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        category: 'log',
        message: 'Debug message',
        level: 'debug',
        data: {
          component: 'test-component',
          metadata: { key: 'value' },
          sessionId: expect.any(String),
        },
      });
    });

    it('logs info messages', () => {
      logger.info('Info message', { key: 'value' }, 'test-component');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        category: 'log',
        message: 'Info message',
        level: 'info',
        data: {
          component: 'test-component',
          metadata: { key: 'value' },
          sessionId: expect.any(String),
        },
      });
    });

    it('logs warning messages and sends to Sentry', () => {
      logger.warn('Warning message', { key: 'value' }, 'test-component');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureMessage).toHaveBeenCalledWith('Warning message', 'warning', {
        contexts: {
          log: {
            level: 'warn',
            component: 'test-component',
            sessionId: expect.any(String),
            metadata: { key: 'value' },
          },
        },
        tags: {
          log_level: 'warn',
          component: 'test-component',
        },
      });
    });

    it('logs error messages and sends to Sentry', () => {
      logger.error('Error message', { key: 'value' }, 'test-component');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureMessage).toHaveBeenCalledWith('Error message', 'error', {
        contexts: {
          log: {
            level: 'error',
            component: 'test-component',
            sessionId: expect.any(String),
            metadata: { key: 'value' },
          },
        },
        tags: {
          log_level: 'error',
          component: 'test-component',
        },
      });
    });
  });

  describe('exception method', () => {
    it('captures exceptions with context', () => {
      const error = new Error('Test error');
      const context = { operation: 'test' };

      logger.exception(error, context, 'test-component');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureException).toHaveBeenCalledWith(error, {
        contexts: {
          log: {
            component: 'test-component',
            sessionId: expect.any(String),
            context,
          },
        },
        tags: {
          log_type: 'exception',
          component: 'test-component',
        },
      });
    });
  });

  describe('timing method', () => {
    it('logs performance timing', () => {
      logger.timing({
        name: 'api.call',
        duration: 250,
        metadata: { endpoint: '/api/test' },
        component: 'api',
      });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('api.call', 250, 'millisecond');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        category: 'log',
        message: 'Performance: api.call',
        level: 'info',
        data: {
          component: 'api',
          metadata: {
            duration_ms: 250,
            performance_metric: 'api.call',
            endpoint: '/api/test',
          },
          sessionId: expect.any(String),
        },
      });
    });
  });

  describe('userAction method', () => {
    it('logs user actions with enhanced context', () => {
      // Mock window object
      const mockLocation = { href: 'https://example.com/test' };
      const mockNavigator = { userAgent: 'test-agent' };
      Object.defineProperty(global, 'window', {
        value: { location: mockLocation, navigator: mockNavigator },
        writable: true,
      });

      logger.userAction('click', { button: 'submit' }, 'form');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setContext).toHaveBeenCalledWith('userAction', {
        action: 'click',
        timestamp: expect.any(String),
        button: 'submit',
      });
    });
  });

  describe('apiCall method', () => {
    it('logs successful API calls as info', () => {
      logger.apiCall('/api/users', 'GET', 150, 200, { cached: true });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        category: 'log',
        message: 'API call: GET /api/users',
        level: 'info',
        data: {
          component: 'api',
          metadata: {
            duration_ms: 150,
            status_code: 200,
            method: 'GET',
            url: '/api/users',
            success: true,
            cached: true,
          },
          sessionId: expect.any(String),
        },
      });
    });

    it('logs failed API calls as errors', () => {
      logger.apiCall('/api/users', 'POST', 300, 500, { error: 'server error' });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureMessage).toHaveBeenCalledWith('API call: POST /api/users', 'error', {
        contexts: {
          log: {
            level: 'error',
            component: 'api',
            sessionId: expect.any(String),
            metadata: {
              duration_ms: 300,
              status_code: 500,
              method: 'POST',
              url: '/api/users',
              success: false,
              error: 'server error',
            },
          },
        },
        tags: {
          log_level: 'error',
          component: 'api',
        },
      });
    });
  });

  describe('securityEvent method', () => {
    it('logs security events as warnings', () => {
      logger.securityEvent('unauthorized_access', { ip: '192.168.1.1' }, 'auth');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureMessage).toHaveBeenCalledWith('Security event: unauthorized_access', 'warning', {
        contexts: {
          log: {
            level: 'warn',
            component: 'auth',
            sessionId: expect.any(String),
            metadata: {
              security_event: 'unauthorized_access',
              timestamp: expect.any(Number),
              ip: '192.168.1.1',
            },
          },
        },
        tags: {
          log_level: 'warn',
          component: 'auth',
        },
      });
    });
  });

  describe('user context methods', () => {
    it('sets user context', () => {
      const user = { id: 'user-123', email: 'test@example.com', role: 'admin' };
      logger.setUser(user);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setUser).toHaveBeenCalledWith({
        id: 'user-123',
        email: 'test@example.com',
        role: 'admin',
      });
    });

    it('clears user context', () => {
      logger.clearUser();

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setUser).toHaveBeenCalledWith(null);
    });
  });

  describe('session management', () => {
    it('returns session ID', () => {
      const sessionId = logger.getSessionId();
      expect(sessionId).toMatch(/^session_\d+_[a-z0-9]+$/);
    });

    it('flushes logs', async () => {
      const result = await logger.flush();
      
      const Sentry = require('@sentry/nextjs');
      expect(Sentry.flush).toHaveBeenCalledWith(2000);
      expect(result).toBe(true);
    });
  });
});

describe('logUtils', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockPerformance.now.mockReturnValue(100);
  });

  describe('withPerformanceLogging', () => {
    it('wraps function with performance logging', () => {
      mockPerformance.now
        .mockReturnValueOnce(100) // start
        .mockReturnValueOnce(250); // end

      const originalFn = jest.fn(() => 'result');
      const wrappedFn = logUtils.withPerformanceLogging(originalFn, 'test.function', 'test');

      const result = wrappedFn('arg1', 'arg2');

      expect(result).toBe('result');
      expect(originalFn).toHaveBeenCalledWith('arg1', 'arg2');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.function', 150, 'millisecond');
    });

    it('handles function errors while still logging performance', () => {
      mockPerformance.now
        .mockReturnValueOnce(100) // start
        .mockReturnValueOnce(200); // end

      const originalFn = jest.fn(() => {
        throw new Error('Test error');
      });
      const wrappedFn = logUtils.withPerformanceLogging(originalFn, 'test.function', 'test');

      expect(() => wrappedFn()).toThrow('Test error');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.function', 100, 'millisecond');
    });
  });

  describe('withAsyncPerformanceLogging', () => {
    it('wraps async function with performance logging', async () => {
      mockPerformance.now
        .mockReturnValueOnce(100) // start
        .mockReturnValueOnce(300); // end

      const originalFn = jest.fn(async () => {
        await new Promise(resolve => setTimeout(resolve, 50));
        return 'async result';
      });
      const wrappedFn = logUtils.withAsyncPerformanceLogging(originalFn, 'test.async', 'test');

      const result = await wrappedFn('arg1');

      expect(result).toBe('async result');
      expect(originalFn).toHaveBeenCalledWith('arg1');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.async', 200, 'millisecond');
    });
  });

  describe('createLoggedFetch', () => {
    it('creates fetch wrapper with logging', async () => {
      const mockFetch = jest.fn().mockResolvedValue({
        status: 200,
        headers: { get: jest.fn(() => 'application/json') },
      });
      global.fetch = mockFetch;

      mockPerformance.now
        .mockReturnValueOnce(100) // start
        .mockReturnValueOnce(350); // end

      const loggedFetch = logUtils.createLoggedFetch('https://api.example.com');
      await loggedFetch('/users', { method: 'POST', body: '{"name":"test"}' });

      expect(mockFetch).toHaveBeenCalledWith('https://api.example.com/users', {
        method: 'POST',
        body: '{"name":"test"}',
      });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        category: 'log',
        message: 'API call: POST https://api.example.com/users',
        level: 'info',
        data: {
          component: 'api',
          metadata: {
            duration_ms: 250,
            status_code: 200,
            method: 'POST',
            url: 'https://api.example.com/users',
            success: true,
            requestSize: 15,
            responseType: 'application/json',
          },
          sessionId: expect.any(String),
        },
      });
    });

    it('logs fetch errors', async () => {
      const mockFetch = jest.fn().mockRejectedValue(new Error('Network error'));
      global.fetch = mockFetch;

      mockPerformance.now
        .mockReturnValueOnce(100) // start
        .mockReturnValueOnce(200); // end

      const loggedFetch = logUtils.createLoggedFetch();

      await expect(loggedFetch('/users')).rejects.toThrow('Network error');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.captureMessage).toHaveBeenCalledWith('API call: GET /users', 'error', {
        contexts: {
          log: {
            level: 'error',
            component: 'api',
            sessionId: expect.any(String),
            metadata: {
              duration_ms: 100,
              status_code: 0,
              method: 'GET',
              url: '/users',
              success: false,
              error: 'Network error',
            },
          },
        },
        tags: {
          log_level: 'error',
          component: 'api',
        },
      });
    });
  });
});