'use client';

import React, { useState } from 'react';
import { UserIcon, MapPinIcon, CalendarIcon, CogIcon } from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle, Badge, Button, Input } from '@/components/ui';
import { UserProfile } from '@/types';
import { useAuth } from '@/contexts/AuthContext';

interface ProfileSectionProps {
  profile: UserProfile;
  onUpdateProfile: (profile: UserProfile) => Promise<void>;
  editable?: boolean;
}

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
  { id: 'transfo', name: 'Transformation', desc: 'Fromage, conserves, artisanat alimentaire' },
  { id: 'artisanat', name: 'Artisanat', desc: 'Bois, construction, réparations' },
  { id: 'nature', name: 'Nature', desc: 'Écologie, environnement, biodiversité' },
  { id: 'social', name: 'Social', desc: 'Accueil, animation, transmission' }
];

export function ProfileSection({ profile, onUpdateProfile, editable = true }: ProfileSectionProps) {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [editedProfile, setEditedProfile] = useState<UserProfile>(profile);
  const [isLoading, setIsLoading] = useState(false);

  const handleSave = async () => {
    if (!editable) return;
    
    setIsLoading(true);
    try {
      await onUpdateProfile(editedProfile);
      setIsEditing(false);
    } catch (error) {
      console.error('Failed to update profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setEditedProfile(profile);
    setIsEditing(false);
  };

  const toggleSkill = (skill: string) => {
    setEditedProfile(prev => ({
      ...prev,
      skills: prev.skills.includes(skill)
        ? prev.skills.filter(s => s !== skill)
        : [...prev.skills, skill]
    }));
  };

  const toggleAvailability = (availability: string) => {
    setEditedProfile(prev => ({
      ...prev,
      availability: prev.availability.includes(availability)
        ? prev.availability.filter(a => a !== availability)
        : [...prev.availability, availability]
    }));
  };

  const togglePreference = (preference: string) => {
    setEditedProfile(prev => ({
      ...prev,
      preferences: prev.preferences.includes(preference)
        ? prev.preferences.filter(p => p !== preference)
        : [...prev.preferences, preference]
    }));
  };

  if (isEditing) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <UserIcon className="w-5 h-5" />
            Modifier mon profil
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Basic Info */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Nom"
              value={editedProfile.name || ''}
              onChange={(e) => setEditedProfile(prev => ({ ...prev, name: e.target.value }))}
              placeholder="Votre nom"
            />
            <Input
              label="Localisation"
              value={editedProfile.location}
              onChange={(e) => setEditedProfile(prev => ({ ...prev, location: e.target.value }))}
              placeholder="Ville, région"
            />
          </div>

          {/* Skills */}
          <div>
            <h3 className="font-medium mb-3">Compétences et intérêts</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
              {skillsList.map(skill => (
                <label key={skill} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={editedProfile.skills.includes(skill)}
                    onChange={() => toggleSkill(skill)}
                    className="rounded border-gray-300 text-vida-500 focus:ring-vida-500"
                  />
                  <span className="text-sm">{skill}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Availability */}
          <div>
            <h3 className="font-medium mb-3">Disponibilités</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {availabilityOptions.map(option => (
                <label key={option} className="flex items-center space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={editedProfile.availability.includes(option)}
                    onChange={() => toggleAvailability(option)}
                    className="rounded border-gray-300 text-vida-500 focus:ring-vida-500"
                  />
                  <span className="text-sm">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Preferences */}
          <div>
            <h3 className="font-medium mb-3">Préférences d'activités</h3>
            <div className="space-y-2">
              {categoryOptions.map(category => (
                <label key={category.id} className="flex items-start space-x-2 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={editedProfile.preferences.includes(category.id)}
                    onChange={() => togglePreference(category.id)}
                    className="rounded border-gray-300 text-vida-500 focus:ring-vida-500 mt-0.5"
                  />
                  <div>
                    <span className="text-sm font-medium">{category.name}</span>
                    <p className="text-xs text-gray-500">{category.desc}</p>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-3 pt-4">
            <Button
              onClick={handleSave}
              loading={isLoading}
              className="flex-1"
            >
              Sauvegarder
            </Button>
            <Button
              variant="outline"
              onClick={handleCancel}
              disabled={isLoading}
            >
              Annuler
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <UserIcon className="w-5 h-5" />
            Mon profil
          </CardTitle>
          {editable && (
            <Button variant="ghost" size="sm" onClick={() => setIsEditing(true)}>
              <CogIcon className="w-4 h-4 mr-1" />
              Modifier
            </Button>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Basic Info */}
        <div className="space-y-2">
          {user?.name && (
            <div className="flex items-center gap-2">
              <UserIcon className="w-4 h-4 text-gray-500" />
              <span className="font-medium">{user.name}</span>
            </div>
          )}
          {profile.location && (
            <div className="flex items-center gap-2">
              <MapPinIcon className="w-4 h-4 text-gray-500" />
              <span>{profile.location}</span>
            </div>
          )}
          {profile.experience_level && (
            <div className="flex items-center gap-2">
              <Badge variant="outline">
                Niveau: {profile.experience_level}
              </Badge>
            </div>
          )}
        </div>

        {/* Skills */}
        {profile.skills.length > 0 && (
          <div>
            <h3 className="font-medium text-sm text-gray-500 mb-2">Compétences</h3>
            <div className="flex flex-wrap gap-1">
              {profile.skills.slice(0, 8).map((skill, index) => (
                <Badge key={index} variant="secondary" size="sm">
                  {skill}
                </Badge>
              ))}
              {profile.skills.length > 8 && (
                <Badge variant="outline" size="sm">
                  +{profile.skills.length - 8}
                </Badge>
              )}
            </div>
          </div>
        )}

        {/* Availability */}
        {profile.availability.length > 0 && (
          <div>
            <h3 className="font-medium text-sm text-gray-500 mb-2">Disponibilités</h3>
            <div className="flex flex-wrap gap-1">
              {profile.availability.map((item, index) => (
                <Badge key={index} variant="outline" size="sm">
                  <CalendarIcon className="w-3 h-3 mr-1" />
                  {item}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Preferences */}
        {profile.preferences.length > 0 && (
          <div>
            <h3 className="font-medium text-sm text-gray-500 mb-2">Préférences</h3>
            <div className="flex flex-wrap gap-1">
              {profile.preferences.map((pref, index) => {
                const category = categoryOptions.find(c => c.id === pref);
                return (
                  <Badge key={index} variant="success" size="sm">
                    {category?.name || pref}
                  </Badge>
                );
              })}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}