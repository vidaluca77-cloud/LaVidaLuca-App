// src/lib/logger.ts
export enum LogLevel {
  DEBUG = 0,
  INFO = 1,
  WARN = 2,
  ERROR = 3,
}

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  metadata?: Record<string, any>;
  userId?: string;
  sessionId?: string;
}

export class StructuredLogger {
  private static instance: StructuredLogger;
  private sessionId: string;
  private userId?: string;

  private constructor() {
    this.sessionId = this.generateSessionId();
  }

  public static getInstance(): StructuredLogger {
    if (!StructuredLogger.instance) {
      StructuredLogger.instance = new StructuredLogger();
    }
    return StructuredLogger.instance;
  }

  public setUserId(userId: string) {
    this.userId = userId;
  }

  public debug(message: string, metadata?: Record<string, any>) {
    this.log(LogLevel.DEBUG, message, metadata);
  }

  public info(message: string, metadata?: Record<string, any>) {
    this.log(LogLevel.INFO, message, metadata);
  }

  public warn(message: string, metadata?: Record<string, any>) {
    this.log(LogLevel.WARN, message, metadata);
  }

  public error(message: string, error?: Error, metadata?: Record<string, any>) {
    const errorData = error ? {
      name: error.name,
      message: error.message,
      stack: error.stack,
    } : {};

    this.log(LogLevel.ERROR, message, {
      ...metadata,
      error: errorData,
    });
  }

  private log(level: LogLevel, message: string, metadata?: Record<string, any>) {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      metadata,
      userId: this.userId,
      sessionId: this.sessionId,
    };

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      const levelName = LogLevel[level];
      const color = this.getLogColor(level);
      console.log(
        `%c[${levelName}] ${entry.timestamp} - ${message}`,
        `color: ${color}`,
        metadata || ''
      );
    }

    // Send to logging service in production
    if (process.env.NODE_ENV === 'production') {
      this.sendToLoggingService(entry);
    }
  }

  private getLogColor(level: LogLevel): string {
    switch (level) {
      case LogLevel.DEBUG: return '#6b7280';
      case LogLevel.INFO: return '#3b82f6';
      case LogLevel.WARN: return '#f59e0b';
      case LogLevel.ERROR: return '#ef4444';
      default: return '#000000';
    }
  }

  private sendToLoggingService(entry: LogEntry) {
    // En production, envoyer vers un service de logging
    if (typeof window !== 'undefined') {
      fetch('/api/logs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(entry),
        keepalive: true,
      }).catch(() => {
        // Silently fail to avoid affecting user experience
      });
    }
  }

  private generateSessionId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
}

// Export singleton
export const logger = StructuredLogger.getInstance();