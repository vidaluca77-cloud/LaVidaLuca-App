'use client';

import React, { useState } from 'react';
import { useAppDispatch } from '../../store/hooks';
import { showSuccessToast } from '../../store/slices/uiSlice';
import { UserProfile } from '../../lib/types';

interface OnboardingFlowProps {
  onComplete: (profile: UserProfile) => void;
}

const OnboardingFlow: React.FC<OnboardingFlowProps> = ({ onComplete }) => {
  const dispatch = useAppDispatch();
  const [step, setStep] = useState(1);
  const [profile, setProfile] = useState<UserProfile>({
    skills: [],
    availability: [],
    location: '',
    preferences: []
  });

  const skillsList = [
    'elevage', 'hygiene', 'soins_animaux', 'sol', 'plantes', 'organisation',
    'securite', 'bois', 'precision', 'creativite', 'patience', 'endurance',
    'ecologie', 'accueil', 'pedagogie', 'expression', 'equipe'
  ];

  const availabilityOptions = [
    'weekend', 'semaine', 'matin', 'apres-midi', 'vacances'
  ];

  const categoryOptions = [
    { id: 'agri', name: 'Agriculture', desc: 'Élevage, cultures, soins aux animaux' },
    { id: 'transfo', name: 'Transformation', desc: 'Fromage, conserves, pain...' },
    { id: 'artisanat', name: 'Artisanat', desc: 'Menuiserie, construction, réparation' },
    { id: 'nature', name: 'Environnement', desc: 'Plantation, compostage, écologie' },
    { id: 'social', name: 'Animation', desc: 'Accueil, visites, ateliers enfants' }
  ];

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

  const handleComplete = () => {
    dispatch(showSuccessToast({
      title: 'Profil créé avec succès !',
      message: 'Vos préférences ont été enregistrées.'
    }));
    onComplete(profile);
  };

  if (step === 1) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Comment souhaitez-vous participer ?
          </h1>
          <p className="text-gray-600">
            Sélectionnez vos compétences actuelles ou celles que vous aimeriez développer
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <h3 className="text-lg font-semibold text-gray-900">Vos compétences :</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {skillsList.map(skill => (
              <button
                key={skill}
                onClick={() => handleSkillToggle(skill)}
                className={`p-3 rounded-lg border text-sm font-medium transition-colors ${
                  profile.skills.includes(skill)
                    ? 'bg-green-500 text-white border-green-500'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                }`}
              >
                {skill.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-end">
          <button
            onClick={() => setStep(2)}
            className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            Suivant
          </button>
        </div>
      </div>
    );
  }

  if (step === 2) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Vos disponibilités
          </h1>
          <p className="text-gray-600">
            Quand pourriez-vous participer aux activités ?
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {availabilityOptions.map(option => (
              <button
                key={option}
                onClick={() => handleAvailabilityToggle(option)}
                className={`p-4 rounded-lg border text-sm font-medium transition-colors ${
                  profile.availability.includes(option)
                    ? 'bg-green-500 text-white border-green-500'
                    : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                }`}
              >
                {option.replace('_', ' ')}
              </button>
            ))}
          </div>
        </div>

        <div className="flex justify-between">
          <button
            onClick={() => setStep(1)}
            className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
          >
            Retour
          </button>
          <button
            onClick={() => setStep(3)}
            className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            Suivant
          </button>
        </div>
      </div>
    );
  }

  if (step === 3) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Votre région
          </h1>
          <p className="text-gray-600">
            Dans quelle région souhaitez-vous participer ?
          </p>
        </div>

        <div className="space-y-4 mb-8">
          <input
            type="text"
            placeholder="Ex: Ile-de-France, Auvergne-Rhône-Alpes..."
            value={profile.location}
            onChange={(e) => updateProfile('location', e.target.value)}
            className="w-full p-4 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>

        <div className="flex justify-between">
          <button
            onClick={() => setStep(2)}
            className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
          >
            Retour
          </button>
          <button
            onClick={() => setStep(4)}
            className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            Suivant
          </button>
        </div>
      </div>
    );
  }

  if (step === 4) {
    return (
      <div className="max-w-2xl mx-auto p-6">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Vos préférences
          </h1>
          <p className="text-gray-600">
            Quels types d'activités vous intéressent le plus ?
          </p>
        </div>

        <div className="space-y-4 mb-8">
          {categoryOptions.map(category => (
            <button
              key={category.id}
              onClick={() => handlePreferenceToggle(category.id)}
              className={`w-full p-4 rounded-lg border text-left transition-colors ${
                profile.preferences.includes(category.id)
                  ? 'bg-green-500 text-white border-green-500'
                  : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
              }`}
            >
              <div className="font-medium">{category.name}</div>
              <div className="text-sm opacity-90">{category.desc}</div>
            </button>
          ))}
        </div>

        <div className="flex justify-between">
          <button
            onClick={() => setStep(3)}
            className="bg-gray-300 text-gray-700 px-6 py-3 rounded-lg font-medium hover:bg-gray-400 transition-colors"
          >
            Retour
          </button>
          <button
            onClick={handleComplete}
            className="bg-green-500 text-white px-6 py-3 rounded-lg font-medium hover:bg-green-600 transition-colors"
          >
            Voir mes propositions
          </button>
        </div>
      </div>
    );
  }

  return null;
};

export default OnboardingFlow;