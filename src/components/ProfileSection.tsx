import React, { useState } from 'react';
import { User, UserProfile } from '@/types';
import { Card, CardHeader, CardContent, Button, Input, LoadingOverlay } from '@/components/ui';
import { useAuth, useNotification } from '@/context';
import { api } from '@/services/api';
import { UserIcon, PencilIcon, CheckIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface ProfileSectionProps {
  className?: string;
}

export const ProfileSection: React.FC<ProfileSectionProps> = ({ className }) => {
  const { user } = useAuth();
  const { showSuccess, showError } = useNotification();
  const [isEditing, setIsEditing] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<Partial<UserProfile>>({
    skills: user?.profile?.skills || [],
    availability: user?.profile?.availability || [],
    location: user?.profile?.location || '',
    preferences: user?.profile?.preferences || [],
    bio: user?.profile?.bio || '',
    phone: user?.profile?.phone || '',
  });

  const handleSave = async () => {
    setIsLoading(true);
    try {
      const result = await api.updateProfile(formData);
      if (result.data) {
        showSuccess('Profil mis à jour avec succès');
        setIsEditing(false);
      } else {
        showError(result.error || 'Erreur lors de la mise à jour du profil');
      }
    } catch (error) {
      showError('Erreur lors de la mise à jour du profil');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      skills: user?.profile?.skills || [],
      availability: user?.profile?.availability || [],
      location: user?.profile?.location || '',
      preferences: user?.profile?.preferences || [],
      bio: user?.profile?.bio || '',
      phone: user?.profile?.phone || '',
    });
    setIsEditing(false);
  };

  const handleInputChange = (field: keyof UserProfile, value: string | string[]) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
  };

  const addSkill = (skill: string) => {
    if (skill && !formData.skills?.includes(skill)) {
      handleInputChange('skills', [...(formData.skills || []), skill]);
    }
  };

  const removeSkill = (skillToRemove: string) => {
    handleInputChange('skills', formData.skills?.filter(skill => skill !== skillToRemove) || []);
  };

  const availabilityOptions = [
    { value: 'semaine', label: 'Semaine' },
    { value: 'weekend', label: 'Weekend' },
    { value: 'soir', label: 'Soirée' },
    { value: 'matin', label: 'Matin' },
  ];

  const preferencesOptions = [
    { value: 'agri', label: 'Agriculture' },
    { value: 'transfo', label: 'Transformation' },
    { value: 'artisanat', label: 'Artisanat' },
    { value: 'nature', label: 'Environnement' },
    { value: 'social', label: 'Animation' },
  ];

  if (!user) {
    return (
      <Card className={className}>
        <CardContent>
          <p className="text-gray-500 text-center py-8">
            Connectez-vous pour voir votre profil
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <LoadingOverlay isLoading={isLoading}>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <div className="bg-primary-100 p-3 rounded-full">
                <UserIcon className="h-6 w-6 text-primary-600" />
              </div>
              <div className="ml-4">
                <h3 className="text-lg font-semibold text-gray-900">{user.name}</h3>
                <p className="text-sm text-gray-500">{user.email}</p>
              </div>
            </div>
            {!isEditing ? (
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsEditing(true)}
              >
                <PencilIcon className="h-4 w-4 mr-2" />
                Modifier
              </Button>
            ) : (
              <div className="flex gap-2">
                <Button
                  variant="primary"
                  size="sm"
                  onClick={handleSave}
                >
                  <CheckIcon className="h-4 w-4 mr-2" />
                  Sauvegarder
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleCancel}
                >
                  <XMarkIcon className="h-4 w-4 mr-2" />
                  Annuler
                </Button>
              </div>
            )}
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Bio */}
          <div>
            <label className="form-label">Présentation</label>
            {isEditing ? (
              <textarea
                value={formData.bio || ''}
                onChange={(e) => handleInputChange('bio', e.target.value)}
                className="form-input min-h-[100px] resize-none"
                placeholder="Parlez-nous de vous..."
              />
            ) : (
              <p className="text-gray-600 text-sm">
                {user.profile?.bio || 'Aucune présentation ajoutée'}
              </p>
            )}
          </div>

          {/* Location */}
          <div>
            <label className="form-label">Localisation</label>
            {isEditing ? (
              <Input
                value={formData.location || ''}
                onChange={(e) => handleInputChange('location', e.target.value)}
                placeholder="Votre région ou ville"
              />
            ) : (
              <p className="text-gray-600 text-sm">
                {user.profile?.location || 'Non renseignée'}
              </p>
            )}
          </div>

          {/* Phone */}
          <div>
            <label className="form-label">Téléphone</label>
            {isEditing ? (
              <Input
                type="tel"
                value={formData.phone || ''}
                onChange={(e) => handleInputChange('phone', e.target.value)}
                placeholder="Votre numéro de téléphone"
              />
            ) : (
              <p className="text-gray-600 text-sm">
                {user.profile?.phone || 'Non renseigné'}
              </p>
            )}
          </div>

          {/* Availability */}
          <div>
            <label className="form-label">Disponibilités</label>
            {isEditing ? (
              <div className="space-y-2">
                {availabilityOptions.map(option => (
                  <label key={option.value} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.availability?.includes(option.value) || false}
                      onChange={(e) => {
                        const currentAvailability = formData.availability || [];
                        if (e.target.checked) {
                          handleInputChange('availability', [...currentAvailability, option.value]);
                        } else {
                          handleInputChange('availability', currentAvailability.filter(a => a !== option.value));
                        }
                      }}
                      className="mr-2 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="text-sm text-gray-700">{option.label}</span>
                  </label>
                ))}
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                {user.profile?.availability?.map(avail => (
                  <span key={avail} className="bg-primary-100 text-primary-800 px-2 py-1 rounded text-sm">
                    {availabilityOptions.find(opt => opt.value === avail)?.label || avail}
                  </span>
                )) || <span className="text-gray-500 text-sm">Aucune disponibilité renseignée</span>}
              </div>
            )}
          </div>

          {/* Preferences */}
          <div>
            <label className="form-label">Centres d'intérêt</label>
            {isEditing ? (
              <div className="space-y-2">
                {preferencesOptions.map(option => (
                  <label key={option.value} className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.preferences?.includes(option.value) || false}
                      onChange={(e) => {
                        const currentPreferences = formData.preferences || [];
                        if (e.target.checked) {
                          handleInputChange('preferences', [...currentPreferences, option.value]);
                        } else {
                          handleInputChange('preferences', currentPreferences.filter(p => p !== option.value));
                        }
                      }}
                      className="mr-2 rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                    />
                    <span className="text-sm text-gray-700">{option.label}</span>
                  </label>
                ))}
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                {user.profile?.preferences?.map(pref => (
                  <span key={pref} className="bg-vida-earth-100 text-vida-earth-800 px-2 py-1 rounded text-sm">
                    {preferencesOptions.find(opt => opt.value === pref)?.label || pref}
                  </span>
                )) || <span className="text-gray-500 text-sm">Aucun centre d'intérêt renseigné</span>}
              </div>
            )}
          </div>

          {/* Skills */}
          <div>
            <label className="form-label">Compétences</label>
            {isEditing ? (
              <div className="space-y-2">
                <div className="flex flex-wrap gap-2 mb-2">
                  {formData.skills?.map(skill => (
                    <span key={skill} className="bg-vida-green-100 text-vida-green-800 px-2 py-1 rounded text-sm flex items-center">
                      {skill}
                      <button
                        type="button"
                        onClick={() => removeSkill(skill)}
                        className="ml-1 text-vida-green-600 hover:text-vida-green-800"
                      >
                        <XMarkIcon className="h-3 w-3" />
                      </button>
                    </span>
                  ))}
                </div>
                <Input
                  placeholder="Ajouter une compétence (appuyez sur Entrée)"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter') {
                      e.preventDefault();
                      const target = e.target as HTMLInputElement;
                      addSkill(target.value.trim());
                      target.value = '';
                    }
                  }}
                />
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                {user.profile?.skills?.map(skill => (
                  <span key={skill} className="bg-vida-green-100 text-vida-green-800 px-2 py-1 rounded text-sm">
                    {skill}
                  </span>
                )) || <span className="text-gray-500 text-sm">Aucune compétence renseignée</span>}
              </div>
            )}
          </div>
        </CardContent>
      </LoadingOverlay>
    </Card>
  );
};