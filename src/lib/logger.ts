interface LogEntry {
  timestamp: Date;
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
  metadata?: Record<string, any>;
  component?: string;
}

class Logger {
  private serviceName = 'la-vida-luca-frontend';
  
  private log(level: LogEntry['level'], message: string, metadata?: Record<string, any>, component?: string) {
    const entry: LogEntry = {
      timestamp: new Date(),
      level,
      message,
      metadata,
      component
    };

    // Structured logging in production
    if (process.env.NODE_ENV === 'production') {
      console.log(JSON.stringify({
        service: this.serviceName,
        ...entry,
        timestamp: entry.timestamp.toISOString()
      }));
    } else {
      // Readable logging in development
      const timestamp = entry.timestamp.toISOString();
      const componentStr = component ? `[${component}] ` : '';
      console.log(`${timestamp} [${level.toUpperCase()}] ${componentStr}${message}`, metadata || '');
    }
  }

  debug(message: string, metadata?: Record<string, any>, component?: string) {
    this.log('debug', message, metadata, component);
  }

  info(message: string, metadata?: Record<string, any>, component?: string) {
    this.log('info', message, metadata, component);
  }

  warn(message: string, metadata?: Record<string, any>, component?: string) {
    this.log('warn', message, metadata, component);
  }

  error(message: string, metadata?: Record<string, any>, component?: string) {
    this.log('error', message, metadata, component);
  }

  // Performance logging
  timing(name: string, duration: number, metadata?: Record<string, any>) {
    this.info(`Performance: ${name}`, {
      duration_ms: duration,
      ...metadata
    }, 'performance');
  }

  // User action logging
  userAction(action: string, metadata?: Record<string, any>) {
    this.info(`User action: ${action}`, metadata, 'user');
  }

  // API call logging
  apiCall(url: string, method: string, duration: number, status: number, metadata?: Record<string, any>) {
    this.info(`API call: ${method} ${url}`, {
      duration_ms: duration,
      status_code: status,
      ...metadata
    }, 'api');
  }
}

export const logger = new Logger();