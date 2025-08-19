import React, { useState } from 'react';
import { Activity, BookingFormData } from '@/types';
import { Card, CardHeader, CardContent, CardFooter, Button, Input, LoadingOverlay } from '@/components/ui';
import { useAuth, useNotification } from '@/context';
import { api } from '@/services/api';
import { bookingSchema } from '@/utils/validation';
import { CalendarDaysIcon, ClockIcon, UserGroupIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface BookingModalProps {
  activity: Activity;
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export const BookingModal: React.FC<BookingModalProps> = ({
  activity,
  isOpen,
  onClose,
  onSuccess,
}) => {
  const { isAuthenticated } = useAuth();
  const { showSuccess, showError } = useNotification();
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState<BookingFormData>({
    activityId: activity.id,
    date: '',
    notes: '',
  });
  const [errors, setErrors] = useState<Partial<BookingFormData>>({});

  if (!isOpen) return null;

  const handleInputChange = (field: keyof BookingFormData, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined,
      }));
    }
  };

  const validateForm = (): boolean => {
    try {
      bookingSchema.parse(formData);
      setErrors({});
      return true;
    } catch (error: any) {
      const fieldErrors: Partial<BookingFormData> = {};
      error.errors?.forEach((err: any) => {
        const field = err.path[0] as keyof BookingFormData;
        fieldErrors[field] = err.message;
      });
      setErrors(fieldErrors);
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isAuthenticated) {
      showError('Veuillez vous connecter pour réserver une activité');
      return;
    }

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);
    try {
      const result = await api.createBooking(
        formData.activityId,
        formData.date,
        formData.notes
      );

      if (result.data) {
        showSuccess('Réservation créée avec succès !');
        if (onSuccess) {
          onSuccess();
        }
        onClose();
      } else {
        showError(result.error || 'Erreur lors de la réservation');
      }
    } catch (error) {
      showError('Erreur lors de la réservation');
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate minimum date (tomorrow)
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  const minDate = tomorrow.toISOString().split('T')[0];

  // Calculate maximum date (3 months from now)
  const maxDate = new Date();
  maxDate.setMonth(maxDate.getMonth() + 3);
  const maxDateString = maxDate.toISOString().split('T')[0];

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-screen items-center justify-center px-4 py-8">
        {/* Backdrop */}
        <div
          className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
          onClick={onClose}
        />
        
        {/* Modal */}
        <div className="relative w-full max-w-lg">
          <Card>
            <LoadingOverlay isLoading={isLoading}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="bg-primary-100 p-3 rounded-full w-12 h-12 mb-4 flex items-center justify-center">
                      <CalendarDaysIcon className="h-6 w-6 text-primary-600" />
                    </div>
                    <h2 className="text-xl font-bold text-gray-900 mb-2">
                      Réserver une activité
                    </h2>
                    <h3 className="text-lg font-semibold text-primary-600 mb-2">
                      {activity.title}
                    </h3>
                  </div>
                  <button
                    onClick={onClose}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>
              </CardHeader>

              <CardContent className="space-y-6">
                {/* Activity Summary */}
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-600 mb-3">{activity.summary}</p>
                  
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center text-gray-500">
                      <ClockIcon className="h-4 w-4 mr-1" />
                      <span>{activity.duration_min} minutes</span>
                    </div>
                    
                    {activity.maxParticipants && (
                      <div className="flex items-center text-gray-500">
                        <UserGroupIcon className="h-4 w-4 mr-1" />
                        <span>
                          {activity.currentParticipants || 0}/{activity.maxParticipants} places
                        </span>
                      </div>
                    )}
                  </div>
                </div>

                {/* Booking Form */}
                <form onSubmit={handleSubmit} className="space-y-4">
                  <Input
                    label="Date souhaitée"
                    type="date"
                    value={formData.date}
                    onChange={(e) => handleInputChange('date', e.target.value)}
                    error={errors.date}
                    min={minDate}
                    max={maxDateString}
                    required
                    helperText="Choisissez une date entre demain et dans 3 mois"
                  />

                  <div>
                    <label className="form-label">Notes (optionnel)</label>
                    <textarea
                      value={formData.notes || ''}
                      onChange={(e) => handleInputChange('notes', e.target.value)}
                      className="form-input min-h-[100px] resize-none"
                      placeholder="Informations complémentaires, questions particulières..."
                    />
                  </div>

                  {/* Seasonality Warning */}
                  {activity.seasonality.length > 0 && 
                   !activity.seasonality.includes('toutes') && (
                    <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                      <p className="text-sm text-yellow-800">
                        <strong>Attention :</strong> Cette activité est disponible 
                        principalement en {activity.seasonality.join(', ')}.
                      </p>
                    </div>
                  )}

                  {/* Materials Info */}
                  {activity.materials.length > 0 && (
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                      <p className="text-sm text-blue-800">
                        <strong>Matériel requis :</strong> {activity.materials.join(', ')}
                      </p>
                    </div>
                  )}
                </form>
              </CardContent>

              <CardFooter>
                <div className="flex gap-3 w-full">
                  <Button
                    variant="outline"
                    onClick={onClose}
                    disabled={isLoading}
                    className="flex-1"
                  >
                    Annuler
                  </Button>
                  <Button
                    onClick={handleSubmit}
                    disabled={isLoading || 
                             (activity.maxParticipants && 
                              (activity.currentParticipants || 0) >= activity.maxParticipants)}
                    isLoading={isLoading}
                    className="flex-1"
                  >
                    {activity.maxParticipants && 
                     (activity.currentParticipants || 0) >= activity.maxParticipants
                      ? 'Complet'
                      : 'Confirmer la réservation'
                    }
                  </Button>
                </div>
              </CardFooter>
            </LoadingOverlay>
          </Card>
        </div>
      </div>
    </div>
  );
};