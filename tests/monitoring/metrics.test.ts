import { metrics, businessMetrics, MetricData } from '../../src/monitoring/metrics';

// Mock Sentry
jest.mock('@sentry/nextjs', () => ({
  setMeasurement: jest.fn(),
  addBreadcrumb: jest.fn(),
}));

// Mock performance API
const mockPerformance = {
  now: jest.fn(() => 100),
};

Object.defineProperty(global, 'performance', {
  value: mockPerformance,
  writable: true,
});

describe('MetricsCollector', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    mockPerformance.now.mockReturnValue(100);
  });

  describe('record method', () => {
    it('records a metric with timestamp', () => {
      const metric = {
        name: 'test.metric',
        value: 42,
        unit: 'count',
        tags: { component: 'test' },
      };

      metrics.record(metric);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.metric', 42, 'count');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        category: 'metric',
        message: 'test.metric: 42count',
        level: 'info',
        data: {
          name: 'test.metric',
          value: 42,
          unit: 'count',
          tags: { component: 'test' },
        },
      });
    });

    it('uses default unit when not provided', () => {
      metrics.record({
        name: 'test.metric',
        value: 42,
      });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.metric', 42, 'none');
    });
  });

  describe('increment method', () => {
    it('increments a counter with default value', () => {
      metrics.increment('test.counter');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.counter', 1, 'count');
    });

    it('increments a counter with custom value', () => {
      metrics.increment('test.counter', 5, { component: 'test' });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.counter', 5, 'count');
    });
  });

  describe('timing method', () => {
    it('records timing metrics', () => {
      metrics.timing('test.duration', 250, { endpoint: '/api/test' });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.duration', 250, 'millisecond');
    });
  });

  describe('gauge method', () => {
    it('records gauge metrics', () => {
      metrics.gauge('test.value', 75, 'percent', { service: 'test' });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.value', 75, 'percent');
    });
  });

  describe('timeFunction method', () => {
    it('measures function execution time', () => {
      mockPerformance.now
        .mockReturnValueOnce(100) // start time
        .mockReturnValueOnce(250); // end time

      const testFunction = jest.fn(() => 'result');
      const result = metrics.timeFunction('test.function', testFunction, { component: 'test' });

      expect(result).toBe('result');
      expect(testFunction).toHaveBeenCalled();

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.function', 150, 'millisecond');
    });

    it('measures function execution time even when function throws', () => {
      mockPerformance.now
        .mockReturnValueOnce(100) // start time
        .mockReturnValueOnce(300); // end time

      const testFunction = jest.fn(() => {
        throw new Error('Test error');
      });

      expect(() => {
        metrics.timeFunction('test.function', testFunction);
      }).toThrow('Test error');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.function', 200, 'millisecond');
    });
  });

  describe('timeAsyncFunction method', () => {
    it('measures async function execution time', async () => {
      mockPerformance.now
        .mockReturnValueOnce(100) // start time
        .mockReturnValueOnce(350); // end time

      const asyncFunction = jest.fn(async () => {
        await new Promise(resolve => setTimeout(resolve, 50));
        return 'async result';
      });

      const result = await metrics.timeAsyncFunction('test.async', asyncFunction);

      expect(result).toBe('async result');
      expect(asyncFunction).toHaveBeenCalled();

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('test.async', 250, 'millisecond');
    });
  });
});

describe('businessMetrics', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('trackPageView', () => {
    it('tracks page view without load time', () => {
      businessMetrics.trackPageView('/test-page');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('page.view', 1, 'count');
    });

    it('tracks page view with load time', () => {
      businessMetrics.trackPageView('/test-page', 1500);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('page.view', 1, 'count');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('page.load_time', 1500, 'millisecond');
    });
  });

  describe('trackUserAction', () => {
    it('tracks user action with breadcrumb', () => {
      businessMetrics.trackUserAction('click', 'button', { buttonId: 'submit' });

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('user.action', 1, 'count');
      expect(Sentry.addBreadcrumb).toHaveBeenCalledWith({
        category: 'user',
        message: 'User click',
        level: 'info',
        data: {
          action: 'click',
          component: 'button',
          buttonId: 'submit',
        },
      });
    });
  });

  describe('trackFormInteraction', () => {
    it('tracks form interactions', () => {
      businessMetrics.trackFormInteraction('contact-form', 'complete');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('form.interaction', 1, 'count');
    });
  });

  describe('trackApiCall', () => {
    it('tracks API call metrics', () => {
      businessMetrics.trackApiCall('/api/users', 'GET', 250, 200);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('api.call.duration', 250, 'millisecond');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('api.call', 1, 'count');
    });
  });

  describe('trackContactFormSubmission', () => {
    it('tracks successful form submission', () => {
      businessMetrics.trackContactFormSubmission(true);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('contact.form.submission', 1, 'count');
    });

    it('tracks failed form submission', () => {
      businessMetrics.trackContactFormSubmission(false);

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('contact.form.submission', 1, 'count');
    });
  });

  describe('trackCatalogueView', () => {
    it('tracks catalogue view with category', () => {
      businessMetrics.trackCatalogueView('vegetables');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('catalogue.view', 1, 'count');
    });

    it('tracks catalogue view without category', () => {
      businessMetrics.trackCatalogueView();

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('catalogue.view', 1, 'count');
    });
  });

  describe('trackJoinFormInteraction', () => {
    it('tracks join form step', () => {
      businessMetrics.trackJoinFormInteraction('personal-info');

      const Sentry = require('@sentry/nextjs');
      expect(Sentry.setMeasurement).toHaveBeenCalledWith('join.form.step', 1, 'count');
    });
  });
});