import { renderHook, act } from '@testing-library/react';
import { useUserProfile } from '@/hooks/useUserProfile';

describe('useUserProfile', () => {
  it('should initialize with default values', () => {
    const { result } = renderHook(() => useUserProfile());
    
    expect(result.current.profile).toEqual({
      skills: [],
      availability: [],
      location: '',
      preferences: [],
    });
  });

  it('should initialize with provided initial values', () => {
    const initialProfile = {
      skills: ['elevage'],
      location: 'Paris',
    };

    const { result } = renderHook(() => useUserProfile(initialProfile));
    
    expect(result.current.profile.skills).toEqual(['elevage']);
    expect(result.current.profile.location).toBe('Paris');
  });

  it('should update profile correctly', () => {
    const { result } = renderHook(() => useUserProfile());
    
    act(() => {
      result.current.updateProfile('location', 'Lyon');
    });

    expect(result.current.profile.location).toBe('Lyon');
  });

  it('should toggle skills correctly', () => {
    const { result } = renderHook(() => useUserProfile());
    
    // Add skill
    act(() => {
      result.current.handleSkillToggle('elevage');
    });

    expect(result.current.profile.skills).toContain('elevage');

    // Remove skill
    act(() => {
      result.current.handleSkillToggle('elevage');
    });

    expect(result.current.profile.skills).not.toContain('elevage');
  });

  it('should toggle availability correctly', () => {
    const { result } = renderHook(() => useUserProfile());
    
    act(() => {
      result.current.handleAvailabilityToggle('weekend');
    });

    expect(result.current.profile.availability).toContain('weekend');
  });

  it('should toggle preferences correctly', () => {
    const { result } = renderHook(() => useUserProfile());
    
    act(() => {
      result.current.handlePreferenceToggle('agri');
    });

    expect(result.current.profile.preferences).toContain('agri');
  });

  it('should reset profile correctly', () => {
    const { result } = renderHook(() => useUserProfile({
      skills: ['elevage'],
      location: 'Paris',
    }));
    
    act(() => {
      result.current.resetProfile();
    });

    expect(result.current.profile).toEqual({
      skills: [],
      availability: [],
      location: '',
      preferences: [],
    });
  });
});