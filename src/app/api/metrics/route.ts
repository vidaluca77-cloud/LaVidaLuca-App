import { NextRequest, NextResponse } from 'next/server';
import { logger } from '@/lib/logger';

/**
 * API route for collecting performance metrics and analytics
 */

interface MetricsData {
  type: 'performance' | 'analytics' | 'error' | 'custom';
  timestamp: number;
  sessionId: string;
  userId?: string;
  data: any;
}

// Store metrics in memory (in production, use a proper database)
const metricsStore: MetricsData[] = [];
const MAX_STORED_METRICS = 10000;

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { type, data, sessionId, userId } = body;

    if (!type || !data || !sessionId) {
      return NextResponse.json(
        { error: 'Missing required fields: type, data, sessionId' },
        { status: 400 }
      );
    }

    const metricsEntry: MetricsData = {
      type,
      timestamp: Date.now(),
      sessionId,
      userId,
      data,
    };

    // Store metrics
    metricsStore.push(metricsEntry);

    // Keep only recent metrics
    if (metricsStore.length > MAX_STORED_METRICS) {
      metricsStore.splice(0, metricsStore.length - MAX_STORED_METRICS);
    }

    // Log important metrics
    if (type === 'error') {
      logger.error('Client error reported', { 
        error: data.error, 
        context: data.context,
        sessionId,
        userId 
      });
    } else if (type === 'performance') {
      logger.info('Performance metrics collected', { 
        metrics: data,
        sessionId,
        userId 
      });
    }

    return NextResponse.json({ 
      success: true, 
      message: 'Metrics collected successfully' 
    });

  } catch (error) {
    logger.error('Error collecting metrics', { error });
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const type = searchParams.get('type');
    const sessionId = searchParams.get('sessionId');
    const userId = searchParams.get('userId');
    const limit = parseInt(searchParams.get('limit') || '100');
    const offset = parseInt(searchParams.get('offset') || '0');

    let filteredMetrics = [...metricsStore];

    // Apply filters
    if (type) {
      filteredMetrics = filteredMetrics.filter(m => m.type === type);
    }
    if (sessionId) {
      filteredMetrics = filteredMetrics.filter(m => m.sessionId === sessionId);
    }
    if (userId) {
      filteredMetrics = filteredMetrics.filter(m => m.userId === userId);
    }

    // Sort by timestamp (newest first)
    filteredMetrics.sort((a, b) => b.timestamp - a.timestamp);

    // Apply pagination
    const paginatedMetrics = filteredMetrics.slice(offset, offset + limit);

    // Generate summary statistics
    const summary = generateMetricsSummary(filteredMetrics);

    return NextResponse.json({
      metrics: paginatedMetrics,
      total: filteredMetrics.length,
      summary,
      pagination: {
        limit,
        offset,
        hasMore: offset + limit < filteredMetrics.length,
      },
    });

  } catch (error) {
    logger.error('Error retrieving metrics', { error });
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

/**
 * Generate summary statistics from metrics
 */
function generateMetricsSummary(metrics: MetricsData[]) {
  const summary = {
    totalEvents: metrics.length,
    types: {} as Record<string, number>,
    sessions: new Set(),
    users: new Set(),
    timeRange: {
      oldest: 0,
      newest: 0,
    },
    performance: {
      avgFCP: 0,
      avgLCP: 0,
      avgFID: 0,
      avgCLS: 0,
    },
    errors: {
      total: 0,
      byType: {} as Record<string, number>,
    },
  };

  if (metrics.length === 0) {
    return summary;
  }

  const performanceMetrics: any[] = [];
  const errorMetrics: any[] = [];

  metrics.forEach(metric => {
    // Count by type
    summary.types[metric.type] = (summary.types[metric.type] || 0) + 1;
    
    // Track sessions and users
    summary.sessions.add(metric.sessionId);
    if (metric.userId) {
      summary.users.add(metric.userId);
    }

    // Collect performance metrics
    if (metric.type === 'performance') {
      performanceMetrics.push(metric.data);
    }

    // Collect error metrics
    if (metric.type === 'error') {
      errorMetrics.push(metric.data);
      summary.errors.total++;
      
      const errorType = metric.data.error?.name || 'Unknown';
      summary.errors.byType[errorType] = (summary.errors.byType[errorType] || 0) + 1;
    }
  });

  // Time range
  summary.timeRange.oldest = Math.min(...metrics.map(m => m.timestamp));
  summary.timeRange.newest = Math.max(...metrics.map(m => m.timestamp));

  // Calculate performance averages
  if (performanceMetrics.length > 0) {
    const vitals = performanceMetrics.filter(m => m.fcp || m.lcp || m.fid || m.cls);
    if (vitals.length > 0) {
      summary.performance.avgFCP = calculateAverage(vitals, 'fcp');
      summary.performance.avgLCP = calculateAverage(vitals, 'lcp');
      summary.performance.avgFID = calculateAverage(vitals, 'fid');
      summary.performance.avgCLS = calculateAverage(vitals, 'cls');
    }
  }

  // Convert sets to counts
  (summary as any).sessions = summary.sessions.size;
  (summary as any).users = summary.users.size;

  return summary;
}

function calculateAverage(metrics: any[], field: string): number {
  const values = metrics.map(m => m[field]).filter(v => v !== undefined);
  return values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;
}