/**
 * Analytics Service for La Vida Luca App
 * Handles user event tracking, analytics data collection, and reporting
 */

import { logger } from './logger';
import { cache } from './cache';

export interface AnalyticsEvent {
  id: string;
  name: string;
  properties: Record<string, any>;
  timestamp: number;
  sessionId: string;
  userId?: string;
  userAgent: string;
  url: string;
  referrer: string;
  viewport: {
    width: number;
    height: number;
  };
  deviceInfo: {
    platform: string;
    mobile: boolean;
    language: string;
    timezone: string;
  };
  synced: boolean;
}

export interface UserSession {
  sessionId: string;
  userId?: string;
  startTime: number;
  lastActivity: number;
  pageViews: number;
  events: number;
  duration: number;
  deviceInfo: AnalyticsEvent['deviceInfo'];
  referrer: string;
  utm: {
    source?: string;
    medium?: string;
    campaign?: string;
    term?: string;
    content?: string;
  };
}

export interface AnalyticsConfig {
  enabled: boolean;
  endpoint: string;
  flushInterval: number;
  maxBatchSize: number;
  maxStorageEvents: number;
  enableUserTracking: boolean;
  enablePageTracking: boolean;
  enableErrorTracking: boolean;
}

class AnalyticsService {
  private static instance: AnalyticsService;
  private config: AnalyticsConfig;
  private events: AnalyticsEvent[] = [];
  private currentSession: UserSession | null = null;
  private flushTimer: NodeJS.Timeout | null = null;
  private isOnline = true;

  static getInstance(config?: AnalyticsConfig): AnalyticsService {
    if (!AnalyticsService.instance) {
      if (!config) {
        throw new Error('Analytics configuration required for first initialization');
      }
      AnalyticsService.instance = new AnalyticsService(config);
    }
    return AnalyticsService.instance;
  }

  private constructor(config: AnalyticsConfig) {
    this.config = {
      enabled: true,
      endpoint: '/api/analytics',
      flushInterval: 30000, // 30 seconds
      maxBatchSize: 50,
      maxStorageEvents: 1000,
      enableUserTracking: true,
      enablePageTracking: true,
      enableErrorTracking: true,
      ...config,
    };

    this.initializeAnalytics();
  }

  /**
   * Initialize analytics service
   */
  private async initializeAnalytics(): Promise<void> {
    if (!this.config.enabled) {
      logger.info('Analytics disabled');
      return;
    }

    // Start new session
    this.startSession();

    // Load cached events
    await this.loadCachedEvents();

    // Setup auto-flush
    this.setupAutoFlush();

    // Setup page tracking
    if (this.config.enablePageTracking) {
      this.setupPageTracking();
    }

    // Setup error tracking
    if (this.config.enableErrorTracking) {
      this.setupErrorTracking();
    }

    // Monitor online status
    this.setupOnlineMonitoring();

    logger.info('Analytics service initialized', { sessionId: this.currentSession?.sessionId });
  }

  /**
   * Track an event
   */
  track(name: string, properties: Record<string, any> = {}): void {
    if (!this.config.enabled || !this.currentSession) {
      return;
    }

    const event: AnalyticsEvent = {
      id: crypto.randomUUID(),
      name,
      properties: { ...properties },
      timestamp: Date.now(),
      sessionId: this.currentSession.sessionId,
      userId: this.currentSession.userId,
      userAgent: navigator.userAgent,
      url: window.location.href,
      referrer: document.referrer,
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight,
      },
      deviceInfo: this.getDeviceInfo(),
      synced: false,
    };

    this.events.push(event);
    this.currentSession.events++;
    this.currentSession.lastActivity = Date.now();

    // Cache event for offline persistence
    this.cacheEvent(event);

    logger.debug('Analytics event tracked', { name, properties });

    // Flush if batch size reached
    if (this.events.length >= this.config.maxBatchSize) {
      this.flush();
    }
  }

  /**
   * Track page view
   */
  page(page?: string, properties: Record<string, any> = {}): void {
    if (!this.config.enablePageTracking) {
      return;
    }

    const pageName = page || this.getPageName();
    
    this.track('page_view', {
      page: pageName,
      title: document.title,
      path: window.location.pathname,
      search: window.location.search,
      hash: window.location.hash,
      ...properties,
    });

    if (this.currentSession) {
      this.currentSession.pageViews++;
    }
  }

  /**
   * Identify user
   */
  identify(userId: string, traits: Record<string, any> = {}): void {
    if (!this.config.enableUserTracking) {
      return;
    }

    if (this.currentSession) {
      this.currentSession.userId = userId;
    }

    this.track('user_identified', {
      userId,
      traits,
    });

    logger.info('User identified', { userId });
  }

  /**
   * Track error
   */
  trackError(error: Error | string, context: Record<string, any> = {}): void {
    if (!this.config.enableErrorTracking) {
      return;
    }

    const errorInfo = typeof error === 'string' 
      ? { message: error, stack: '' }
      : { message: error.message, stack: error.stack || '' };

    this.track('error', {
      error: errorInfo,
      context,
      url: window.location.href,
      userAgent: navigator.userAgent,
    });
  }

  /**
   * Track timing event
   */
  timing(name: string, duration: number, properties: Record<string, any> = {}): void {
    this.track('timing', {
      metric: name,
      duration,
      ...properties,
    });
  }

  /**
   * Flush events to server
   */
  async flush(): Promise<void> {
    if (this.events.length === 0 || !this.isOnline) {
      return;
    }

    const eventsToFlush = [...this.events];
    this.events = [];

    try {
      const response = await fetch(this.config.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          events: eventsToFlush,
          session: this.currentSession,
        }),
      });

      if (response.ok) {
        // Mark events as synced and remove from cache
        for (const event of eventsToFlush) {
          event.synced = true;
          await cache.appData.delete(`analytics_event_${event.id}`);
        }
        
        logger.debug('Analytics events flushed successfully', { count: eventsToFlush.length });
      } else {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

    } catch (error) {
      logger.error('Error flushing analytics events', { error });
      
      // Re-add events to queue for retry
      this.events.unshift(...eventsToFlush);
      
      // Cache events for later retry
      for (const event of eventsToFlush) {
        await this.cacheEvent(event);
      }
    }
  }

  /**
   * Sync events (called by periodic sync)
   */
  async syncEvents(): Promise<void> {
    // Load cached events
    await this.loadCachedEvents();
    
    // Flush events
    await this.flush();
  }

  /**
   * Get current session
   */
  getSession(): UserSession | null {
    return this.currentSession ? { ...this.currentSession } : null;
  }

  /**
   * Get analytics statistics
   */
  getStats(): {
    eventsInQueue: number;
    eventsInSession: number;
    sessionDuration: number;
    pageViews: number;
  } {
    return {
      eventsInQueue: this.events.length,
      eventsInSession: this.currentSession?.events || 0,
      sessionDuration: this.currentSession 
        ? Date.now() - this.currentSession.startTime 
        : 0,
      pageViews: this.currentSession?.pageViews || 0,
    };
  }

  /**
   * Update configuration
   */
  updateConfig(updates: Partial<AnalyticsConfig>): void {
    this.config = { ...this.config, ...updates };
    
    // Restart auto-flush if interval changed
    if (updates.flushInterval && this.flushTimer) {
      this.setupAutoFlush();
    }
    
    logger.info('Analytics configuration updated', { config: this.config });
  }

  /**
   * Start new session
   */
  private startSession(): void {
    const sessionId = crypto.randomUUID();
    const now = Date.now();
    
    this.currentSession = {
      sessionId,
      startTime: now,
      lastActivity: now,
      pageViews: 0,
      events: 0,
      duration: 0,
      deviceInfo: this.getDeviceInfo(),
      referrer: document.referrer,
      utm: this.getUtmParameters(),
    };
  }

  /**
   * Get device information
   */
  private getDeviceInfo(): AnalyticsEvent['deviceInfo'] {
    return {
      platform: navigator.platform,
      mobile: /Mobi|Android/i.test(navigator.userAgent),
      language: navigator.language,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    };
  }

  /**
   * Get UTM parameters from URL
   */
  private getUtmParameters(): UserSession['utm'] {
    const params = new URLSearchParams(window.location.search);
    return {
      source: params.get('utm_source') || undefined,
      medium: params.get('utm_medium') || undefined,
      campaign: params.get('utm_campaign') || undefined,
      term: params.get('utm_term') || undefined,
      content: params.get('utm_content') || undefined,
    };
  }

  /**
   * Get page name from URL
   */
  private getPageName(): string {
    const path = window.location.pathname;
    if (path === '/') return 'home';
    return path.replace(/^\//, '').replace(/\//g, '_') || 'unknown';
  }

  /**
   * Cache event for offline persistence
   */
  private async cacheEvent(event: AnalyticsEvent): Promise<void> {
    try {
      await cache.appData.set(`analytics_event_${event.id}`, event, { ttl: 7 * 24 * 60 * 60 * 1000 }); // 7 days
    } catch (error) {
      logger.error('Error caching analytics event', { error });
    }
  }

  /**
   * Load cached events
   */
  private async loadCachedEvents(): Promise<void> {
    try {
      const cachedEvents = await cache.appData.getAll({
        filter: (item) => item.id.startsWith('analytics_event_'),
      }) as AnalyticsEvent[];

      const unSyncedEvents = cachedEvents
        .filter((event: AnalyticsEvent) => !event.synced)
        .slice(0, this.config.maxStorageEvents);

      this.events.unshift(...unSyncedEvents);
      
      logger.debug('Loaded cached analytics events', { count: unSyncedEvents.length });
    } catch (error) {
      logger.error('Error loading cached analytics events', { error });
    }
  }

  /**
   * Setup auto-flush timer
   */
  private setupAutoFlush(): void {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
    }

    this.flushTimer = setInterval(() => {
      this.flush();
    }, this.config.flushInterval);
  }

  /**
   * Setup page tracking
   */
  private setupPageTracking(): void {
    // Track initial page view
    this.page();

    // Track page changes in SPA
    let currentUrl = window.location.href;
    const checkUrlChange = () => {
      if (window.location.href !== currentUrl) {
        currentUrl = window.location.href;
        this.page();
      }
    };

    // Use both popstate and interval checking for SPA navigation
    window.addEventListener('popstate', checkUrlChange);
    setInterval(checkUrlChange, 1000);
  }

  /**
   * Setup error tracking
   */
  private setupErrorTracking(): void {
    // Track JavaScript errors
    window.addEventListener('error', (event) => {
      this.trackError(event.error || event.message, {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
      });
    });

    // Track unhandled promise rejections
    window.addEventListener('unhandledrejection', (event) => {
      this.trackError(event.reason, {
        type: 'unhandled_promise_rejection',
      });
    });
  }

  /**
   * Setup online monitoring
   */
  private setupOnlineMonitoring(): void {
    this.isOnline = navigator.onLine;

    window.addEventListener('online', () => {
      this.isOnline = true;
      this.track('connection_restored');
      // Flush any pending events
      this.flush();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      this.track('connection_lost');
    });
  }
}

// Export singleton instance factory
export const createAnalyticsService = (config: AnalyticsConfig) => {
  return AnalyticsService.getInstance(config);
};

// Export for getting existing instance
export const getAnalyticsService = () => {
  return AnalyticsService.getInstance();
};

// Default instance with basic config
export const analyticsService = AnalyticsService.getInstance({
  enabled: process.env.NODE_ENV === 'production',
  endpoint: '/api/analytics',
  flushInterval: 30000,
  maxBatchSize: 50,
  maxStorageEvents: 1000,
  enableUserTracking: true,
  enablePageTracking: true,
  enableErrorTracking: true,
});