'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useSync } from '@/hooks/useSync';
import { cache } from '@/lib/cache';
import { logger } from '@/lib/logger';

interface SyncedContentProps<T> {
  storeName: string;
  itemId: string;
  fallbackContent?: React.ReactNode;
  loadingContent?: React.ReactNode;
  errorContent?: React.ReactNode;
  children: (data: T | null, isLoading: boolean, error: string | null) => React.ReactNode;
  onDataChange?: (data: T | null) => void;
  refreshInterval?: number;
  ttl?: number; // Cache time-to-live in milliseconds
}

/**
 * Component that automatically syncs and caches content from remote sources
 */
export function SyncedContent<T>({
  storeName,
  itemId,
  fallbackContent = null,
  loadingContent = <div className="animate-pulse bg-gray-200 h-4 w-3/4 rounded"></div>,
  errorContent = <div className="text-red-500 text-sm">Erreur de chargement</div>,
  children,
  onDataChange,
  refreshInterval = 30000, // 30 seconds
  ttl = 300000, // 5 minutes
}: SyncedContentProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const { isOnline, queueChange } = useSync();

  // Load data from cache or fetch from API
  const loadData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      // First, try to get from cache
      const cachedData = await cache[storeName as keyof typeof cache]?.get(itemId);
      
      if (cachedData) {
        setData(cachedData);
        setIsLoading(false);
        
        if (onDataChange) {
          onDataChange(cachedData);
        }
      }

      // If online, try to fetch fresh data
      if (isOnline) {
        try {
          const response = await fetch(`/api/${storeName}/${itemId}`);
          
          if (response.ok) {
            const freshData = await response.json();
            
            // Update cache
            await cache[storeName as keyof typeof cache]?.set(itemId, freshData, { ttl });
            
            // Update state if data changed
            if (JSON.stringify(freshData) !== JSON.stringify(cachedData)) {
              setData(freshData);
              
              if (onDataChange) {
                onDataChange(freshData);
              }
            }
          } else {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
        } catch (fetchError) {
          // If we have cached data, don't show error
          if (!cachedData) {
            throw fetchError;
          } else {
            logger.warn('Failed to fetch fresh data, using cached version', { 
              error: fetchError, 
              storeName, 
              itemId 
            });
          }
        }
      }

    } catch (err) {
      logger.error('Error loading synced content', { error: err, storeName, itemId });
      setError(err instanceof Error ? err.message : 'Erreur de chargement');
    } finally {
      setIsLoading(false);
    }
  }, [storeName, itemId, isOnline, onDataChange, ttl]);

  // Initial load
  useEffect(() => {
    loadData();
  }, [loadData]);

  // Periodic refresh
  useEffect(() => {
    if (refreshInterval > 0 && isOnline) {
      const interval = setInterval(loadData, refreshInterval);
      return () => clearInterval(interval);
    }
  }, [loadData, refreshInterval, isOnline]);

  // Update content optimistically
  const updateContent = useCallback(async (updates: Partial<T>) => {
    try {
      const currentData = data || {} as T;
      const updatedData = { ...currentData, ...updates };
      
      // Optimistic update
      setData(updatedData);
      
      if (onDataChange) {
        onDataChange(updatedData);
      }

      // Update cache
      await cache[storeName as keyof typeof cache]?.set(itemId, updatedData, { ttl });

      // Queue for sync if online, or queue for later if offline
      await queueChange({
        action: 'update' as const,
        data: updatedData,
        endpoint: `/${storeName}/${itemId}`,
        method: 'PUT' as const,
        maxRetries: 3,
      });

      logger.info('Content updated successfully', { storeName, itemId });
      
    } catch (err) {
      logger.error('Error updating content', { error: err, storeName, itemId });
      
      // Revert optimistic update
      await loadData();
      
      throw err;
    }
  }, [data, storeName, itemId, onDataChange, ttl, queueChange, loadData]);

  // Provide update function to children through context or props
  const renderContent = useCallback(() => {
    if (error && !data) {
      return errorContent;
    }
    
    if (isLoading && !data) {
      return loadingContent;
    }
    
    if (!data && fallbackContent) {
      return fallbackContent;
    }
    
    return children(data, isLoading, error);
  }, [data, isLoading, error, children, errorContent, loadingContent, fallbackContent]);

  return (
    <div className="synced-content" data-store={storeName} data-item-id={itemId}>
      {renderContent()}
    </div>
  );
}

/**
 * Higher-order component for synced content
 */
export function withSyncedContent<T, P extends object>(
  WrappedComponent: React.ComponentType<P & { data: T | null; isLoading: boolean; updateData: (updates: Partial<T>) => Promise<void> }>,
  syncConfig: {
    storeName: string;
    getItemId: (props: P) => string;
    ttl?: number;
    refreshInterval?: number;
  }
) {
  return function SyncedWrapper(props: P) {
    const itemId = syncConfig.getItemId(props);
    
    return (
      <SyncedContent<T>
        storeName={syncConfig.storeName}
        itemId={itemId}
        ttl={syncConfig.ttl}
        refreshInterval={syncConfig.refreshInterval}
      >
        {(data, isLoading, error) => (
          <SyncedContentInner
            {...props}
            data={data}
            isLoading={isLoading}
            error={error}
            WrappedComponent={WrappedComponent}
            storeName={syncConfig.storeName}
            itemId={itemId}
          />
        )}
      </SyncedContent>
    );
  };
}

// Helper component for the HOC
function SyncedContentInner<T, P extends object>({
  WrappedComponent,
  data,
  isLoading,
  error,
  storeName,
  itemId,
  ...props
}: {
  WrappedComponent: React.ComponentType<P & { data: T | null; isLoading: boolean; updateData: (updates: Partial<T>) => Promise<void> }>;
  data: T | null;
  isLoading: boolean;
  error: string | null;
  storeName: string;
  itemId: string;
} & P) {
  const { queueChange } = useSync();

  const updateData = useCallback(async (updates: Partial<T>) => {
    const currentData = data || {} as T;
    const updatedData = { ...currentData, ...updates };
    
    // Update cache
    await cache[storeName as keyof typeof cache]?.set(itemId, updatedData);

    // Queue for sync
    await queueChange({
      action: 'update' as const,
      data: updatedData,
      endpoint: `/${storeName}/${itemId}`,
      method: 'PUT' as const,
      maxRetries: 3,
    });
  }, [data, storeName, itemId, queueChange]);

  return (
    <WrappedComponent
      {...(props as P)}
      data={data}
      isLoading={isLoading}
      updateData={updateData}
    />
  );
}

export default SyncedContent;