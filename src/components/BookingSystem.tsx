'use client';

import React, { useState } from 'react';
import { CalendarIcon, ClockIcon, ExclamationTriangleIcon, CheckCircleIcon } from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle, Button, Input } from '@/components/ui';
import { Activity, Booking } from '@/types';
import { apiClient } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';

interface BookingSystemProps {
  activity: Activity;
  onBookingComplete?: (booking: Booking) => void;
  onCancel?: () => void;
}

interface TimeSlot {
  id: string;
  date: string;
  time: string;
  available: boolean;
  capacity?: number;
  booked?: number;
}

export function BookingSystem({ activity, onBookingComplete, onCancel }: BookingSystemProps) {
  const { user, isAuthenticated } = useAuth();
  const [selectedDate, setSelectedDate] = useState('');
  const [selectedTime, setSelectedTime] = useState('');
  const [notes, setNotes] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  // Generate available time slots (this would normally come from an API)
  const generateTimeSlots = (): TimeSlot[] => {
    const slots: TimeSlot[] = [];
    const today = new Date();
    
    // Generate slots for the next 14 days
    for (let i = 1; i <= 14; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() + i);
      
      // Skip weekends for some activities
      if (activity.seasonality.includes('semaine') && (date.getDay() === 0 || date.getDay() === 6)) {
        continue;
      }
      
      // Generate morning and afternoon slots
      const dateStr = date.toISOString().split('T')[0];
      
      if (activity.skill_tags.includes('matin') || !activity.skill_tags.includes('apres-midi')) {
        slots.push({
          id: `${dateStr}-09:00`,
          date: dateStr,
          time: '09:00',
          available: Math.random() > 0.3, // 70% availability
          capacity: 8,
          booked: Math.floor(Math.random() * 5)
        });
      }
      
      if (activity.skill_tags.includes('apres-midi') || !activity.skill_tags.includes('matin')) {
        slots.push({
          id: `${dateStr}-14:00`,
          date: dateStr,
          time: '14:00',
          available: Math.random() > 0.2, // 80% availability
          capacity: 8,
          booked: Math.floor(Math.random() * 4)
        });
      }
    }
    
    return slots;
  };

  const [timeSlots] = useState<TimeSlot[]>(generateTimeSlots());

  const handleBooking = async () => {
    if (!isAuthenticated || !user) {
      setError('Vous devez être connecté pour réserver une activité.');
      return;
    }

    if (!selectedDate || !selectedTime) {
      setError('Veuillez sélectionner une date et une heure.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      const scheduledDate = `${selectedDate}T${selectedTime}:00`;
      const response = await apiClient.createBooking(activity.id, scheduledDate, notes);
      
      if (response.success) {
        setSuccess(true);
        onBookingComplete?.(response.data);
      } else {
        throw new Error(response.message || 'Erreur lors de la réservation');
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Erreur lors de la réservation';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('fr-FR', {
      weekday: 'long',
      day: 'numeric',
      month: 'long'
    });
  };

  const getAvailableDates = () => {
    const uniqueDates = new Set(timeSlots.map(slot => slot.date));
    const dates = Array.from(uniqueDates);
    return dates.sort();
  };

  const getAvailableTimesForDate = (date: string) => {
    return timeSlots.filter(slot => slot.date === date && slot.available);
  };

  if (success) {
    return (
      <Card>
        <CardContent className="p-6 text-center">
          <CheckCircleIcon className="w-16 h-16 text-green-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">Réservation confirmée !</h3>
          <p className="text-gray-600 mb-4">
            Votre réservation pour "{activity.title}" a été enregistrée.
          </p>
          <p className="text-sm text-gray-500 mb-6">
            Vous recevrez un email de confirmation avec tous les détails.
          </p>
          <div className="flex gap-3">
            <Button onClick={onCancel} className="flex-1">
              Retour aux activités
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!isAuthenticated) {
    return (
      <Card>
        <CardContent className="p-6 text-center">
          <ExclamationTriangleIcon className="w-16 h-16 text-vida-warm-500 mx-auto mb-4" />
          <h3 className="text-lg font-semibold mb-2">Connexion requise</h3>
          <p className="text-gray-600 mb-6">
            Vous devez être connecté pour réserver une activité.
          </p>
          <div className="flex gap-3">
            <Button variant="outline" onClick={onCancel} className="flex-1">
              Annuler
            </Button>
            <Button className="flex-1">
              Se connecter
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <CalendarIcon className="w-5 h-5" />
          Réserver: {activity.title}
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Activity Summary */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <h4 className="font-medium mb-2">Détails de l'activité</h4>
          <p className="text-sm text-gray-600 mb-2">{activity.summary}</p>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <div className="flex items-center gap-1">
              <ClockIcon className="w-4 h-4" />
              <span>{Math.floor(activity.duration_min / 60)}h{activity.duration_min % 60 > 0 ? activity.duration_min % 60 + 'min' : ''}</span>
            </div>
            {activity.materials.length > 0 && (
              <span>Matériel: {activity.materials.join(', ')}</span>
            )}
          </div>
        </div>

        {/* Date Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Choisir une date
          </label>
          <select
            value={selectedDate}
            onChange={(e) => {
              setSelectedDate(e.target.value);
              setSelectedTime(''); // Reset time when date changes
            }}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-vida-500"
          >
            <option value="">Sélectionner une date</option>
            {getAvailableDates().map(date => (
              <option key={date} value={date}>
                {formatDate(date)}
              </option>
            ))}
          </select>
        </div>

        {/* Time Selection */}
        {selectedDate && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Choisir un horaire
            </label>
            <div className="grid grid-cols-2 gap-2">
              {getAvailableTimesForDate(selectedDate).map(slot => (
                <button
                  key={slot.id}
                  onClick={() => setSelectedTime(slot.time)}
                  className={`p-3 rounded-lg border text-sm transition-colors ${
                    selectedTime === slot.time
                      ? 'border-vida-500 bg-vida-50 text-vida-700'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <div className="font-medium">{slot.time}</div>
                  {slot.capacity && (
                    <div className="text-xs text-gray-500">
                      {slot.capacity - (slot.booked || 0)} places libres
                    </div>
                  )}
                </button>
              ))}
            </div>
            {getAvailableTimesForDate(selectedDate).length === 0 && (
              <p className="text-sm text-gray-500 text-center py-4">
                Aucun créneau disponible pour cette date.
              </p>
            )}
          </div>
        )}

        {/* Notes */}
        <div>
          <Input
            label="Notes (optionnel)"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="Questions ou informations particulières..."
            helperText="Mentionnez toute information utile pour l'organisateur"
          />
        </div>

        {/* Safety Information */}
        {activity.safety_level > 1 && (
          <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-lg">
            <div className="flex items-start gap-2">
              <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600 mt-0.5" />
              <div>
                <h4 className="font-medium text-yellow-800">Information sécurité</h4>
                <p className="text-sm text-yellow-700">
                  Cette activité nécessite un niveau d'attention particulier. 
                  Assurez-vous de respecter toutes les consignes de sécurité.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 p-4 rounded-lg">
            <p className="text-sm text-red-700">{error}</p>
          </div>
        )}

        {/* Actions */}
        <div className="flex gap-3 pt-4">
          <Button
            variant="outline"
            onClick={onCancel}
            disabled={isLoading}
            className="flex-1"
          >
            Annuler
          </Button>
          <Button
            onClick={handleBooking}
            loading={isLoading}
            disabled={!selectedDate || !selectedTime}
            className="flex-1"
          >
            Confirmer la réservation
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}