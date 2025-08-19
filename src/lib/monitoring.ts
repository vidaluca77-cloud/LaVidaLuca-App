// src/lib/monitoring.ts
export class PerformanceMonitor {
  private static instance: PerformanceMonitor;
  
  public static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor();
    }
    return PerformanceMonitor.instance;
  }

  /**
   * Mesure le temps d'exécution d'une fonction
   */
  public async measureAsync<T>(
    name: string,
    fn: () => Promise<T>,
    metadata?: Record<string, any>
  ): Promise<T> {
    const startTime = performance.now();
    
    try {
      const result = await fn();
      const duration = performance.now() - startTime;
      
      this.recordMetric('performance', {
        name,
        duration,
        status: 'success',
        ...metadata
      });
      
      return result;
    } catch (error) {
      const duration = performance.now() - startTime;
      
      this.recordMetric('performance', {
        name,
        duration,
        status: 'error',
        error: error instanceof Error ? error.message : 'Unknown error',
        ...metadata
      });
      
      throw error;
    }
  }

  /**
   * Enregistre une métrique business
   */
  public recordBusinessMetric(event: string, properties?: Record<string, any>) {
    this.recordMetric('business', {
      event,
      timestamp: new Date().toISOString(),
      ...properties
    });
  }

  /**
   * Enregistre une métrique système
   */
  private recordMetric(type: string, data: Record<string, any>) {
    // En développement, log dans la console
    if (process.env.NODE_ENV === 'development') {
      console.log(`[${type.toUpperCase()}]`, data);
    }

    // En production, envoyer vers un service de monitoring
    if (typeof window !== 'undefined' && 'navigator' in window) {
      // Utilise Navigator Beacon API pour l'envoi fiable
      const payload = JSON.stringify({ type, ...data });
      
      if ('sendBeacon' in navigator) {
        navigator.sendBeacon('/api/metrics', payload);
      } else {
        // Fallback pour les navigateurs plus anciens
        fetch('/api/metrics', {
          method: 'POST',
          body: payload,
          headers: { 'Content-Type': 'application/json' },
          keepalive: true
        }).catch(() => {
          // Ignore les erreurs d'envoi de métiques pour ne pas affecter l'UX
        });
      }
    }
  }
}

// Utilitaires pour les métriques Web Vitals
export function reportWebVitals(metric: any) {
  const monitor = PerformanceMonitor.getInstance();
  
  monitor.recordBusinessMetric('web_vital', {
    name: metric.name,
    value: metric.value,
    delta: metric.delta,
    id: metric.id,
    rating: metric.rating
  });
}

// Export singleton
export const performanceMonitor = PerformanceMonitor.getInstance();