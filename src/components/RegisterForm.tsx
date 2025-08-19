'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { apiClient } from '@/lib/api';

interface RegisterFormProps {
  onSuccess?: () => void;
  onSwitchToLogin?: () => void;
}

interface FormData {
  email: string;
  username: string;
  password: string;
  confirmPassword: string;
  first_name: string;
  last_name: string;
  bio: string;
  location: string;
  phone: string;
  skills: string[];
  preferences: string[];
  availability: string[];
}

export default function RegisterForm({ onSuccess, onSwitchToLogin }: RegisterFormProps) {
  const { register } = useAuth();
  const [formData, setFormData] = useState<FormData>({
    email: '',
    username: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    bio: '',
    location: '',
    phone: '',
    skills: [],
    preferences: [],
    availability: [],
  });
  
  const [availableSkills, setAvailableSkills] = useState<Array<{id: string; name: string}>>([]);
  const [categories, setCategories] = useState<Array<{id: string; name: string}>>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(1);

  useEffect(() => {
    // Load available skills and categories
    loadOptions();
  }, []);

  const loadOptions = async () => {
    try {
      const [skillsResponse, categoriesResponse] = await Promise.all([
        apiClient.getSkills(),
        apiClient.getCategories(),
      ]);

      if (skillsResponse.data) {
        setAvailableSkills(skillsResponse.data.skills);
      }
      
      if (categoriesResponse.data) {
        setCategories(categoriesResponse.data.categories);
      }
    } catch (error) {
      console.error('Failed to load options:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (step < 3) {
      setStep(step + 1);
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError('Les mots de passe ne correspondent pas');
      return;
    }

    setLoading(true);
    setError('');

    const { confirmPassword, ...registerData } = formData;
    const result = await register(registerData);
    
    if (result.success) {
      onSuccess?.();
    } else {
      setError(result.error || 'Inscription échouée');
    }
    
    setLoading(false);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleMultiSelect = (name: keyof FormData, value: string) => {
    setFormData(prev => {
      const currentArray = prev[name] as string[];
      const newArray = currentArray.includes(value)
        ? currentArray.filter(item => item !== value)
        : [...currentArray, value];
      
      return {
        ...prev,
        [name]: newArray,
      };
    });
  };

  const availabilityOptions = [
    { id: 'weekend', name: 'Week-end' },
    { id: 'semaine', name: 'Semaine' },
    { id: 'matin', name: 'Matin' },
    { id: 'apres-midi', name: 'Après-midi' },
    { id: 'vacances', name: 'Vacances scolaires' },
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Step 1: Basic Information */}
      {step === 1 && (
        <>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="first_name" className="block text-sm font-medium text-gray-700 mb-1">
                Prénom *
              </label>
              <input
                type="text"
                id="first_name"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
              />
            </div>
            
            <div>
              <label htmlFor="last_name" className="block text-sm font-medium text-gray-700 mb-1">
                Nom *
              </label>
              <input
                type="text"
                id="last_name"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
              />
            </div>
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email *
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
            />
          </div>

          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
              Nom d'utilisateur *
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Mot de passe *
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
              />
            </div>
            
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                Confirmer le mot de passe *
              </label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
              />
            </div>
          </div>
        </>
      )}

      {/* Step 2: Profile Information */}
      {step === 2 && (
        <>
          <div>
            <label htmlFor="bio" className="block text-sm font-medium text-gray-700 mb-1">
              Présentation
            </label>
            <textarea
              id="bio"
              name="bio"
              value={formData.bio}
              onChange={handleChange}
              rows={3}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
              placeholder="Parlez-nous de vous et de vos motivations..."
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-1">
                Localisation
              </label>
              <input
                type="text"
                id="location"
                name="location"
                value={formData.location}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
                placeholder="Région, département..."
              />
            </div>
            
            <div>
              <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">
                Téléphone
              </label>
              <input
                type="tel"
                id="phone"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-vida-green focus:border-vida-green"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Catégories d'activités préférées
            </label>
            <div className="grid grid-cols-2 gap-2">
              {categories.map((category) => (
                <label key={category.id} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.preferences.includes(category.id)}
                    onChange={() => handleMultiSelect('preferences', category.id)}
                    className="rounded border-gray-300 text-vida-green focus:ring-vida-green"
                  />
                  <span className="ml-2 text-sm text-gray-700">{category.name}</span>
                </label>
              ))}
            </div>
          </div>
        </>
      )}

      {/* Step 3: Skills and Availability */}
      {step === 3 && (
        <>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Compétences actuelles
            </label>
            <div className="grid grid-cols-2 gap-2 max-h-40 overflow-y-auto">
              {availableSkills.map((skill) => (
                <label key={skill.id} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.skills.includes(skill.id)}
                    onChange={() => handleMultiSelect('skills', skill.id)}
                    className="rounded border-gray-300 text-vida-green focus:ring-vida-green"
                  />
                  <span className="ml-2 text-sm text-gray-700">{skill.name}</span>
                </label>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Disponibilités
            </label>
            <div className="grid grid-cols-2 gap-2">
              {availabilityOptions.map((option) => (
                <label key={option.id} className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.availability.includes(option.id)}
                    onChange={() => handleMultiSelect('availability', option.id)}
                    className="rounded border-gray-300 text-vida-green focus:ring-vida-green"
                  />
                  <span className="ml-2 text-sm text-gray-700">{option.name}</span>
                </label>
              ))}
            </div>
          </div>
        </>
      )}

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-md">
          <p className="text-sm text-red-600">{error}</p>
        </div>
      )}

      <div className="flex justify-between">
        {step > 1 && (
          <button
            type="button"
            onClick={() => setStep(step - 1)}
            className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
          >
            Précédent
          </button>
        )}
        
        <button
          type="submit"
          disabled={loading}
          className="ml-auto bg-vida-green text-white py-2 px-4 rounded-md hover:bg-vida-green/90 focus:outline-none focus:ring-2 focus:ring-vida-green focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Inscription...' : step < 3 ? 'Suivant' : 'S\'inscrire'}
        </button>
      </div>

      <div className="flex justify-center space-x-2 mt-4">
        {[1, 2, 3].map((stepNumber) => (
          <div
            key={stepNumber}
            className={`w-3 h-3 rounded-full ${
              stepNumber <= step ? 'bg-vida-green' : 'bg-gray-200'
            }`}
          />
        ))}
      </div>

      {onSwitchToLogin && (
        <div className="text-center">
          <p className="text-sm text-gray-600">
            Déjà un compte ?{' '}
            <button
              type="button"
              onClick={onSwitchToLogin}
              className="text-vida-green hover:text-vida-green/80 font-medium"
            >
              Se connecter
            </button>
          </p>
        </div>
      )}
    </form>
  );
}