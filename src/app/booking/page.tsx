// src/app/booking/page.tsx
'use client';

import { useState } from 'react';
import { Card, CardHeader, CardTitle, Button, Input } from '@/components/ui';
import { 
  CalendarDaysIcon, 
  ClockIcon, 
  UserIcon,
  MapPinIcon,
  StarIcon 
} from '@heroicons/react/24/outline';

const activities = [
  {
    id: '1',
    title: 'Soins aux animaux',
    description: 'Apprendre les gestes essentiels pour s\'occuper des animaux de la ferme.',
    duration: 120,
    supervisor: 'Marie Dupont',
    farm: 'Ferme de la Vallée Verte',
    location: 'Calvados (14)',
    difficulty: 'Débutant',
    available_slots: [
      { date: '2024-01-20', time: '09:00' },
      { date: '2024-01-20', time: '14:00' },
      { date: '2024-01-22', time: '09:00' },
      { date: '2024-01-25', time: '14:00' },
    ]
  },
  {
    id: '2',
    title: 'Plantation de cultures',
    description: 'Semis, arrosage, paillage et suivi des plants selon les principes de l\'agriculture biologique.',
    duration: 90,
    supervisor: 'Jean Martin',
    farm: 'Domaine des Chênes',
    location: 'Ille-et-Vilaine (35)',
    difficulty: 'Débutant',
    available_slots: [
      { date: '2024-01-21', time: '10:00' },
      { date: '2024-01-23', time: '14:00' },
      { date: '2024-01-26', time: '09:00' },
    ]
  },
  {
    id: '3',
    title: 'Fabrication de fromage',
    description: 'Du lait au caillé : découverte des techniques d\'hygiène, moulage et affinage.',
    duration: 90,
    supervisor: 'Sophie Durand',
    farm: 'Ferme du Soleil Levant',
    location: 'Vaucluse (84)',
    difficulty: 'Intermédiaire',
    available_slots: [
      { date: '2024-01-24', time: '08:00' },
      { date: '2024-01-27', time: '13:00' },
    ]
  }
];

export default function BookingPage() {
  const [selectedActivity, setSelectedActivity] = useState<string | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<{ date: string; time: string } | null>(null);
  const [step, setStep] = useState<'activities' | 'slots' | 'confirm'>('activities');
  const [notes, setNotes] = useState('');

  const selectedActivityData = activities.find(a => a.id === selectedActivity);

  const handleActivitySelect = (activityId: string) => {
    setSelectedActivity(activityId);
    setStep('slots');
  };

  const handleSlotSelect = (slot: { date: string; time: string }) => {
    setSelectedSlot(slot);
    setStep('confirm');
  };

  const handleConfirm = () => {
    // TODO: Save booking to database
    alert('Réservation confirmée ! Un email de confirmation vous sera envoyé.');
    // Reset form
    setSelectedActivity(null);
    setSelectedSlot(null);
    setStep('activities');
    setNotes('');
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Réserver une activité</h1>
        <p className="text-gray-600 mt-2">
          Choisissez une activité et réservez votre créneau avec un encadrant
        </p>
      </div>

      {/* Progress Steps */}
      <div className="flex items-center justify-center space-x-8">
        <div className={`flex items-center ${step === 'activities' ? 'text-vida-green' : 'text-gray-400'}`}>
          <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center ${
            step === 'activities' ? 'border-vida-green bg-vida-green text-white' : 'border-gray-300'
          }`}>
            1
          </div>
          <span className="ml-2 font-medium">Activité</span>
        </div>
        <div className={`w-16 h-px ${step === 'slots' || step === 'confirm' ? 'bg-vida-green' : 'bg-gray-300'}`} />
        <div className={`flex items-center ${step === 'slots' ? 'text-vida-green' : step === 'confirm' ? 'text-vida-green' : 'text-gray-400'}`}>
          <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center ${
            step === 'slots' || step === 'confirm' ? 'border-vida-green bg-vida-green text-white' : 'border-gray-300'
          }`}>
            2
          </div>
          <span className="ml-2 font-medium">Créneaux</span>
        </div>
        <div className={`w-16 h-px ${step === 'confirm' ? 'bg-vida-green' : 'bg-gray-300'}`} />
        <div className={`flex items-center ${step === 'confirm' ? 'text-vida-green' : 'text-gray-400'}`}>
          <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center ${
            step === 'confirm' ? 'border-vida-green bg-vida-green text-white' : 'border-gray-300'
          }`}>
            3
          </div>
          <span className="ml-2 font-medium">Confirmation</span>
        </div>
      </div>

      {step === 'activities' && (
        <div className="space-y-6">
          <h2 className="text-xl font-semibold text-gray-900">Choisissez une activité</h2>
          <div className="grid gap-6">
            {activities.map((activity) => (
              <div key={activity.id} className="cursor-pointer" onClick={() => handleActivitySelect(activity.id)}>
                <Card hover>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-900 mb-2">{activity.title}</h3>
                      <p className="text-gray-600 mb-4">{activity.description}</p>
                      
                      <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                        <div className="flex items-center">
                          <ClockIcon className="w-4 h-4 mr-1" />
                          {activity.duration} min
                        </div>
                        <div className="flex items-center">
                          <UserIcon className="w-4 h-4 mr-1" />
                          {activity.supervisor}
                        </div>
                        <div className="flex items-center">
                          <MapPinIcon className="w-4 h-4 mr-1" />
                          {activity.farm}, {activity.location}
                        </div>
                        <span className="bg-vida-green/10 text-vida-green px-2 py-1 rounded-full text-xs">
                          {activity.difficulty}
                        </span>
                      </div>
                    </div>
                    <Button variant="outline">
                      Réserver
                    </Button>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </div>
      )}

      {step === 'slots' && selectedActivityData && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">Choisissez un créneau</h2>
            <Button variant="ghost" onClick={() => setStep('activities')}>
              ← Retour aux activités
            </Button>
          </div>
          
          <Card>
            <h3 className="font-semibold text-gray-900 mb-2">{selectedActivityData.title}</h3>
            <p className="text-gray-600 text-sm">{selectedActivityData.description}</p>
          </Card>

          <div className="grid gap-4 md:grid-cols-2">
            {selectedActivityData.available_slots.map((slot, index) => (
              <div 
                key={index} 
                className="cursor-pointer" 
                onClick={() => handleSlotSelect(slot)}
              >
                <Card hover>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="flex items-center text-gray-900 font-medium">
                        <CalendarDaysIcon className="w-4 h-4 mr-2" />
                        {formatDate(slot.date)}
                      </div>
                      <div className="flex items-center text-gray-600 mt-1">
                        <ClockIcon className="w-4 h-4 mr-2" />
                        {slot.time} - {parseInt(slot.time.split(':')[0]) + Math.floor(selectedActivityData.duration / 60)}:{String((parseInt(slot.time.split(':')[1]) + selectedActivityData.duration % 60) % 60).padStart(2, '0')}
                      </div>
                    </div>
                    <Button size="sm">
                      Choisir
                    </Button>
                  </div>
                </Card>
              </div>
            ))}
          </div>
        </div>
      )}

      {step === 'confirm' && selectedActivityData && selectedSlot && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">Confirmer la réservation</h2>
            <Button variant="ghost" onClick={() => setStep('slots')}>
              ← Modifier le créneau
            </Button>
          </div>

          <Card>
            <CardHeader>
              <CardTitle>Récapitulatif de votre réservation</CardTitle>
            </CardHeader>
            
            <div className="space-y-4">
              <div>
                <h4 className="font-medium text-gray-900">Activité</h4>
                <p className="text-gray-600">{selectedActivityData.title}</p>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900">Date et heure</h4>
                <p className="text-gray-600">
                  {formatDate(selectedSlot.date)} à {selectedSlot.time}
                </p>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900">Durée</h4>
                <p className="text-gray-600">{selectedActivityData.duration} minutes</p>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900">Encadrant</h4>
                <p className="text-gray-600">{selectedActivityData.supervisor}</p>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900">Lieu</h4>
                <p className="text-gray-600">{selectedActivityData.farm}, {selectedActivityData.location}</p>
              </div>
            </div>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Notes (optionnel)</CardTitle>
            </CardHeader>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Ajoutez des notes ou des demandes particulières..."
              className="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-vida-green focus:border-transparent"
              rows={4}
            />
          </Card>

          <div className="flex gap-4">
            <Button variant="outline" onClick={() => setStep('activities')} className="flex-1">
              Annuler
            </Button>
            <Button onClick={handleConfirm} className="flex-1">
              Confirmer la réservation
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}