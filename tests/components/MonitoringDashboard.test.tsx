/**
 * Tests for Monitoring Dashboard component
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MonitoringDashboard } from '../../src/components/MonitoringDashboard';

// Mock the monitoring modules
jest.mock('@/monitoring/dashboard', () => ({
  monitoringDashboard: {
    getMetrics: jest.fn(() => ({
      performance: {
        avgPageLoad: 1500,
        webVitals: {
          fcp: 1200,
          lcp: 2000,
          fid: 50,
          cls: 0.05
        },
        apiCalls: {
          total: 100,
          successful: 95,
          failed: 5,
          avgLatency: 250
        }
      },
      alerts: {
        total: 10,
        errors: 2,
        warnings: 3,
        recent: 1
      },
      health: {
        status: 'healthy',
        issues: []
      }
    })),
    startRealTimeMonitoring: jest.fn(() => 123),
    stopRealTimeMonitoring: jest.fn(),
    exportMetrics: jest.fn(() => '{"test": "data"}')
  }
}));

jest.mock('@/monitoring/performance', () => ({
  performanceMonitor: {
    clearMetrics: jest.fn()
  }
}));

jest.mock('@/monitoring/alerts', () => ({
  alertManager: {
    clearAlerts: jest.fn()
  }
}));

describe('MonitoringDashboard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders dashboard with metrics', async () => {
    render(<MonitoringDashboard />);

    await waitFor(() => {
      expect(screen.getByText('Monitoring Dashboard')).toBeInTheDocument();
      expect(screen.getByText('1.50s')).toBeInTheDocument(); // Page load time
      expect(screen.getByText('100')).toBeInTheDocument(); // Total API calls
      expect(screen.getByText('10')).toBeInTheDocument(); // Total alerts
    });
  });

  it('displays health status correctly', async () => {
    render(<MonitoringDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Statut: Sain/)).toBeInTheDocument();
    });
  });

  it('displays web vitals with correct colors', async () => {
    render(<MonitoringDashboard />);

    await waitFor(() => {
      expect(screen.getByText('1.20s')).toBeInTheDocument(); // FCP
      expect(screen.getByText('2.00s')).toBeInTheDocument(); // LCP
      expect(screen.getByText('50ms')).toBeInTheDocument(); // FID
      expect(screen.getByText('0.050')).toBeInTheDocument(); // CLS
    });
  });

  it('shows API performance metrics', async () => {
    render(<MonitoringDashboard />);

    await waitFor(() => {
      expect(screen.getByText('250ms')).toBeInTheDocument(); // Avg latency
      expect(screen.getByText('95%')).toBeInTheDocument(); // Success rate
      expect(screen.getByText('5%')).toBeInTheDocument(); // Error rate
    });
  });

  it('handles refresh button click', async () => {
    const { monitoringDashboard } = require('@/monitoring/dashboard');
    
    render(<MonitoringDashboard />);

    await waitFor(() => {
      const refreshButton = screen.getByText('Actualiser');
      fireEvent.click(refreshButton);
      expect(monitoringDashboard.getMetrics).toHaveBeenCalled();
    });
  });

  it('handles live mode toggle', async () => {
    const { monitoringDashboard } = require('@/monitoring/dashboard');
    
    render(<MonitoringDashboard />);

    await waitFor(() => {
      const liveButton = screen.getByText('Mode temps réel');
      fireEvent.click(liveButton);
      expect(monitoringDashboard.startRealTimeMonitoring).toHaveBeenCalled();
      
      // Button text should change
      expect(screen.getByText('Arrêter temps réel')).toBeInTheDocument();
    });
  });

  it('handles export metrics', async () => {
    const mockCreateObjectURL = jest.fn(() => 'mock-url');
    const mockRevokeObjectURL = jest.fn();
    const mockAppendChild = jest.fn();
    const mockRemoveChild = jest.fn();
    const mockClick = jest.fn();

    Object.defineProperty(window, 'URL', {
      value: {
        createObjectURL: mockCreateObjectURL,
        revokeObjectURL: mockRevokeObjectURL,
      },
    });

    Object.defineProperty(document, 'createElement', {
      value: jest.fn(() => ({
        href: '',
        download: '',
        click: mockClick,
      })),
    });

    Object.defineProperty(document.body, 'appendChild', {
      value: mockAppendChild,
    });

    Object.defineProperty(document.body, 'removeChild', {
      value: mockRemoveChild,
    });

    render(<MonitoringDashboard />);

    await waitFor(() => {
      const exportButton = screen.getByText('Exporter');
      fireEvent.click(exportButton);
      expect(mockCreateObjectURL).toHaveBeenCalled();
    });
  });

  it('handles clear metrics', async () => {
    const { performanceMonitor } = require('@/monitoring/performance');
    const { alertManager } = require('@/monitoring/alerts');
    
    render(<MonitoringDashboard />);

    await waitFor(() => {
      const clearButton = screen.getByText('Vider');
      fireEvent.click(clearButton);
      expect(performanceMonitor.clearMetrics).toHaveBeenCalled();
      expect(alertManager.clearAlerts).toHaveBeenCalled();
    });
  });

  it('shows warning status when there are issues', async () => {
    const { monitoringDashboard } = require('@/monitoring/dashboard');
    
    monitoringDashboard.getMetrics.mockReturnValue({
      performance: {
        avgPageLoad: 1500,
        webVitals: { fcp: 1200, lcp: 2000, fid: 50, cls: 0.05 },
        apiCalls: { total: 100, successful: 95, failed: 5, avgLatency: 250 }
      },
      alerts: { total: 10, errors: 2, warnings: 3, recent: 1 },
      health: {
        status: 'warning',
        issues: ['High error rate detected']
      }
    });

    render(<MonitoringDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Statut: Attention/)).toBeInTheDocument();
      expect(screen.getByText(/High error rate detected/)).toBeInTheDocument();
    });
  });
});