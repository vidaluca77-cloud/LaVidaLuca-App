/**
 * Offline-aware Data Provider
 * Provides data from cache when offline, syncs when online
 */

'use client';

import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { offlineManager } from '@/lib/offlineManager';
import { logger } from '@/lib/logger';

interface OfflineDataContextValue {
  isOnline: boolean;
  isSyncing: boolean;
  pendingCount: number;
  
  // Data operations
  getActivity: (id: string) => Promise<any>;
  getAllActivities: () => Promise<any[]>;
  saveActivity: (activity: any) => Promise<void>;
  deleteActivity: (id: string) => Promise<void>;
  
  getUserProfile: (id: string) => Promise<any>;
  saveUserProfile: (profile: any) => Promise<void>;
  
  // Sync operations
  syncNow: () => Promise<void>;
  clearCache: () => Promise<void>;
}

const OfflineDataContext = createContext<OfflineDataContextValue | null>(null);

interface OfflineDataProviderProps {
  children: React.ReactNode;
}

export const OfflineDataProvider: React.FC<OfflineDataProviderProps> = ({ children }) => {
  const [isOnline, setIsOnline] = useState(typeof navigator !== 'undefined' ? navigator.onLine : true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    const updateOnlineStatus = () => {
      setIsOnline(navigator.onLine);
    };

    const updatePendingCount = async () => {
      try {
        const activitiesStatus = await offlineManager.getSyncStatus('activities');
        const profilesStatus = await offlineManager.getSyncStatus('userProfiles');
        setPendingCount(activitiesStatus.pending + profilesStatus.pending);
      } catch (error) {
        logger.error('Failed to update pending count', { error });
      }
    };

    const handleSyncResult = (result: any) => {
      setIsSyncing(false);
      updatePendingCount();
    };

    // Set up event listeners
    window.addEventListener('online', updateOnlineStatus);
    window.addEventListener('offline', updateOnlineStatus);
    offlineManager.onSync(handleSyncResult);

    // Initial updates
    updatePendingCount();

    return () => {
      window.removeEventListener('online', updateOnlineStatus);
      window.removeEventListener('offline', updateOnlineStatus);
      offlineManager.offSync(handleSyncResult);
    };
  }, []);

  // Activity operations
  const getActivity = useCallback(async (id: string) => {
    try {
      // Try to get from local storage first
      let activity = await offlineManager.getLocal('activities', id);
      
      // If online and no local data, try to fetch from server
      if (!activity && isOnline) {
        try {
          const response = await fetch(`/api/activities/${id}`);
          if (response.ok) {
            activity = await response.json();
            // Store in local cache
            await offlineManager.storeLocally('activities', id, activity, 'synced');
          }
        } catch (error) {
          logger.warn('Failed to fetch activity from server', { error, id });
        }
      }
      
      return activity;
    } catch (error) {
      logger.error('Failed to get activity', { error, id });
      throw error;
    }
  }, [isOnline]);

  const getAllActivities = useCallback(async () => {
    try {
      // Get all local activities
      let activities = await offlineManager.getAllLocal('activities');
      
      // If online, try to fetch latest from server
      if (isOnline) {
        try {
          const response = await fetch('/api/activities');
          if (response.ok) {
            const serverActivities = await response.json();
            
            // Merge with local data (server data takes precedence for synced items)
            const mergedActivities = [...serverActivities];
            
            // Add local-only activities (pending sync)
            activities.forEach(local => {
              if (local.syncStatus === 'pending' && 
                  !serverActivities.find((server: any) => server.id === local.id)) {
                mergedActivities.push(local);
              }
            });
            
            // Update local cache with server data
            for (const activity of serverActivities) {
              await offlineManager.storeLocally('activities', activity.id, activity, 'synced');
            }
            
            activities = mergedActivities;
          }
        } catch (error) {
          logger.warn('Failed to fetch activities from server', { error });
        }
      }
      
      return activities;
    } catch (error) {
      logger.error('Failed to get activities', { error });
      throw error;
    }
  }, [isOnline]);

  const saveActivity = useCallback(async (activity: any) => {
    try {
      // Always save locally first
      await offlineManager.storeLocally('activities', activity.id, activity, 'pending');
      
      // If online, try to sync immediately
      if (isOnline) {
        try {
          const response = await fetch(`/api/activities/${activity.id}`, {
            method: activity.id ? 'PUT' : 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(activity)
          });
          
          if (response.ok) {
            const savedActivity = await response.json();
            await offlineManager.storeLocally('activities', savedActivity.id, savedActivity, 'synced');
          }
        } catch (error) {
          logger.warn('Failed to sync activity to server', { error });
          // Still counts as success since it's saved locally
        }
      }
      
      await updatePendingCount();
    } catch (error) {
      logger.error('Failed to save activity', { error });
      throw error;
    }
  }, [isOnline]);

  const deleteActivity = useCallback(async (id: string) => {
    try {
      // Mark as deleted locally
      const activity = await offlineManager.getLocal('activities', id);
      if (activity) {
        activity.deleted = true;
        await offlineManager.storeLocally('activities', id, activity, 'pending');
      }
      
      // If online, try to delete from server
      if (isOnline) {
        try {
          await fetch(`/api/activities/${id}`, { method: 'DELETE' });
          // Remove from local storage if successfully deleted from server
          // (implement removal in offlineManager if needed)
        } catch (error) {
          logger.warn('Failed to delete activity from server', { error });
        }
      }
    } catch (error) {
      logger.error('Failed to delete activity', { error });
      throw error;
    }
  }, [isOnline]);

  // User profile operations
  const getUserProfile = useCallback(async (id: string) => {
    try {
      let profile = await offlineManager.getLocal('userProfiles', id);
      
      if (!profile && isOnline) {
        try {
          const response = await fetch(`/api/users/${id}/profile`);
          if (response.ok) {
            profile = await response.json();
            await offlineManager.storeLocally('userProfiles', id, profile, 'synced');
          }
        } catch (error) {
          logger.warn('Failed to fetch user profile from server', { error });
        }
      }
      
      return profile;
    } catch (error) {
      logger.error('Failed to get user profile', { error });
      throw error;
    }
  }, [isOnline]);

  const saveUserProfile = useCallback(async (profile: any) => {
    try {
      await offlineManager.storeLocally('userProfiles', profile.id, profile, 'pending');
      
      if (isOnline) {
        try {
          const response = await fetch(`/api/users/${profile.id}/profile`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profile)
          });
          
          if (response.ok) {
            const savedProfile = await response.json();
            await offlineManager.storeLocally('userProfiles', savedProfile.id, savedProfile, 'synced');
          }
        } catch (error) {
          logger.warn('Failed to sync user profile to server', { error });
        }
      }
    } catch (error) {
      logger.error('Failed to save user profile', { error });
      throw error;
    }
  }, [isOnline]);

  // Sync operations
  const syncNow = useCallback(async () => {
    if (isSyncing || !isOnline) return;
    
    setIsSyncing(true);
    try {
      await offlineManager.synchronize();
    } finally {
      setIsSyncing(false);
    }
  }, [isSyncing, isOnline]);

  const clearCache = useCallback(async () => {
    try {
      await offlineManager.clearLocalData();
      setPendingCount(0);
      logger.info('Local cache cleared');
    } catch (error) {
      logger.error('Failed to clear cache', { error });
      throw error;
    }
  }, []);

  const updatePendingCount = async () => {
    try {
      const activitiesStatus = await offlineManager.getSyncStatus('activities');
      const profilesStatus = await offlineManager.getSyncStatus('userProfiles');
      setPendingCount(activitiesStatus.pending + profilesStatus.pending);
    } catch (error) {
      logger.error('Failed to update pending count', { error });
    }
  };

  const contextValue: OfflineDataContextValue = {
    isOnline,
    isSyncing,
    pendingCount,
    getActivity,
    getAllActivities,
    saveActivity,
    deleteActivity,
    getUserProfile,
    saveUserProfile,
    syncNow,
    clearCache
  };

  return (
    <OfflineDataContext.Provider value={contextValue}>
      {children}
    </OfflineDataContext.Provider>
  );
};

export const useOfflineData = () => {
  const context = useContext(OfflineDataContext);
  if (!context) {
    throw new Error('useOfflineData must be used within an OfflineDataProvider');
  }
  return context;
};

export default OfflineDataProvider;