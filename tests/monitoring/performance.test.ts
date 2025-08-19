/**
 * Test suite for PerformanceMonitor
 */

// Mock performance API
const mockPerformance = {
  now: jest.fn(() => Date.now()),
  getEntries: jest.fn(() => []),
  getEntriesByType: jest.fn(() => []),
  mark: jest.fn(),
  measure: jest.fn(),
};

Object.defineProperty(global, 'performance', {
  value: mockPerformance,
  writable: true,
});

// Mock PerformanceObserver
class MockPerformanceObserver {
  constructor(private callback: Function) {}
  observe() {}
  disconnect() {}
}

Object.defineProperty(global, 'PerformanceObserver', {
  value: MockPerformanceObserver,
  writable: true,
});

import { performanceMonitor } from '../../src/monitoring/performance';

describe('PerformanceMonitor', () => {
  beforeEach(() => {
    performanceMonitor.clearMetrics();
    jest.clearAllMocks();
    
    // Reset mock performance timer
    let time = 0;
    mockPerformance.now.mockImplementation(() => {
      time += 100; // Each call advances by 100ms
      return time;
    });
  });

  test('should record timing metrics', () => {
    performanceMonitor.start('test-operation');
    performanceMonitor.end('test-operation');

    const metrics = performanceMonitor.getMetrics();
    expect(metrics).toHaveLength(1);
    expect(metrics[0].name).toBe('test-operation');
    expect(metrics[0].value).toBe(100); // Based on mock
  });

  test('should handle ending timing without start', () => {
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    
    performanceMonitor.end('non-existent-timer');
    
    expect(consoleSpy).toHaveBeenCalledWith(
      expect.stringContaining("Performance timing 'non-existent-timer' was ended without being started"),
      ""
    );
    
    consoleSpy.mockRestore();
  });

  test('should record direct metrics', () => {
    performanceMonitor.recordMetric('custom-metric', 250, { source: 'test' });

    const metrics = performanceMonitor.getMetrics();
    expect(metrics).toHaveLength(1);
    expect(metrics[0].name).toBe('custom-metric');
    expect(metrics[0].value).toBe(250);
    expect(metrics[0].metadata).toEqual({ source: 'test' });
  });

  test('should filter metrics by name', () => {
    performanceMonitor.recordMetric('metric-a', 100);
    performanceMonitor.recordMetric('metric-b', 200);
    performanceMonitor.recordMetric('metric-a', 150);

    const metricsA = performanceMonitor.getMetricsByName('metric-a');
    expect(metricsA).toHaveLength(2);
    expect(metricsA[0].value).toBe(100);
    expect(metricsA[1].value).toBe(150);
  });

  test('should limit stored metrics', () => {
    // Add more than the limit
    for (let i = 0; i < 1200; i++) {
      performanceMonitor.recordMetric(`metric-${i}`, i);
    }

    const metrics = performanceMonitor.getMetrics();
    expect(metrics.length).toBeLessThanOrEqual(1000);
  });

  test('should wrap fetch calls with monitoring', async () => {
    // Mock fetch
    const mockFetch = jest.fn().mockResolvedValue({
      ok: true,
      status: 200,
    });
    
    Object.defineProperty(global, 'window', {
      value: { fetch: mockFetch },
      writable: true,
    });

    performanceMonitor.wrapFetch();

    // Make a fetch call
    await window.fetch('/api/test', { method: 'POST' });

    // Check that metrics were recorded
    const metrics = performanceMonitor.getMetrics();
    const apiMetrics = metrics.filter(m => m.name === 'api_call');
    
    expect(apiMetrics).toHaveLength(1);
    expect(apiMetrics[0].metadata).toMatchObject({
      url: '/api/test',
      method: 'POST',
      status: 200,
      success: true,
    });
  });

  test('should handle fetch errors', async () => {
    const mockFetch = jest.fn().mockRejectedValue(new Error('Network error'));
    
    Object.defineProperty(global, 'window', {
      value: { fetch: mockFetch },
      writable: true,
    });

    performanceMonitor.wrapFetch();

    try {
      await window.fetch('/api/test');
    } catch (error) {
      // Expected to throw
    }

    const metrics = performanceMonitor.getMetrics();
    const apiMetrics = metrics.filter(m => m.name === 'api_call');
    
    expect(apiMetrics).toHaveLength(1);
    expect(apiMetrics[0].metadata).toMatchObject({
      url: '/api/test',
      method: 'GET',
      error: true,
      errorMessage: 'Network error',
    });
  });

  test('should clear metrics', () => {
    performanceMonitor.recordMetric('test', 100);
    expect(performanceMonitor.getMetrics()).toHaveLength(1);
    
    performanceMonitor.clearMetrics();
    expect(performanceMonitor.getMetrics()).toHaveLength(0);
  });
});