import { performanceMonitor } from './performance';
import { alertManager } from './alerts';

interface DashboardMetrics {
  performance: {
    avgPageLoad: number;
    webVitals: {
      fcp: number;
      lcp: number;
      fid: number;
      cls: number;
    };
    apiCalls: {
      total: number;
      successful: number;
      failed: number;
      avgLatency: number;
    };
  };
  alerts: {
    total: number;
    errors: number;
    warnings: number;
    recent: number; // last hour
  };
  health: {
    status: 'healthy' | 'warning' | 'critical';
    issues: string[];
  };
}

export class MonitoringDashboard {
  private static instance: MonitoringDashboard;

  static getInstance(): MonitoringDashboard {
    if (!MonitoringDashboard.instance) {
      MonitoringDashboard.instance = new MonitoringDashboard();
    }
    return MonitoringDashboard.instance;
  }

  getMetrics(): DashboardMetrics {
    const metrics = performanceMonitor.getMetrics();
    const alerts = alertManager.getAlerts();
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);

    // Calculate performance metrics
    const webVitalMetrics = metrics.filter(m => m.metadata?.type === 'web-vital');
    const apiMetrics = metrics.filter(m => m.name === 'api_call');
    
    const webVitals = {
      fcp: this.getLatestMetricValue(webVitalMetrics, 'fcp') || 0,
      lcp: this.getLatestMetricValue(webVitalMetrics, 'lcp') || 0,
      fid: this.getLatestMetricValue(webVitalMetrics, 'fid') || 0,
      cls: this.getLatestMetricValue(webVitalMetrics, 'cls') || 0,
    };

    const successfulAPICalls = apiMetrics.filter(m => !m.metadata?.error);
    const failedAPICalls = apiMetrics.filter(m => m.metadata?.error);
    const avgApiLatency = apiMetrics.length > 0 
      ? apiMetrics.reduce((sum, m) => sum + m.value, 0) / apiMetrics.length 
      : 0;

    // Calculate alert metrics
    const recentAlerts = alerts.filter(alert => alert.timestamp > oneHourAgo);
    const errorAlerts = alerts.filter(alert => alert.type === 'error');
    const warningAlerts = alerts.filter(alert => alert.type === 'warning');

    // Determine health status
    const health = this.calculateHealthStatus(webVitals, errorAlerts.length, failedAPICalls.length);

    return {
      performance: {
        avgPageLoad: this.getAveragePageLoadTime(),
        webVitals,
        apiCalls: {
          total: apiMetrics.length,
          successful: successfulAPICalls.length,
          failed: failedAPICalls.length,
          avgLatency: avgApiLatency,
        },
      },
      alerts: {
        total: alerts.length,
        errors: errorAlerts.length,
        warnings: warningAlerts.length,
        recent: recentAlerts.length,
      },
      health,
    };
  }

  private getLatestMetricValue(metrics: any[], name: string): number | null {
    const filtered = metrics.filter(m => m.name === name);
    if (filtered.length === 0) return null;
    return filtered[filtered.length - 1].value;
  }

  private getAveragePageLoadTime(): number {
    if (typeof window === 'undefined') return 0;
    
    try {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      if (navigation.loadEventEnd && navigation.fetchStart) {
        return navigation.loadEventEnd - navigation.fetchStart;
      }
      return 0;
    } catch {
      return 0;
    }
  }

  private calculateHealthStatus(
    webVitals: any, 
    errorCount: number, 
    failedAPICount: number
  ): { status: 'healthy' | 'warning' | 'critical'; issues: string[] } {
    const issues: string[] = [];
    let status: 'healthy' | 'warning' | 'critical' = 'healthy';

    // Check Web Vitals
    if (webVitals.fcp > 1500) {
      issues.push('First Contentful Paint is slow');
      status = 'warning';
    }
    if (webVitals.lcp > 2500) {
      issues.push('Largest Contentful Paint is slow');
      status = 'warning';
    }
    if (webVitals.fid > 100) {
      issues.push('First Input Delay is high');
      status = 'warning';
    }
    if (webVitals.cls > 0.1) {
      issues.push('Cumulative Layout Shift is high');
      status = 'warning';
    }

    // Check error rates
    if (errorCount > 10) {
      issues.push('High error rate detected');
      status = status === 'healthy' ? 'warning' : 'critical';
    }
    if (failedAPICount > 5) {
      issues.push('Multiple API failures detected');
      status = status === 'healthy' ? 'warning' : 'critical';
    }

    return { status, issues };
  }

  exportMetrics(): string {
    const metrics = this.getMetrics();
    return JSON.stringify(metrics, null, 2);
  }

  // Real-time monitoring
  startRealTimeMonitoring(callback: (metrics: DashboardMetrics) => void, interval: number = 30000) {
    return setInterval(() => {
      callback(this.getMetrics());
    }, interval);
  }

  stopRealTimeMonitoring(intervalId: NodeJS.Timeout) {
    clearInterval(intervalId);
  }
}

export const monitoringDashboard = MonitoringDashboard.getInstance();