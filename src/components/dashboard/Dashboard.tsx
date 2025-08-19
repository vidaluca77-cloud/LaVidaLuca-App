import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardContent, LoadingOverlay } from '@/components/ui';
import { ActivityCard } from '@/components/ActivityCard';
import { useAuth, useNotification } from '@/context';
import { Activity, Booking } from '@/types';
import { api } from '@/services/api';
import {
  CalendarDaysIcon,
  ChartBarIcon,
  ClockIcon,
  TrophyIcon,
  BookOpenIcon,
} from '@heroicons/react/24/outline';

interface DashboardProps {
  className?: string;
}

interface DashboardStats {
  totalBookings: number;
  completedActivities: number;
  upcomingBookings: number;
  totalHours: number;
}

export const Dashboard: React.FC<DashboardProps> = ({ className }) => {
  const { user, isAuthenticated } = useAuth();
  const { showError } = useNotification();
  const [isLoading, setIsLoading] = useState(true);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [suggestions, setSuggestions] = useState<Activity[]>([]);
  const [stats, setStats] = useState<DashboardStats>({
    totalBookings: 0,
    completedActivities: 0,
    upcomingBookings: 0,
    totalHours: 0,
  });

  useEffect(() => {
    if (isAuthenticated) {
      loadDashboardData();
    }
  }, [isAuthenticated]);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      // Load bookings and suggestions in parallel
      const [bookingsResult, suggestionsResult] = await Promise.all([
        api.getBookings(),
        api.getSuggestions(),
      ]);

      if (bookingsResult.data) {
        setBookings(bookingsResult.data);
        calculateStats(bookingsResult.data);
      }

      if (suggestionsResult.data) {
        setSuggestions(suggestionsResult.data.slice(0, 3)); // Show top 3 suggestions
      }
    } catch (error) {
      showError('Erreur lors du chargement du tableau de bord');
    } finally {
      setIsLoading(false);
    }
  };

  const calculateStats = (bookings: Booking[]) => {
    const completed = bookings.filter(b => b.status === 'completed');
    const upcoming = bookings.filter(b => 
      b.status === 'confirmed' && new Date(b.date) > new Date()
    );
    
    // Calculate total hours from completed activities
    // Note: This would need activity duration data in real implementation
    const totalHours = completed.length * 1.5; // Assuming 1.5 hours average per activity

    setStats({
      totalBookings: bookings.length,
      completedActivities: completed.length,
      upcomingBookings: upcoming.length,
      totalHours,
    });
  };

  const handleActivityBooking = (activity: Activity) => {
    // This would open a booking modal or navigate to booking page
    console.log('Book activity:', activity);
  };

  const handleActivityDetails = (activity: Activity) => {
    // This would navigate to activity details page
    console.log('View activity details:', activity);
  };

  if (!isAuthenticated) {
    return (
      <Card className={className}>
        <CardContent className="text-center py-12">
          <div className="bg-gray-100 p-4 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
            <BookOpenIcon className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Tableau de bord personnel
          </h3>
          <p className="text-gray-600">
            Connectez-vous pour voir vos activités et votre progression
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className={className}>
      <LoadingOverlay isLoading={isLoading}>
        {/* Welcome Section */}
        <Card className="mb-6">
          <CardContent className="py-6">
            <div className="flex items-center">
              <div className="bg-primary-100 p-3 rounded-full">
                <TrophyIcon className="h-8 w-8 text-primary-600" />
              </div>
              <div className="ml-4">
                <h1 className="text-2xl font-bold text-gray-900">
                  Bienvenue, {user?.name} !
                </h1>
                <p className="text-gray-600">
                  Voici un aperçu de votre parcours à La Vida Luca
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <div className="bg-vida-green-100 p-2 rounded-lg">
                  <CalendarDaysIcon className="h-5 w-5 text-vida-green-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Réservations</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalBookings}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <div className="bg-vida-earth-100 p-2 rounded-lg">
                  <TrophyIcon className="h-5 w-5 text-vida-earth-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Complétées</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.completedActivities}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <div className="bg-vida-sky-100 p-2 rounded-lg">
                  <ClockIcon className="h-5 w-5 text-vida-sky-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">À venir</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.upcomingBookings}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-4">
              <div className="flex items-center">
                <div className="bg-vida-warm-100 p-2 rounded-lg">
                  <ChartBarIcon className="h-5 w-5 text-vida-warm-600" />
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-gray-500">Heures</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalHours.toFixed(1)}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Bookings */}
        {bookings.length > 0 && (
          <Card className="mb-6">
            <CardHeader>
              <h2 className="text-lg font-semibold text-gray-900">Mes réservations récentes</h2>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {bookings.slice(0, 3).map((booking) => (
                  <div
                    key={booking.id}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div>
                      <p className="font-medium text-gray-900">
                        Activité #{booking.activityId}
                      </p>
                      <p className="text-sm text-gray-500">
                        {new Date(booking.date).toLocaleDateString('fr-FR')}
                      </p>
                    </div>
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-medium ${
                        booking.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : booking.status === 'confirmed'
                          ? 'bg-blue-100 text-blue-800'
                          : booking.status === 'pending'
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-red-100 text-red-800'
                      }`}
                    >
                      {booking.status === 'completed' && 'Terminée'}
                      {booking.status === 'confirmed' && 'Confirmée'}
                      {booking.status === 'pending' && 'En attente'}
                      {booking.status === 'cancelled' && 'Annulée'}
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Suggested Activities */}
        {suggestions.length > 0 && (
          <Card>
            <CardHeader>
              <h2 className="text-lg font-semibold text-gray-900">Activités recommandées pour vous</h2>
              <p className="text-sm text-gray-600">
                Basées sur vos préférences et votre profil
              </p>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {suggestions.map((activity) => (
                  <ActivityCard
                    key={activity.id}
                    activity={activity}
                    onBooking={handleActivityBooking}
                    onLearnMore={handleActivityDetails}
                    showBookingButton={true}
                  />
                ))}
              </div>
            </CardContent>
          </Card>
        )}
      </LoadingOverlay>
    </div>
  );
};