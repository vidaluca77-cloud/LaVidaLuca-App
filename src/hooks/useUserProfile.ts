/**
 * Custom hook for managing user profile state
 */
import { useState, useCallback } from 'react';
import { UserProfile } from '@/types';

interface UseUserProfileReturn {
  profile: UserProfile;
  updateProfile: (key: keyof UserProfile, value: any) => void;
  resetProfile: () => void;
  isProfileComplete: boolean;
}

const initialProfile: UserProfile = {
  skills: [],
  availability: [],
  location: '',
  preferences: [],
};

/**
 * Hook for managing user profile state and operations
 * @returns Object with profile state and methods
 */
export const useUserProfile = (): UseUserProfileReturn => {
  const [profile, setProfile] = useState<UserProfile>(initialProfile);

  const updateProfile = useCallback((key: keyof UserProfile, value: any) => {
    setProfile(prev => ({ ...prev, [key]: value }));
  }, []);

  const resetProfile = useCallback(() => {
    setProfile(initialProfile);
  }, []);

  const isProfileComplete =
    profile.skills.length > 0 &&
    profile.availability.length > 0 &&
    profile.location.trim() !== '' &&
    profile.preferences.length > 0;

  return {
    profile,
    updateProfile,
    resetProfile,
    isProfileComplete,
  };
};
