import { useState, useCallback } from 'react';

export interface UserProfile {
  skills: string[];
  availability: string[];
  location: string;
  preferences: string[];
}

export const useUserProfile = (initialProfile?: Partial<UserProfile>) => {
  const [profile, setProfile] = useState<UserProfile>({
    skills: [],
    availability: [],
    location: '',
    preferences: [],
    ...initialProfile,
  });

  const updateProfile = useCallback((key: keyof UserProfile, value: any) => {
    setProfile(prev => ({ ...prev, [key]: value }));
  }, []);

  const handleSkillToggle = useCallback((skill: string) => {
    setProfile(prev => ({
      ...prev,
      skills: prev.skills.includes(skill)
        ? prev.skills.filter(s => s !== skill)
        : [...prev.skills, skill]
    }));
  }, []);

  const handleAvailabilityToggle = useCallback((option: string) => {
    setProfile(prev => ({
      ...prev,
      availability: prev.availability.includes(option)
        ? prev.availability.filter(a => a !== option)
        : [...prev.availability, option]
    }));
  }, []);

  const handlePreferenceToggle = useCallback((category: string) => {
    setProfile(prev => ({
      ...prev,
      preferences: prev.preferences.includes(category)
        ? prev.preferences.filter(p => p !== category)
        : [...prev.preferences, category]
    }));
  }, []);

  const resetProfile = useCallback(() => {
    setProfile({
      skills: [],
      availability: [],
      location: '',
      preferences: [],
    });
  }, []);

  return {
    profile,
    updateProfile,
    handleSkillToggle,
    handleAvailabilityToggle,
    handlePreferenceToggle,
    resetProfile,
  };
};