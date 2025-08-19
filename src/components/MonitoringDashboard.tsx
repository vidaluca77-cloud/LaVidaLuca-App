'use client';

import React, { useState, useEffect } from 'react';
import { monitoringDashboard } from '@/monitoring/dashboard';
import { performanceMonitor } from '@/monitoring/performance';
import { alertManager } from '@/monitoring/alerts';

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
    recent: number;
  };
  health: {
    status: 'healthy' | 'warning' | 'critical';
    issues: string[];
  };
}

const formatDuration = (ms: number): string => {
  if (ms < 1000) return `${Math.round(ms)}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
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
    fcp: { good: 1800, poor: 3000 },
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

export const MonitoringDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [isLive, setIsLive] = useState(false);
  const [intervalId, setIntervalId] = useState<NodeJS.Timeout | null>(null);

  const refreshMetrics = () => {
    const currentMetrics = monitoringDashboard.getMetrics();
    setMetrics(currentMetrics);
  };

  const toggleLiveMode = () => {
    if (isLive) {
      // Stop live monitoring
      if (intervalId) {
        monitoringDashboard.stopRealTimeMonitoring(intervalId);
        setIntervalId(null);
      }
      setIsLive(false);
    } else {
      // Start live monitoring
      const id = monitoringDashboard.startRealTimeMonitoring(setMetrics, 30000);
      setIntervalId(id);
      setIsLive(true);
    }
  };

  const clearMetrics = () => {
    performanceMonitor.clearMetrics();
    alertManager.clearAlerts();
    refreshMetrics();
  };

  const exportMetrics = () => {
    const data = monitoringDashboard.exportMetrics();
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `monitoring-metrics-${new Date().toISOString()}.json`;
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
        monitoringDashboard.stopRealTimeMonitoring(intervalId);
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
            <h1 className="text-3xl font-bold text-gray-900">Monitoring Dashboard</h1>
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
              <div className={`w-2 h-2 rounded-full mr-2 ${
                metrics.health.status === 'healthy' ? 'bg-green-400' :
                metrics.health.status === 'warning' ? 'bg-yellow-400' : 'bg-red-400'
              }`}></div>
              Statut: {metrics.health.status === 'healthy' ? 'Sain' : 
                      metrics.health.status === 'warning' ? 'Attention' : 'Critique'}
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
          {/* Page Load Performance */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Temps de chargement</h3>
            <p className="text-3xl font-bold text-blue-600">
              {formatDuration(metrics.performance.avgPageLoad)}
            </p>
            <p className="text-sm text-gray-500 mt-1">Temps moyen de chargement</p>
          </div>

          {/* API Calls */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Appels API</h3>
            <p className="text-3xl font-bold text-purple-600">{metrics.performance.apiCalls.total}</p>
            <div className="text-sm text-gray-500 mt-1">
              <span className="text-green-600">{metrics.performance.apiCalls.successful} réussies</span>
              {metrics.performance.apiCalls.failed > 0 && (
                <span className="text-red-600 ml-2">{metrics.performance.apiCalls.failed} échouées</span>
              )}
            </div>
          </div>

          {/* Alerts */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Alertes</h3>
            <p className="text-3xl font-bold text-orange-600">{metrics.alerts.total}</p>
            <div className="text-sm text-gray-500 mt-1">
              <span className="text-red-600">{metrics.alerts.errors} erreurs</span>
              <span className="text-yellow-600 ml-2">{metrics.alerts.warnings} avertissements</span>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Activité récente</h3>
            <p className="text-3xl font-bold text-indigo-600">{metrics.alerts.recent}</p>
            <p className="text-sm text-gray-500 mt-1">Alertes dernière heure</p>
          </div>
        </div>

        {/* Web Vitals */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Core Web Vitals</h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center">
              <h4 className="text-sm font-medium text-gray-500 mb-2">First Contentful Paint</h4>
              <p className={`text-2xl font-bold ${getWebVitalColor('fcp', metrics.performance.webVitals.fcp)}`}>
                {formatDuration(metrics.performance.webVitals.fcp)}
              </p>
            </div>
            <div className="text-center">
              <h4 className="text-sm font-medium text-gray-500 mb-2">Largest Contentful Paint</h4>
              <p className={`text-2xl font-bold ${getWebVitalColor('lcp', metrics.performance.webVitals.lcp)}`}>
                {formatDuration(metrics.performance.webVitals.lcp)}
              </p>
            </div>
            <div className="text-center">
              <h4 className="text-sm font-medium text-gray-500 mb-2">First Input Delay</h4>
              <p className={`text-2xl font-bold ${getWebVitalColor('fid', metrics.performance.webVitals.fid)}`}>
                {formatDuration(metrics.performance.webVitals.fid)}
              </p>
            </div>
            <div className="text-center">
              <h4 className="text-sm font-medium text-gray-500 mb-2">Cumulative Layout Shift</h4>
              <p className={`text-2xl font-bold ${getWebVitalColor('cls', metrics.performance.webVitals.cls)}`}>
                {metrics.performance.webVitals.cls.toFixed(3)}
              </p>
            </div>
          </div>
        </div>

        {/* API Performance */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Performance API</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center">
              <h4 className="text-sm font-medium text-gray-500 mb-2">Latence moyenne</h4>
              <p className="text-2xl font-bold text-blue-600">
                {formatDuration(metrics.performance.apiCalls.avgLatency)}
              </p>
            </div>
            <div className="text-center">
              <h4 className="text-sm font-medium text-gray-500 mb-2">Taux de succès</h4>
              <p className="text-2xl font-bold text-green-600">
                {metrics.performance.apiCalls.total > 0 
                  ? `${Math.round((metrics.performance.apiCalls.successful / metrics.performance.apiCalls.total) * 100)}%`
                  : 'N/A'
                }
              </p>
            </div>
            <div className="text-center">
              <h4 className="text-sm font-medium text-gray-500 mb-2">Taux d'erreur</h4>
              <p className="text-2xl font-bold text-red-600">
                {metrics.performance.apiCalls.total > 0 
                  ? `${Math.round((metrics.performance.apiCalls.failed / metrics.performance.apiCalls.total) * 100)}%`
                  : 'N/A'
                }
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};