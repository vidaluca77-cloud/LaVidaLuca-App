'use client';

import { useState, useEffect } from 'react';
import { apiClient, Recommendation } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export function useRecommendations(limit: number = 5) {
  const { user } = useAuth();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [profileCompleteness, setProfileCompleteness] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user) {
      fetchRecommendations();
    }
  }, [user, limit]);

  const fetchRecommendations = async () => {
    if (!user) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getRecommendations(limit);
      
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setRecommendations(response.data.recommendations);
        setProfileCompleteness(response.data.user_profile_completeness || null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch recommendations');
    } finally {
      setLoading(false);
    }
  };

  const fetchRecommendationsByPreferences = async (preferences: {
    user_skills?: string[];
    user_preferences?: string[];
    user_availability?: string[];
    limit?: number;
  }) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.getRecommendationsByPreferences(preferences);
      
      if (response.error) {
        setError(response.error);
      } else if (response.data) {
        setRecommendations(response.data.recommendations);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch recommendations');
    } finally {
      setLoading(false);
    }
  };

  return {
    recommendations,
    profileCompleteness,
    loading,
    error,
    refetch: fetchRecommendations,
    fetchByPreferences: fetchRecommendationsByPreferences,
  };
}