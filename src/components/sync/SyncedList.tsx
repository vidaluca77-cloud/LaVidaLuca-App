'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { useSync } from '@/hooks/useSync';
import { cache } from '@/lib/cache';
import { logger } from '@/lib/logger';

interface SyncedListProps<T> {
  storeName: string;
  endpoint?: string;
  children: (items: T[], isLoading: boolean, error: string | null, actions: ListActions<T>) => React.ReactNode;
  loadingContent?: React.ReactNode;
  errorContent?: React.ReactNode;
  emptyContent?: React.ReactNode;
  refreshInterval?: number;
  ttl?: number;
  filter?: (item: T) => boolean;
  sort?: (a: T, b: T) => number;
  limit?: number;
  onDataChange?: (items: T[]) => void;
}

interface ListActions<T> {
  refresh: () => Promise<void>;
  addItem: (item: Omit<T, 'id'>) => Promise<void>;
  updateItem: (id: string, updates: Partial<T>) => Promise<void>;
  deleteItem: (id: string) => Promise<void>;
  clearCache: () => Promise<void>;
}

/**
 * Component for synced lists with full CRUD operations
 */
export function SyncedList<T extends { id: string }>({
  storeName,
  endpoint = `/${storeName}`,
  children,
  loadingContent = (
    <div className="space-y-3">
      {[...Array(3)].map((_, i) => (
        <div key={i} className="animate-pulse bg-gray-200 h-16 w-full rounded"></div>
      ))}
    </div>
  ),
  errorContent = <div className="text-red-500 text-sm">Erreur de chargement de la liste</div>,
  emptyContent = <div className="text-gray-500 text-sm text-center py-8">Aucun élément</div>,
  refreshInterval = 60000, // 1 minute
  ttl = 300000, // 5 minutes
  filter,
  sort,
  limit,
  onDataChange,
}: SyncedListProps<T>) {
  const [items, setItems] = useState<T[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const { isOnline, queueChange } = useSync();

  // Load data from cache or fetch from API
  const loadData = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      // First, try to get from cache
      const cachedItems = await cache[storeName as keyof typeof cache]?.getAll() || [];
      
      if (cachedItems.length > 0) {
        let processedItems = [...cachedItems] as T[];
        
        // Apply filter
        if (filter) {
          processedItems = processedItems.filter(filter);
        }
        
        // Apply sort
        if (sort) {
          processedItems.sort(sort);
        }
        
        // Apply limit
        if (limit) {
          processedItems = processedItems.slice(0, limit);
        }
        
        setItems(processedItems);
        setIsLoading(false);
        
        if (onDataChange) {
          onDataChange(processedItems);
        }
      }

      // If online, try to fetch fresh data
      if (isOnline) {
        try {
          const response = await fetch(`/api${endpoint}`);
          
          if (response.ok) {
            const freshData = await response.json();
            const freshItems = Array.isArray(freshData) ? freshData : freshData.data || [];
            
            // Update cache for each item
            for (const item of freshItems) {
              await cache[storeName as keyof typeof cache]?.set(item.id, item, { ttl });
            }
            
            // Process fresh items
            let processedItems = [...freshItems] as T[];
            
            if (filter) {
              processedItems = processedItems.filter(filter);
            }
            
            if (sort) {
              processedItems.sort(sort);
            }
            
            if (limit) {
              processedItems = processedItems.slice(0, limit);
            }
            
            // Update state if data changed
            if (JSON.stringify(processedItems) !== JSON.stringify(cachedItems)) {
              setItems(processedItems);
              
              if (onDataChange) {
                onDataChange(processedItems);
              }
            }
          } else {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
        } catch (fetchError) {
          // If we have cached data, don't show error
          if (cachedItems.length === 0) {
            throw fetchError;
          } else {
            logger.warn('Failed to fetch fresh data, using cached version', { 
              error: fetchError, 
              storeName, 
              endpoint 
            });
          }
        }
      }

    } catch (err) {
      logger.error('Error loading synced list', { error: err, storeName, endpoint });
      setError(err instanceof Error ? err.message : 'Erreur de chargement');
    } finally {
      setIsLoading(false);
    }
  }, [storeName, endpoint, isOnline, filter, sort, limit, onDataChange, ttl]);

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

  // Refresh function
  const refresh = useCallback(async () => {
    await loadData();
  }, [loadData]);

  // Add item
  const addItem = useCallback(async (newItem: Omit<T, 'id'>) => {
    try {
      const id = crypto.randomUUID();
      const itemWithId = { ...newItem, id } as T;
      
      // Optimistic update
      setItems(prev => [itemWithId, ...prev]);
      
      // Update cache
      await cache[storeName as keyof typeof cache]?.set(id, itemWithId, { ttl });

      // Queue for sync
      await queueChange({
        action: 'create' as const,
        data: itemWithId,
        endpoint: endpoint,
        method: 'POST' as const,
        maxRetries: 3,
      });

      logger.info('Item added successfully', { storeName, id });
      
    } catch (err) {
      logger.error('Error adding item', { error: err, storeName });
      
      // Revert optimistic update
      await loadData();
      
      throw err;
    }
  }, [storeName, endpoint, ttl, queueChange, loadData]);

  // Update item
  const updateItem = useCallback(async (id: string, updates: Partial<T>) => {
    try {
      // Find and update item
      const updatedItems = items.map(item => 
        item.id === id ? { ...item, ...updates } : item
      );
      
      // Optimistic update
      setItems(updatedItems);
      
      // Update cache
      const updatedItem = updatedItems.find(item => item.id === id);
      if (updatedItem) {
        await cache[storeName as keyof typeof cache]?.set(id, updatedItem, { ttl });
      }

      // Queue for sync
      await queueChange({
        action: 'update' as const,
        data: updates,
        endpoint: `${endpoint}/${id}`,
        method: 'PUT' as const,
        maxRetries: 3,
      });

      logger.info('Item updated successfully', { storeName, id });
      
    } catch (err) {
      logger.error('Error updating item', { error: err, storeName, id });
      
      // Revert optimistic update
      await loadData();
      
      throw err;
    }
  }, [items, storeName, endpoint, ttl, queueChange, loadData]);

  // Delete item
  const deleteItem = useCallback(async (id: string) => {
    try {
      // Optimistic update
      setItems(prev => prev.filter(item => item.id !== id));
      
      // Remove from cache
      await cache[storeName as keyof typeof cache]?.delete(id);

      // Queue for sync
      await queueChange({
        action: 'delete' as const,
        data: { id },
        endpoint: `${endpoint}/${id}`,
        method: 'DELETE' as const,
        maxRetries: 3,
      });

      logger.info('Item deleted successfully', { storeName, id });
      
    } catch (err) {
      logger.error('Error deleting item', { error: err, storeName, id });
      
      // Revert optimistic update
      await loadData();
      
      throw err;
    }
  }, [storeName, endpoint, queueChange, loadData]);

  // Clear cache
  const clearCache = useCallback(async () => {
    try {
      await cache[storeName as keyof typeof cache]?.clear?.();
      await loadData();
      logger.info('Cache cleared successfully', { storeName });
    } catch (err) {
      logger.error('Error clearing cache', { error: err, storeName });
      throw err;
    }
  }, [storeName, loadData]);

  const actions: ListActions<T> = {
    refresh,
    addItem,
    updateItem,
    deleteItem,
    clearCache,
  };

  const renderContent = useCallback(() => {
    if (error && items.length === 0) {
      return errorContent;
    }
    
    if (isLoading && items.length === 0) {
      return loadingContent;
    }
    
    if (items.length === 0) {
      return emptyContent;
    }
    
    return children(items, isLoading, error, actions);
  }, [items, isLoading, error, children, actions, errorContent, loadingContent, emptyContent]);

  return (
    <div className="synced-list" data-store={storeName} data-endpoint={endpoint}>
      {renderContent()}
    </div>
  );
}

/**
 * Simple list component for read-only synced data
 */
export function SimpleSyncedList<T extends { id: string }>({
  storeName,
  endpoint,
  renderItem,
  className = '',
  ...props
}: Omit<SyncedListProps<T>, 'children'> & {
  renderItem: (item: T, index: number) => React.ReactNode;
  className?: string;
}) {
  return (
    <SyncedList<T> storeName={storeName} endpoint={endpoint} {...props}>
      {(items, isLoading, error) => (
        <div className={className}>
          {items.map((item, index) => (
            <div key={item.id}>
              {renderItem(item, index)}
            </div>
          ))}
        </div>
      )}
    </SyncedList>
  );
}

export default SyncedList;