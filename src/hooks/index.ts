import { useState } from 'react';
import { UserProfile, Suggestion, PageType } from '@/types';
import { calculateMatching } from '@/lib/utils';

/**
 * Custom hook for managing the main application state
 */
export const useAppNavigation = () => {
  const [currentPage, setCurrentPage] = useState<PageType>('home');
  const [userProfile, setUserProfile] = useState<UserProfile | null>(null);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);

  const handleOnboardingComplete = (profile: UserProfile) => {
    setUserProfile(profile);
    const calculatedSuggestions = calculateMatching(profile);
    setSuggestions(calculatedSuggestions);
    setCurrentPage('suggestions');
  };

  const navigateToOnboarding = () => {
    setCurrentPage('onboarding');
  };

  const navigateToCatalog = () => {
    setCurrentPage('catalog');
  };

  const navigateToHome = () => {
    setCurrentPage('home');
  };

  return {
    currentPage,
    userProfile,
    suggestions,
    handleOnboardingComplete,
    navigateToOnboarding,
    navigateToCatalog,
    navigateToHome,
  };
};

/**
 * Custom hook for managing onboarding form state
 */
export const useOnboardingForm = () => {
  const [step, setStep] = useState(1);
  const [profile, setProfile] = useState<UserProfile>({
    skills: [],
    availability: [],
    location: '',
    preferences: [],
  });

  const updateProfile = (key: keyof UserProfile, value: any) => {
    setProfile(prev => ({ ...prev, [key]: value }));
  };

  const handleSkillToggle = (skill: string) => {
    const newSkills = profile.skills.includes(skill)
      ? profile.skills.filter(s => s !== skill)
      : [...profile.skills, skill];
    updateProfile('skills', newSkills);
  };

  const handleAvailabilityToggle = (option: string) => {
    const newAvailability = profile.availability.includes(option)
      ? profile.availability.filter(a => a !== option)
      : [...profile.availability, option];
    updateProfile('availability', newAvailability);
  };

  const handlePreferenceToggle = (category: string) => {
    const newPreferences = profile.preferences.includes(category)
      ? profile.preferences.filter(p => p !== category)
      : [...profile.preferences, category];
    updateProfile('preferences', newPreferences);
  };

  return {
    step,
    setStep,
    profile,
    updateProfile,
    handleSkillToggle,
    handleAvailabilityToggle,
    handlePreferenceToggle,
  };
};
