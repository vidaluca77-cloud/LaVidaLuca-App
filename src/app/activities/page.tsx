'use client';

import React, { useState } from 'react';
import { ActivityCard } from '@/components/ActivityCard';
import { BookingSystem } from '@/components/BookingSystem';
import { Button, Card, CardContent, CardHeader, CardTitle, Badge } from '@/components/ui';
import { Activity, Booking } from '@/types';

// Sample activities data
const ACTIVITIES: Activity[] = [
  {
    id: '1',
    slug: 'nourrir-soigner-moutons',
    title: 'Nourrir et soigner les moutons',
    category: 'agri',
    summary: 'Gestes quotidiens : alimentation, eau, observation.',
    duration_min: 60,
    skill_tags: ['elevage', 'responsabilite'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['bottes', 'gants']
  },
  {
    id: '2',
    slug: 'fromage',
    title: 'Fabrication de fromage',
    category: 'transfo',
    summary: 'Du lait au caillé : hygiène, moulage, affinage (découverte).',
    duration_min: 90,
    skill_tags: ['hygiene', 'precision'],
    seasonality: ['toutes'],
    safety_level: 2,
    materials: ['tablier']
  },
  {
    id: '3',
    slug: 'menuiserie-reparations',
    title: 'Menuiserie & réparations',
    category: 'artisanat',
    summary: 'Techniques de base, outils, sécurité, finitions.',
    duration_min: 120,
    skill_tags: ['bois', 'precision', 'securite'],
    seasonality: ['toutes'],
    safety_level: 3,
    materials: ['gants', 'lunettes']
  },
  {
    id: '4',
    slug: 'entretien-riviere',
    title: 'Entretien de la rivière',
    category: 'nature',
    summary: 'Nettoyage doux, observation des berges.',
    duration_min: 90,
    skill_tags: ['prudence', 'ecologie'],
    seasonality: ['printemps', 'ete'],
    safety_level: 2,
    materials: ['bottes', 'gants']
  },
  {
    id: '5',
    slug: 'portes-ouvertes',
    title: 'Journée portes ouvertes',
    category: 'social',
    summary: 'Préparer, accueillir, guider un public.',
    duration_min: 180,
    skill_tags: ['accueil', 'organisation'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: []
  },
  {
    id: '6',
    slug: 'plantation-cultures',
    title: 'Plantation de cultures',
    category: 'agri',
    summary: 'Semis, arrosage, paillage, suivi de plants.',
    duration_min: 90,
    skill_tags: ['sol', 'plantes'],
    seasonality: ['printemps', 'ete'],
    safety_level: 1,
    materials: ['gants']
  }
];

export default function ActivitiesPage() {
  const [selectedActivity, setSelectedActivity] = useState<Activity | null>(null);
  const [showBooking, setShowBooking] = useState(false);
  const [filter, setFilter] = useState<string>('all');

  const handleBookActivity = (activity: Activity) => {
    setSelectedActivity(activity);
    setShowBooking(true);
  };

  const handleViewDetails = (activity: Activity) => {
    setSelectedActivity(activity);
    setShowBooking(false);
  };

  const handleBookingComplete = (booking: Booking) => {
    console.log('Booking completed:', booking);
    setShowBooking(false);
    setSelectedActivity(null);
  };

  const categories = [
    { value: 'all', label: 'Toutes les activités' },
    { value: 'agri', label: 'Agriculture' },
    { value: 'transfo', label: 'Transformation' },
    { value: 'artisanat', label: 'Artisanat' },
    { value: 'nature', label: 'Nature' },
    { value: 'social', label: 'Social' }
  ];

  const filteredActivities = filter === 'all' 
    ? ACTIVITIES 
    : ACTIVITIES.filter(activity => activity.category === filter);

  if (showBooking && selectedActivity) {
    return (
      <div className="max-w-2xl mx-auto">
        <BookingSystem
          activity={selectedActivity}
          onBookingComplete={handleBookingComplete}
          onCancel={() => {
            setShowBooking(false);
            setSelectedActivity(null);
          }}
        />
      </div>
    );
  }

  if (selectedActivity && !showBooking) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <Button
            variant="outline"
            onClick={() => setSelectedActivity(null)}
            className="mb-4"
          >
            ← Retour aux activités
          </Button>
        </div>
        
        <Card>
          <CardHeader>
            <div className="flex items-start justify-between">
              <div>
                <CardTitle className="text-2xl mb-2">{selectedActivity.title}</CardTitle>
                <div className="flex items-center gap-2 mb-4">
                  <Badge variant="secondary">{selectedActivity.category}</Badge>
                  <Badge variant="outline">
                    {Math.floor(selectedActivity.duration_min / 60)}h{selectedActivity.duration_min % 60 > 0 ? selectedActivity.duration_min % 60 + 'min' : ''}
                  </Badge>
                  <Badge variant={selectedActivity.safety_level > 2 ? 'destructive' : selectedActivity.safety_level > 1 ? 'warning' : 'success'}>
                    Niveau {selectedActivity.safety_level}
                  </Badge>
                </div>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <h3 className="font-semibold mb-2">Description</h3>
              <p className="text-gray-600">{selectedActivity.summary}</p>
            </div>

            {selectedActivity.skill_tags.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Compétences développées</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedActivity.skill_tags.map((skill, index) => (
                    <Badge key={index} variant="outline">{skill}</Badge>
                  ))}
                </div>
              </div>
            )}

            {selectedActivity.materials.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Matériel nécessaire</h3>
                <ul className="list-disc list-inside text-gray-600">
                  {selectedActivity.materials.map((material, index) => (
                    <li key={index}>{material}</li>
                  ))}
                </ul>
              </div>
            )}

            {selectedActivity.seasonality.length > 0 && !selectedActivity.seasonality.includes('toutes') && (
              <div>
                <h3 className="font-semibold mb-2">Saisons recommandées</h3>
                <div className="flex flex-wrap gap-2">
                  {selectedActivity.seasonality.map((season, index) => (
                    <Badge key={index} variant="outline">{season}</Badge>
                  ))}
                </div>
              </div>
            )}

            <div className="flex gap-3 pt-4">
              <Button
                onClick={() => handleBookActivity(selectedActivity)}
                className="flex-1"
              >
                Réserver cette activité
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Activités disponibles</h1>
        <p className="text-gray-600">Découvrez et réservez nos activités pédagogiques</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        {categories.map(category => (
          <Button
            key={category.value}
            variant={filter === category.value ? 'primary' : 'outline'}
            size="sm"
            onClick={() => setFilter(category.value)}
          >
            {category.label}
          </Button>
        ))}
      </div>

      {/* Activities Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredActivities.map(activity => (
          <ActivityCard
            key={activity.id}
            activity={activity}
            onBook={handleBookActivity}
            onViewDetails={handleViewDetails}
          />
        ))}
      </div>

      {filteredActivities.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">Aucune activité trouvée pour cette catégorie.</p>
        </div>
      )}
    </div>
  );
}