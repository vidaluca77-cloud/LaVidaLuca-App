'use client';

import { useState, useEffect } from 'react';
import { apiClient, Activity } from '@/lib/api';

export function useActivities(params?: {
  category?: string;
  search?: string;
  limit?: number;
}) {
  const [activities, setActivities] = useState<Activity[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchActivities();
  }, [params?.category, params?.search]);

  const fetchActivities = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getActivities({
        ...params,
        active_only: true,
      });
      
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setActivities(response.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch activities');
    } finally {
      setLoading(false);
    }
  };

  return {
    activities,
    loading,
    error,
    refetch: fetchActivities,
  };
}

export function useActivity(activityId: number | null) {
  const [activity, setActivity] = useState<Activity | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (activityId) {
      fetchActivity(activityId);
    }
  }, [activityId]);

  const fetchActivity = async (id: number) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getActivity(id);
      
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setActivity(response.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch activity');
    } finally {
      setLoading(false);
    }
  };

  return {
    activity,
    loading,
    error,
    refetch: () => activityId && fetchActivity(activityId),
  };
}