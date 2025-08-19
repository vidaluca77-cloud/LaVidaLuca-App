'use client';

import React, { useState, useEffect } from 'react';
import { ClockIcon, ShieldCheckIcon, UserGroupIcon, StarIcon } from '@heroicons/react/24/outline';
import { useAppSelector, useAppDispatch } from '../../store/hooks';
import { generateSuggestions, generateLocalSuggestions } from '../../store/slices/activitiesSlice';
import { showSuccessToast, showInfoToast } from '../../store/slices/uiSlice';
import { LoadingSpinner } from '../../lib/components/ui/Loading';
import { UserProfile, Activity, Suggestion } from '../../lib/types';

interface SuggestionsPageProps {
  profile: UserProfile;
}

const SuggestionsPage: React.FC<SuggestionsPageProps> = ({ profile }) => {
  const dispatch = useAppDispatch();
  const { suggestions, isLoading } = useAppSelector(state => state.activities);
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [showGuide, setShowGuide] = useState(false);

  // Generate suggestions when component mounts
  useEffect(() => {
    const generateSuggestionsForProfile = async () => {
      try {
        await dispatch(generateSuggestions(profile)).unwrap();
      } catch (error) {
        // Fallback to local suggestions if API fails
        dispatch(generateLocalSuggestions(profile));
        dispatch(showInfoToast({
          title: 'Mode hors ligne',
          message: 'Suggestions générées localement'
        }));
      }
    };

    generateSuggestionsForProfile();
  }, [dispatch, profile]);

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h${mins > 0 ? mins.toString().padStart(2, '0') : ''}`;
    }
    return `${mins}min`;
  };

  const getSafetyColor = (level: number) => {
    switch (level) {
      case 1: return 'bg-green-100 text-green-800';
      case 2: return 'bg-yellow-100 text-yellow-800';
      case 3: return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSafetyText = (level: number) => {
    switch (level) {
      case 1: return 'Facile';
      case 2: return 'Attention';
      case 3: return 'Expert';
      default: return 'Non défini';
    }
  };

  const generateSafetyGuide = (activity: Activity) => {
    const rules = [
      "Respecter les consignes de l'encadrant en permanence",
      "Porter les équipements de protection indiqués",
      "Signaler immédiatement tout problème ou incident"
    ];

    const checklist = [
      "Vérifier la présence de l'encadrant",
      "S'assurer d'avoir tous les matériels nécessaires",
      "Prendre connaissance des consignes de sécurité"
    ];

    if (activity.safety_level >= 2) {
      rules.push(
        "Ne jamais agir seul, toujours en binôme minimum",
        "Vérifier deux fois avant d'utiliser un outil"
      );
      checklist.push(
        "Vérifier l'état des outils avant utilisation",
        "S'assurer de la présence d'une trousse de premiers secours"
      );
    }

    return { rules, checklist };
  };

  const handleRegister = (activity: Activity) => {
    dispatch(showSuccessToast({
      title: 'Inscription enregistrée !',
      message: `Vous êtes inscrit à l'activité "${activity.title}". Un encadrant vous contactera bientôt.`
    }));
    setShowGuide(false);
    setSelectedActivity(null);
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto p-6 flex items-center justify-center min-h-96">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-gray-600">Génération de vos suggestions personnalisées...</p>
        </div>
      </div>
    );
  }

  if (showGuide && selectedActivity) {
    const guide = generateSafetyGuide(selectedActivity);
    
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">
            Guide sécurité : {selectedActivity.title}
          </h2>
          
          <div className="mb-6">
            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-4">
              <div className="flex items-center">
                <ClockIcon className="w-4 h-4 mr-1" />
                {formatDuration(selectedActivity.duration_min)}
              </div>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${getSafetyColor(selectedActivity.safety_level)}`}>
                {getSafetyText(selectedActivity.safety_level)}
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Règles de sécurité
              </h3>
              <ul className="space-y-2">
                {guide.rules.map((rule, index) => (
                  <li key={index} className="flex items-start">
                    <ShieldCheckIcon className="w-5 h-5 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    <span className="text-gray-700">{rule}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Checklist avant de commencer
              </h3>
              <ul className="space-y-2">
                {guide.checklist.map((item, index) => (
                  <li key={index} className="flex items-start">
                    <input 
                      type="checkbox" 
                      className="w-4 h-4 text-green-500 mr-3 mt-1"
                      onChange={() => {}}
                    />
                    <span className="text-gray-700">{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {selectedActivity.materials.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  Matériel requis
                </h3>
                <div className="flex flex-wrap gap-2">
                  {selectedActivity.materials.map((material, index) => (
                    <span 
                      key={index}
                      className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium"
                    >
                      {material}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="flex justify-between mt-8">
            <button
              onClick={() => setShowGuide(false)}
              className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
            >
              Retour
            </button>
            <button
              onClick={() => handleRegister(selectedActivity)}
              className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
            >
              Je m'inscris
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Vos propositions personnalisées
        </h1>
        <p className="text-gray-600">
          Notre IA a sélectionné ces activités spécialement pour vous
        </p>
      </div>

      <div className="space-y-6">
        {suggestions.map((suggestion, index) => (
          <div key={suggestion.activity.id} className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <div className="flex items-start justify-between mb-4">
              <div className="flex-1">
                <div className="flex items-center mb-2">
                  <span className="bg-green-500 text-white px-3 py-1 rounded-full text-xs font-medium mr-3">
                    #{index + 1}
                  </span>
                  <h3 className="text-xl font-bold text-gray-900">
                    {suggestion.activity.title}
                  </h3>
                </div>
                <p className="text-gray-600 mb-4">
                  {suggestion.activity.summary}
                </p>
              </div>
              <div className="text-right ml-4">
                <div className="flex items-center text-yellow-500 mb-2">
                  <StarIcon className="w-5 h-5 mr-1" />
                  <span className="font-bold">{Math.round(suggestion.score)}%</span>
                </div>
                <span className="text-xs text-gray-500">compatibilité</span>
              </div>
            </div>

            <div className="flex items-center space-x-4 text-sm text-gray-600 mb-4">
              <div className="flex items-center">
                <ClockIcon className="w-4 h-4 mr-1" />
                {formatDuration(suggestion.activity.duration_min)}
              </div>
              <div className={`px-2 py-1 rounded-full text-xs font-medium ${getSafetyColor(suggestion.activity.safety_level)}`}>
                {getSafetyText(suggestion.activity.safety_level)}
              </div>
              <div className="flex items-center">
                <UserGroupIcon className="w-4 h-4 mr-1" />
                {suggestion.activity.category}
              </div>
            </div>

            <div className="mb-4">
              <h4 className="font-medium text-gray-900 mb-2">Pourquoi cette activité vous correspond :</h4>
              <ul className="space-y-1">
                {suggestion.reasons.map((reason, reasonIndex) => (
                  <li key={reasonIndex} className="flex items-start text-sm text-gray-700">
                    <span className="text-green-500 mr-2">•</span>
                    {reason}
                  </li>
                ))}
              </ul>
            </div>

            <div className="flex space-x-3">
              <button
                onClick={() => {
                  setSelectedActivity(suggestion.activity);
                  setShowGuide(true);
                }}
                className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors flex-1"
              >
                Voir le guide & m'inscrire
              </button>
              <button
                onClick={() => setSelectedActivity(suggestion.activity)}
                className="bg-white text-green-500 border-2 border-green-500 px-4 py-3 rounded-lg font-medium hover:bg-green-50 transition-colors"
              >
                Détails
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="text-center mt-8">
        <p className="text-gray-600 mb-4">
          Ces propositions ne vous conviennent pas ?
        </p>
        <button
          onClick={() => window.location.reload()}
          className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
        >
          Refaire le questionnaire
        </button>
      </div>
    </div>
  );
};

export default SuggestionsPage;