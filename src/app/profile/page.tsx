'use client';

import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useAuth } from '../../context/AuthContext';
import { ProfileFormData } from '../../types';
import { activityService } from '../../lib/services';
import { useRouter } from 'next/navigation';

export default function ProfilePage() {
  const { user, profile, updateProfile, isAuthenticated, isLoading } = useAuth();
  const [availableSkills, setAvailableSkills] = useState<string[]>([]);
  const [availableCategories, setAvailableCategories] = useState<string[]>([]);
  const router = useRouter();

  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<ProfileFormData>();

  const watchedSkills = watch('skills', []);
  const watchedPreferences = watch('preferences', []);
  const watchedAvailability = watch('availability', []);

  // Redirection si non authentifié
  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push('/auth/login');
    }
  }, [isAuthenticated, isLoading, router]);

  // Charger les données des activités
  useEffect(() => {
    const loadData = async () => {
      try {
        const [skills, categories] = await Promise.all([
          activityService.getSkills(),
          activityService.getCategories(),
        ]);
        setAvailableSkills(skills);
        setAvailableCategories(categories);
      } catch (error) {
        console.error('Erreur lors du chargement des données:', error);
      }
    };

    loadData();
  }, []);

  // Pré-remplir le formulaire avec les données du profil
  useEffect(() => {
    if (profile) {
      setValue('location', profile.location || '');
      setValue('availability', profile.availability || []);
      setValue('experience_level', profile.experience_level || 'debutant');
      setValue('skills', profile.skills || []);
      setValue('preferences', profile.preferences || []);
    }
  }, [profile, setValue]);

  const availabilityOptions = [
    'weekend',
    'semaine',
    'matin',
    'apres-midi',
    'vacances',
  ];

  const experienceLevels = [
    { value: 'debutant', label: 'Débutant' },
    { value: 'intermediaire', label: 'Intermédiaire' },
    { value: 'avance', label: 'Avancé' },
  ];

  const categoryLabels: Record<string, string> = {
    agri: 'Agriculture',
    transfo: 'Transformation',
    artisanat: 'Artisanat',
    nature: 'Environnement',
    social: 'Animation sociale',
  };

  const handleSkillToggle = (skill: string) => {
    const currentSkills = watchedSkills || [];
    const newSkills = currentSkills.includes(skill)
      ? currentSkills.filter((s) => s !== skill)
      : [...currentSkills, skill];
    setValue('skills', newSkills);
  };

  const handlePreferenceToggle = (category: string) => {
    const currentPrefs = watchedPreferences || [];
    const newPrefs = currentPrefs.includes(category)
      ? currentPrefs.filter((p) => p !== category)
      : [...currentPrefs, category];
    setValue('preferences', newPrefs);
  };

  const handleAvailabilityToggle = (option: string) => {
    const currentAvailability = watchedAvailability || [];
    const newAvailability = currentAvailability.includes(option)
      ? currentAvailability.filter((a) => a !== option)
      : [...currentAvailability, option];
    setValue('availability', newAvailability);
  };

  const onSubmit = async (data: ProfileFormData) => {
    try {
      await updateProfile(data);
      router.push('/recommendations');
    } catch (error) {
      // L'erreur est déjà gérée dans le contexte
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null; // Redirection en cours
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-4">
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Mon Profil</h1>
          <p className="text-gray-600">
            Complétez votre profil pour recevoir des recommandations personnalisées
          </p>
          {user && (
            <div className="mt-4 p-4 bg-green-50 rounded-lg">
              <p className="text-sm text-green-800">
                <strong>Email:</strong> {user.email}
              </p>
              {user.full_name && (
                <p className="text-sm text-green-800">
                  <strong>Nom:</strong> {user.full_name}
                </p>
              )}
              {user.is_mfr_student && (
                <p className="text-sm text-green-800">
                  ✓ Élève en MFR
                </p>
              )}
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
          {/* Localisation */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Localisation
            </label>
            <input
              {...register('location')}
              type="text"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-green-500 focus:border-green-500"
              placeholder="Ex: Calvados (14), Normandie"
            />
          </div>

          {/* Niveau d'expérience */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Niveau d'expérience
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {experienceLevels.map((level) => (
                <label key={level.value} className="relative flex cursor-pointer">
                  <input
                    {...register('experience_level')}
                    type="radio"
                    value={level.value}
                    className="sr-only"
                  />
                  <div className="flex-1 p-3 border border-gray-300 rounded-lg text-center hover:border-green-500 transition-colors">
                    {level.label}
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Disponibilités */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Quand pouvez-vous participer ?
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {availabilityOptions.map((option) => (
                <button
                  key={option}
                  type="button"
                  onClick={() => handleAvailabilityToggle(option)}
                  className={`p-3 rounded-lg border text-sm font-medium transition-colors ${
                    (watchedAvailability || []).includes(option)
                      ? 'bg-green-500 text-white border-green-500'
                      : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                  }`}
                >
                  {option.replace('-', ' ')}
                </button>
              ))}
            </div>
          </div>

          {/* Compétences */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Vos compétences et intérêts
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              {availableSkills.map((skill) => (
                <button
                  key={skill}
                  type="button"
                  onClick={() => handleSkillToggle(skill)}
                  className={`p-2 rounded-md border text-xs font-medium transition-colors ${
                    (watchedSkills || []).includes(skill)
                      ? 'bg-green-500 text-white border-green-500'
                      : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                  }`}
                >
                  {skill.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>

          {/* Préférences de catégories */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Catégories d'activités préférées
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {availableCategories.map((category) => (
                <button
                  key={category}
                  type="button"
                  onClick={() => handlePreferenceToggle(category)}
                  className={`p-4 rounded-lg border text-left transition-colors ${
                    (watchedPreferences || []).includes(category)
                      ? 'bg-green-500 text-white border-green-500'
                      : 'bg-white text-gray-700 border-gray-300 hover:border-green-500'
                  }`}
                >
                  <div className="font-medium">
                    {categoryLabels[category] || category}
                  </div>
                </button>
              ))}
            </div>
          </div>

          <div className="flex justify-between">
            <button
              type="button"
              onClick={() => router.back()}
              className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50 transition-colors"
            >
              Retour
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? 'Enregistrement...' : 'Enregistrer'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}