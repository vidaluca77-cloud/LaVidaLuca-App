'use client'

import React, { useEffect } from 'react';
import { useAppDispatch } from '../../store/hooks';
import { setCurrentPage } from '../../store/slices/uiSlice';
import { fetchActivities } from '../../store/slices/activitiesSlice';
import { setUserProfile } from '../../store/slices/authSlice';
import { useUserProfile, useNavigation } from '../../lib/hooks';
import { UserProfile } from '../../lib/types';

// Import existing components (refactored to use Redux)
import HomePage from './HomePage';
import OnboardingFlow from './OnboardingFlow';
import SuggestionsPage from './SuggestionsPage';
import ActivityCatalog from './ActivityCatalog';

// Main App component using Redux state management
const App = () => {
  const dispatch = useAppDispatch();
  const { currentPage } = useNavigation();
  const { user } = useUserProfile();

  // Initialize app data
  useEffect(() => {
    dispatch(fetchActivities({}));
  }, [dispatch]);

  const handleOnboardingComplete = (profile: UserProfile) => {
    dispatch(setUserProfile(profile));
    dispatch(setCurrentPage('suggestions'));
  };

  const navigateToOnboarding = () => {
    dispatch(setCurrentPage('onboarding'));
  };

  const navigateToCatalog = () => {
    dispatch(setCurrentPage('catalog'));
  };

  const navigateToHome = () => {
    dispatch(setCurrentPage('home'));
  };

  // Render current page based on Redux state
  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'onboarding':
        return (
          <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50">
            <div className="py-8">
              <div className="text-center mb-8">
                <button 
                  onClick={navigateToHome}
                  className="inline-flex items-center space-x-2 text-green-500 hover:text-green-600 mb-4"
                >
                  <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-sm">VL</span>
                  </div>
                  <span className="font-bold text-xl">La Vida Luca</span>
                </button>
              </div>
              <OnboardingFlow onComplete={handleOnboardingComplete} />
            </div>
          </div>
        );

      case 'suggestions':
        if (!user.profile) {
          dispatch(setCurrentPage('onboarding'));
          return null;
        }
        return (
          <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50">
            <div className="py-8">
              <div className="text-center mb-8">
                <button 
                  onClick={navigateToHome}
                  className="inline-flex items-center space-x-2 text-green-500 hover:text-green-600 mb-4"
                >
                  <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-sm">VL</span>
                  </div>
                  <span className="font-bold text-xl">La Vida Luca</span>
                </button>
              </div>
              <SuggestionsPage profile={user.profile} />
            </div>
          </div>
        );

      case 'catalog':
        return (
          <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50">
            <div className="py-8">
              <div className="text-center mb-8">
                <button 
                  onClick={navigateToHome}
                  className="inline-flex items-center space-x-2 text-green-500 hover:text-green-600 mb-4"
                >
                  <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
                    <span className="text-white font-bold text-sm">VL</span>
                  </div>
                  <span className="font-bold text-xl">La Vida Luca</span>
                </button>
              </div>
              <ActivityCatalog />
            </div>
          </div>
        );

      default:
        return (
          <div onClick={(e) => {
            const target = e.target as HTMLElement;
            if (target.textContent === 'Proposer mon aide') {
              e.preventDefault();
              navigateToOnboarding();
            } else if (target.textContent === 'Découvrir nos activités') {
              e.preventDefault();
              navigateToCatalog();
            }
          }}>
            <HomePage />
          </div>
        );
    }
  };

  return renderCurrentPage();
};

export default App;