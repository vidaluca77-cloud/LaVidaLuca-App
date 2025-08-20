'use client';

import React, { useState, useEffect } from 'react';
import { enhancedMonitoringDashboard, type EnhancedMetrics } from '@/monitoring/enhanced';
import { performanceMonitor } from '@/monitoring/performance';
import { alertManager } from '@/monitoring/alerts';

const formatDuration = (ms: number): string => {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
};

const formatBytes = (bytes: number): string => {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
};

const getStatusColor = (status: string): string => {
  switch (status) {
    case 'healthy': return 'text-green-600 bg-green-100';
    case 'warning': return 'text-yellow-600 bg-yellow-100';
    case 'critical': return 'text-red-600 bg-red-100';
    default: return 'text-gray-600 bg-gray-100';
  }
};

const getWebVitalColor = (metric: string, value: number): string => {
  const thresholds = {
    fcp: { good: 1500, poor: 2500 },
    lcp: { good: 2500, poor: 4000 },
    fid: { good: 100, poor: 300 },
    cls: { good: 0.1, poor: 0.25 }
  };

  const threshold = thresholds[metric as keyof typeof thresholds];
  if (!threshold) return 'text-gray-600';

  if (value <= threshold.good) return 'text-green-600';
  if (value <= threshold.poor) return 'text-yellow-600';
  return 'text-red-600';
};

const getScoreColor = (score: number): string => {
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  return 'text-red-600';
};

export const EnhancedMonitoringDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<EnhancedMetrics | null>(null);
  const [isLive, setIsLive] = useState(false);
  const [intervalId, setIntervalId] = useState<number | null>(null);

  const refreshMetrics = async () => {
    try {
      const newMetrics = await enhancedMonitoringDashboard.getEnhancedMetrics();
      setMetrics(newMetrics);
    } catch (error) {
      console.error('Failed to get enhanced metrics:', error);
    }
  };

  const toggleLiveMode = () => {
    if (isLive) {
      // Stop live monitoring
      if (intervalId) {
        enhancedMonitoringDashboard.stopRealTimeMonitoring(intervalId);
        setIntervalId(null);
      }
      setIsLive(false);
    } else {
      // Start live monitoring
      const id = enhancedMonitoringDashboard.startEnhancedRealTimeMonitoring(setMetrics, 30000);
      setIntervalId(id);
      setIsLive(true);
    }
  };

  const clearMetrics = () => {
    performanceMonitor.clearMetrics();
    alertManager.clearAlerts();
    enhancedMonitoringDashboard.resetOfflineMetrics();
    refreshMetrics();
  };

  const exportMetrics = async () => {
    const data = await enhancedMonitoringDashboard.exportEnhancedMetrics();
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `enhanced-monitoring-${new Date().toISOString()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  useEffect(() => {
    refreshMetrics();
    
    // Cleanup on unmount
    return () => {
      if (intervalId) {
        enhancedMonitoringDashboard.stopRealTimeMonitoring(intervalId);
      }
    };
  }, []);

  if (!metrics) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-900">Enhanced Monitoring Dashboard</h1>
            <div className="flex space-x-3">
              <button
                onClick={refreshMetrics}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Actualiser
              </button>
              <button
                onClick={toggleLiveMode}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  isLive 
                    ? 'bg-red-600 text-white hover:bg-red-700' 
                    : 'bg-green-600 text-white hover:bg-green-700'
                }`}
              >
                {isLive ? 'Arrêter temps réel' : 'Mode temps réel'}
              </button>
              <button
                onClick={exportMetrics}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                Exporter
              </button>
              <button
                onClick={clearMetrics}
                className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Vider
              </button>
            </div>
          </div>
          
          {/* Health Status */}
          <div className="mt-4">
            <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(metrics.health.status)}`}>
              <span className="w-2 h-2 bg-current rounded-full mr-2"></span>
              {metrics.health.status === 'healthy' ? 'Système sain' : 
               metrics.health.status === 'warning' ? 'Attention requise' : 'Problèmes critiques'}
              <span className={`ml-2 ${getScoreColor(metrics.health.score)}`}>
                ({metrics.health.score}/100)
              </span>
            </div>
            {metrics.health.issues.length > 0 && (
              <div className="mt-2 text-sm text-gray-600">
                Problèmes détectés: {metrics.health.issues.join(', ')}
              </div>
            )}
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Performance Score */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Score de performance</h3>
            <p className={`text-3xl font-bold ${getScoreColor(metrics.health.score)}`}>
              {metrics.health.score}
            </p>
            <p className="text-sm text-gray-500 mt-1">Score global</p>
          </div>

          {/* Offline Status */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Statut de connexion</h3>
            <p className={`text-3xl font-bold ${metrics.offline.isOnline ? 'text-green-600' : 'text-red-600'}`}>
              {metrics.offline.isOnline ? 'En ligne' : 'Hors ligne'}
            </p>
            <p className="text-sm text-gray-500 mt-1">
              {metrics.offline.connectionType} ({metrics.offline.effectiveType})
            </p>
          </div>

          {/* Cache Hit Rate */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Taux de cache</h3>
            <p className="text-3xl font-bold text-purple-600">
              {metrics.offline.cacheHitRate.toFixed(1)}%
            </p>
            <p className="text-sm text-gray-500 mt-1">Efficacité du cache</p>
          </div>

          {/* Queued Actions */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Actions en attente</h3>
            <p className="text-3xl font-bold text-orange-600">
              {metrics.offline.queuedActions}
            </p>
            <p className="text-sm text-gray-500 mt-1">À synchroniser</p>
          </div>
        </div>

        {/* Web Vitals */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Web Vitals</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 p-6">
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">First Contentful Paint</h3>
              <p className={`text-2xl font-bold ${getWebVitalColor('fcp', metrics.performance.webVitals.fcp)}`}>
                {formatDuration(metrics.performance.webVitals.fcp)}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Largest Contentful Paint</h3>
              <p className={`text-2xl font-bold ${getWebVitalColor('lcp', metrics.performance.webVitals.lcp)}`}>
                {formatDuration(metrics.performance.webVitals.lcp)}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">First Input Delay</h3>
              <p className={`text-2xl font-bold ${getWebVitalColor('fid', metrics.performance.webVitals.fid)}`}>
                {formatDuration(metrics.performance.webVitals.fid)}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Cumulative Layout Shift</h3>
              <p className={`text-2xl font-bold ${getWebVitalColor('cls', metrics.performance.webVitals.cls)}`}>
                {metrics.performance.webVitals.cls.toFixed(3)}
              </p>
            </div>
          </div>
        </div>

        {/* API Performance */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Performance API</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 p-6">
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Total</h3>
              <p className="text-2xl font-bold text-blue-600">{metrics.performance.apiCalls.total}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Réussies</h3>
              <p className="text-2xl font-bold text-green-600">{metrics.performance.apiCalls.successful}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Échouées</h3>
              <p className="text-2xl font-bold text-red-600">{metrics.performance.apiCalls.failed}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Depuis le cache</h3>
              <p className="text-2xl font-bold text-purple-600">{metrics.performance.apiCalls.fromCache}</p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Latence moyenne</h3>
              <p className="text-2xl font-bold text-yellow-600">
                {formatDuration(metrics.performance.apiCalls.avgLatency)}
              </p>
            </div>
          </div>
        </div>

        {/* PWA Status */}
        <div className="bg-white rounded-lg shadow mb-8">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Statut PWA</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 p-6">
            <div className="flex items-center space-x-3">
              <div className={`w-3 h-3 rounded-full ${metrics.pwa.isInstalled ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm font-medium">Application installée</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className={`w-3 h-3 rounded-full ${metrics.pwa.serviceWorkerActive ? 'bg-green-500' : 'bg-red-500'}`}></div>
              <span className="text-sm font-medium">Service Worker actif</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className={`w-3 h-3 rounded-full ${metrics.pwa.notificationsEnabled ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
              <span className="text-sm font-medium">Notifications activées</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className={`w-3 h-3 rounded-full ${metrics.pwa.isStandalone ? 'bg-green-500' : 'bg-blue-500'}`}></div>
              <span className="text-sm font-medium">Mode autonome</span>
            </div>
          </div>
        </div>

        {/* Offline Details */}
        <div className="bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900">Détails hors ligne</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Taille du cache</h3>
              <p className="text-lg font-bold text-blue-600">
                {formatBytes(metrics.offline.cachedDataSize)}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Temps hors ligne total</h3>
              <p className="text-lg font-bold text-orange-600">
                {formatDuration(metrics.offline.offlineDuration)}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Dernière synchronisation</h3>
              <p className="text-lg font-bold text-gray-600">
                {metrics.offline.lastSyncTime 
                  ? new Date(metrics.offline.lastSyncTime).toLocaleTimeString()
                  : 'Jamais'
                }
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnhancedMonitoringDashboard;