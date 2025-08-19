/**
 * Test suite for AlertManager monitoring component
 */

// Mock Sentry for testing
const mockSentry = {
  captureMessage: jest.fn(),
  setContext: jest.fn(),
};

jest.mock('@sentry/nextjs', () => mockSentry);

import { AlertManager } from '../../src/monitoring/alerts';

describe('AlertManager', () => {
  let alertManager: AlertManager;

  beforeEach(() => {
    alertManager = AlertManager.getInstance();
    alertManager.clearAlerts();
    jest.clearAllMocks();
  });

  test('should create singleton instance', () => {
    const instance1 = AlertManager.getInstance();
    const instance2 = AlertManager.getInstance();
    expect(instance1).toBe(instance2);
  });

  test('should add and retrieve alerts', () => {
    alertManager.addAlert('info', 'Test message');
    const alerts = alertManager.getAlerts();

    expect(alerts).toHaveLength(1);
    expect(alerts[0].type).toBe('info');
    expect(alerts[0].message).toBe('Test message');
    expect(alerts[0].timestamp).toBeInstanceOf(Date);
  });

  test('should filter alerts by type', () => {
    alertManager.addAlert('error', 'Error message');
    alertManager.addAlert('warning', 'Warning message');
    alertManager.addAlert('info', 'Info message');

    const errorAlerts = alertManager.getAlertsByType('error');
    const warningAlerts = alertManager.getAlertsByType('warning');

    expect(errorAlerts).toHaveLength(1);
    expect(errorAlerts[0].type).toBe('error');
    expect(warningAlerts).toHaveLength(1);
    expect(warningAlerts[0].type).toBe('warning');
  });

  test('should send error alerts to Sentry', () => {
    alertManager.addAlert('error', 'Critical error', { userId: '123' });

    expect(mockSentry.captureMessage).toHaveBeenCalledWith(
      'Critical error',
      'error'
    );
    expect(mockSentry.setContext).toHaveBeenCalledWith('alert_metadata', {
      userId: '123',
    });
  });

  test('should not send info alerts to Sentry', () => {
    alertManager.addAlert('info', 'Info message');

    expect(mockSentry.captureMessage).not.toHaveBeenCalled();
  });

  test('should limit number of stored alerts', () => {
    // Add more than the max limit
    for (let i = 0; i < 150; i++) {
      alertManager.addAlert('info', `Message ${i}`);
    }

    const alerts = alertManager.getAlerts();
    expect(alerts.length).toBeLessThanOrEqual(100);
  });

  test('should notify listeners when alert is added', () => {
    const mockListener = {
      onAlert: jest.fn(),
    };

    alertManager.subscribe(mockListener);
    alertManager.addAlert('warning', 'Test warning');

    expect(mockListener.onAlert).toHaveBeenCalledWith(
      expect.objectContaining({
        type: 'warning',
        message: 'Test warning',
      })
    );
  });

  test('should provide convenience methods', () => {
    alertManager.error('Error message');
    alertManager.warning('Warning message');
    alertManager.info('Info message');

    const alerts = alertManager.getAlerts();
    expect(alerts).toHaveLength(3);
    expect(alerts[0].type).toBe('error');
    expect(alerts[1].type).toBe('warning');
    expect(alerts[2].type).toBe('info');
  });

  test('should clear all alerts', () => {
    alertManager.addAlert('info', 'Test 1');
    alertManager.addAlert('error', 'Test 2');

    expect(alertManager.getAlerts()).toHaveLength(2);

    alertManager.clearAlerts();
    expect(alertManager.getAlerts()).toHaveLength(0);
  });
});
