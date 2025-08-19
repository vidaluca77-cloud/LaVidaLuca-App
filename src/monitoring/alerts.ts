import * as Sentry from '@sentry/nextjs';

interface Alert {
  type: 'error' | 'warning' | 'info';
  message: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

interface AlertListener {
  onAlert: (alert: Alert) => void;
}

export class AlertManager {
  private static instance: AlertManager;
  private alerts: Alert[] = [];
  private listeners: AlertListener[] = [];
  private maxAlerts = 100; // Keep only last 100 alerts

  static getInstance(): AlertManager {
    if (!AlertManager.instance) {
      AlertManager.instance = new AlertManager();
    }
    return AlertManager.instance;
  }

  addAlert(
    type: Alert['type'],
    message: string,
    metadata?: Record<string, any>
  ) {
    const alert: Alert = {
      type,
      message,
      timestamp: new Date(),
      metadata,
    };

    // Add to alerts array
    this.alerts.push(alert);

    // Keep only recent alerts
    if (this.alerts.length > this.maxAlerts) {
      this.alerts.shift();
    }

    // Notify listeners
    this.listeners.forEach(listener => listener.onAlert(alert));

    // Send to monitoring services
    this.notify(alert);
  }

  private notify(alert: Alert) {
    // Send to Sentry based on alert type
    switch (alert.type) {
      case 'error':
        Sentry.captureMessage(alert.message, 'error');
        if (alert.metadata) {
          Sentry.setContext('alert_metadata', alert.metadata);
        }
        break;
      case 'warning':
        Sentry.captureMessage(alert.message, 'warning');
        break;
      case 'info':
        // Don't send info alerts to Sentry by default
        break;
    }

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.log(
        `[${alert.type.toUpperCase()}] ${alert.message}`,
        alert.metadata
      );
    }
  }

  getAlerts(): Alert[] {
    return [...this.alerts];
  }

  getAlertsByType(type: Alert['type']): Alert[] {
    return this.alerts.filter(alert => alert.type === type);
  }

  clearAlerts() {
    this.alerts = [];
  }

  subscribe(listener: AlertListener) {
    this.listeners.push(listener);
  }

  unsubscribe(listener: AlertListener) {
    const index = this.listeners.indexOf(listener);
    if (index > -1) {
      this.listeners.splice(index, 1);
    }
  }

  // Convenience methods
  error(message: string, metadata?: Record<string, any>) {
    this.addAlert('error', message, metadata);
  }

  warning(message: string, metadata?: Record<string, any>) {
    this.addAlert('warning', message, metadata);
  }

  info(message: string, metadata?: Record<string, any>) {
    this.addAlert('info', message, metadata);
  }
}

// Export singleton instance
export const alertManager = AlertManager.getInstance();
