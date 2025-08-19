import React, { useState, useEffect } from 'react';
import { Booking } from '@/types';
import { Card, CardHeader, CardContent, Button, LoadingOverlay } from '@/components/ui';
import { useAuth, useNotification } from '@/context';
import { api } from '@/services/api';
import { 
  CalendarDaysIcon, 
  ClockIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline';

interface BookingListProps {
  className?: string;
}

export const BookingList: React.FC<BookingListProps> = ({ className }) => {
  const { isAuthenticated } = useAuth();
  const { showSuccess, showError } = useNotification();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [updatingBookingId, setUpdatingBookingId] = useState<string | null>(null);

  useEffect(() => {
    if (isAuthenticated) {
      loadBookings();
    }
  }, [isAuthenticated]);

  const loadBookings = async () => {
    setIsLoading(true);
    try {
      const result = await api.getBookings();
      if (result.data) {
        // Sort bookings by date (most recent first)
        const sortedBookings = result.data.sort((a, b) => 
          new Date(b.date).getTime() - new Date(a.date).getTime()
        );
        setBookings(sortedBookings);
      } else {
        showError(result.error || 'Erreur lors du chargement des réservations');
      }
    } catch (error) {
      showError('Erreur lors du chargement des réservations');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId: string) => {
    if (!confirm('Êtes-vous sûr de vouloir annuler cette réservation ?')) {
      return;
    }

    setUpdatingBookingId(bookingId);
    try {
      const result = await api.cancelBooking(bookingId);
      if (result.error) {
        showError(result.error);
      } else {
        showSuccess('Réservation annulée avec succès');
        // Update local state
        setBookings(prev => 
          prev.map(booking => 
            booking.id === bookingId 
              ? { ...booking, status: 'cancelled' as const }
              : booking
          )
        );
      }
    } catch (error) {
      showError('Erreur lors de l\'annulation de la réservation');
    } finally {
      setUpdatingBookingId(null);
    }
  };

  const getStatusColor = (status: Booking['status']) => {
    switch (status) {
      case 'confirmed':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: Booking['status']) => {
    switch (status) {
      case 'confirmed':
        return <CheckCircleIcon className="h-4 w-4" />;
      case 'completed':
        return <CheckCircleIcon className="h-4 w-4" />;
      case 'pending':
        return <ClockIcon className="h-4 w-4" />;
      case 'cancelled':
        return <XCircleIcon className="h-4 w-4" />;
      default:
        return <ExclamationTriangleIcon className="h-4 w-4" />;
    }
  };

  const getStatusLabel = (status: Booking['status']) => {
    switch (status) {
      case 'confirmed':
        return 'Confirmée';
      case 'completed':
        return 'Terminée';
      case 'pending':
        return 'En attente';
      case 'cancelled':
        return 'Annulée';
      default:
        return status;
    }
  };

  const canCancelBooking = (booking: Booking) => {
    return booking.status === 'pending' || booking.status === 'confirmed';
  };

  const isUpcoming = (booking: Booking) => {
    return new Date(booking.date) > new Date() && booking.status === 'confirmed';
  };

  if (!isAuthenticated) {
    return (
      <Card className={className}>
        <CardContent className="text-center py-12">
          <div className="bg-gray-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
            <CalendarDaysIcon className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Mes réservations
          </h3>
          <p className="text-gray-600">
            Connectez-vous pour voir vos réservations
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <LoadingOverlay isLoading={isLoading}>
        <CardHeader>
          <h2 className="text-xl font-semibold text-gray-900">Mes réservations</h2>
          <p className="text-sm text-gray-600">
            Gérez vos activités réservées
          </p>
        </CardHeader>

        <CardContent>
          {bookings.length === 0 ? (
            <div className="text-center py-8">
              <div className="bg-gray-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                <CalendarDaysIcon className="h-8 w-8 text-gray-400" />
              </div>
              <p className="text-gray-600">
                Vous n'avez pas encore de réservations
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {bookings.map((booking) => (
                <div
                  key={booking.id}
                  className={`border rounded-lg p-4 transition-colors ${
                    isUpcoming(booking) ? 'border-primary-200 bg-primary-50' : 'border-gray-200'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <h3 className="font-semibold text-gray-900 mr-3">
                          Activité #{booking.activityId}
                        </h3>
                        <span
                          className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                            booking.status
                          )}`}
                        >
                          {getStatusIcon(booking.status)}
                          <span className="ml-1">{getStatusLabel(booking.status)}</span>
                        </span>
                      </div>

                      <div className="text-sm text-gray-600 space-y-1">
                        <div className="flex items-center">
                          <CalendarDaysIcon className="h-4 w-4 mr-2" />
                          <span>
                            {new Date(booking.date).toLocaleDateString('fr-FR', {
                              weekday: 'long',
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric',
                            })}
                          </span>
                        </div>
                        
                        {booking.notes && (
                          <div className="mt-2">
                            <p className="text-sm text-gray-700">
                              <strong>Notes :</strong> {booking.notes}
                            </p>
                          </div>
                        )}
                      </div>

                      {isUpcoming(booking) && (
                        <div className="mt-2 text-sm text-primary-600 font-medium">
                          Prochaine activité !
                        </div>
                      )}
                    </div>

                    <div className="flex flex-col gap-2 ml-4">
                      {canCancelBooking(booking) && (
                        <Button
                          variant="destructive"
                          size="sm"
                          onClick={() => handleCancelBooking(booking.id)}
                          disabled={updatingBookingId === booking.id}
                          isLoading={updatingBookingId === booking.id}
                        >
                          Annuler
                        </Button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </LoadingOverlay>
    </Card>
  );
};