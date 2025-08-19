// src/app/profile/page.tsx
'use client';

import { useState } from 'react';
import { Card, CardHeader, CardTitle, Button, Input } from '@/components/ui';
import { 
  UserIcon, 
  EnvelopeIcon, 
  PhoneIcon,
  MapPinIcon,
  PencilIcon 
} from '@heroicons/react/24/outline';

export default function ProfilePage() {
  const [isEditing, setIsEditing] = useState(false);
  const [profile, setProfile] = useState({
    fullName: 'Marie Dubois',
    email: 'marie.dubois@email.com',
    phone: '06 12 34 56 78',
    location: 'Caen, Calvados (14)',
    bio: 'Étudiante en MFR passionnée par l\'agriculture durable et l\'environnement. Je souhaite me spécialiser dans l\'agroécologie.',
    skills: ['Agriculture biologique', 'Soins aux animaux', 'Maraîchage'],
    availability: ['Mercredi après-midi', 'Weekend'],
    preferences: ['Agriculture', 'Environnement']
  });

  const handleSave = () => {
    // TODO: Save to Supabase
    setIsEditing(false);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Mon profil</h1>
        <Button 
          variant={isEditing ? 'primary' : 'outline'}
          onClick={isEditing ? handleSave : () => setIsEditing(true)}
        >
          {isEditing ? 'Enregistrer' : (
            <>
              <PencilIcon className="w-4 h-4 mr-2" />
              Modifier
            </>
          )}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Profile Card */}
        <div className="lg:col-span-1">
          <Card>
            <div className="text-center">
              <div className="w-24 h-24 bg-gray-200 rounded-full mx-auto mb-4 flex items-center justify-center">
                <UserIcon className="w-12 h-12 text-gray-400" />
              </div>
              <h2 className="text-xl font-bold text-gray-900">{profile.fullName}</h2>
              <p className="text-gray-600">Élève MFR</p>
              
              <div className="mt-6 space-y-3 text-left">
                <div className="flex items-center text-sm text-gray-600">
                  <EnvelopeIcon className="w-4 h-4 mr-3 flex-shrink-0" />
                  {profile.email}
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <PhoneIcon className="w-4 h-4 mr-3 flex-shrink-0" />
                  {profile.phone}
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <MapPinIcon className="w-4 h-4 mr-3 flex-shrink-0" />
                  {profile.location}
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* Personal Information */}
          <Card>
            <CardHeader>
              <CardTitle>Informations personnelles</CardTitle>
            </CardHeader>
            
            {isEditing ? (
              <div className="space-y-4">
                <Input
                  label="Nom complet"
                  value={profile.fullName}
                  onChange={(value) => setProfile(prev => ({ ...prev, fullName: value }))}
                />
                <Input
                  label="Email"
                  type="email"
                  value={profile.email}
                  onChange={(value) => setProfile(prev => ({ ...prev, email: value }))}
                />
                <Input
                  label="Téléphone"
                  value={profile.phone}
                  onChange={(value) => setProfile(prev => ({ ...prev, phone: value }))}
                />
                <Input
                  label="Localisation"
                  value={profile.location}
                  onChange={(value) => setProfile(prev => ({ ...prev, location: value }))}
                />
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Biographie
                  </label>
                  <textarea
                    value={profile.bio}
                    onChange={(e) => setProfile(prev => ({ ...prev, bio: e.target.value }))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-vida-green focus:border-transparent"
                    rows={4}
                    placeholder="Parlez-nous de vous..."
                  />
                </div>
              </div>
            ) : (
              <div>
                <h3 className="font-medium text-gray-900 mb-2">À propos</h3>
                <p className="text-gray-600 leading-relaxed">{profile.bio}</p>
              </div>
            )}
          </Card>

          {/* Skills */}
          <Card>
            <CardHeader>
              <CardTitle>Compétences</CardTitle>
            </CardHeader>
            <div className="flex flex-wrap gap-2">
              {profile.skills.map((skill, index) => (
                <span 
                  key={index}
                  className="bg-vida-green/10 text-vida-green px-3 py-1 rounded-full text-sm font-medium"
                >
                  {skill}
                </span>
              ))}
            </div>
          </Card>

          {/* Availability */}
          <Card>
            <CardHeader>
              <CardTitle>Disponibilités</CardTitle>
            </CardHeader>
            <div className="flex flex-wrap gap-2">
              {profile.availability.map((time, index) => (
                <span 
                  key={index}
                  className="bg-vida-earth/10 text-vida-earth px-3 py-1 rounded-full text-sm font-medium"
                >
                  {time}
                </span>
              ))}
            </div>
          </Card>

          {/* Preferences */}
          <Card>
            <CardHeader>
              <CardTitle>Préférences d'activités</CardTitle>
            </CardHeader>
            <div className="flex flex-wrap gap-2">
              {profile.preferences.map((pref, index) => (
                <span 
                  key={index}
                  className="bg-vida-sky/10 text-vida-sky px-3 py-1 rounded-full text-sm font-medium"
                >
                  {pref}
                </span>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}