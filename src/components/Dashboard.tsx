'use client';

import React, { useState, useEffect } from 'react';
import { CalendarIcon, ClockIcon, CheckCircleIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle, Badge, Button } from '@/components/ui';
import { ActivityCard } from '@/components/ActivityCard';
import { Activity, Booking, UserProfile } from '@/types';
import { apiClient } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';

interface DashboardProps {
  userProfile?: UserProfile;
}

interface DashboardStats {
  totalBookings: number;
  completedActivities: number;
  upcomingBookings: number;
  suggestedActivities: number;
}

export function Dashboard({ userProfile }: DashboardProps) {
  const { user } = useAuth();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [suggestedActivities, setSuggestedActivities] = useState<Activity[]>([]);
  const [stats, setStats] = useState<DashboardStats>({
    totalBookings: 0,
    completedActivities: 0,
    upcomingBookings: 0,
    suggestedActivities: 0
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadDashboardData = async () => {
      if (!user) return;

      try {
        setIsLoading(true);
        
        // Load user bookings
        const bookingsResponse = await apiClient.getUserBookings();
        if (bookingsResponse.success) {
          setBookings(bookingsResponse.data);
          
          // Calculate stats
          const completed = bookingsResponse.data.filter(b => b.status === 'completed').length;
          const upcoming = bookingsResponse.data.filter(b => 
            b.status === 'confirmed' && new Date(b.scheduled_date) > new Date()
          ).length;
          
          setStats(prev => ({
            ...prev,
            totalBookings: bookingsResponse.data.length,
            completedActivities: completed,
            upcomingBookings: upcoming
          }));
        }

        // Load suggested activities if profile is available
        if (userProfile) {
          const suggestionsResponse = await apiClient.getActivitySuggestions(userProfile);
          if (suggestionsResponse.success) {
            setSuggestedActivities(suggestionsResponse.data.slice(0, 6)); // Limit to 6 suggestions
            setStats(prev => ({
              ...prev,
              suggestedActivities: suggestionsResponse.data.length
            }));
          }
        }
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();
  }, [user, userProfile]);

  const getBookingStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed': return 'success';
      case 'completed': return 'default';
      case 'pending': return 'warning';
      case 'cancelled': return 'destructive';
      default: return 'outline';
    }
  };

  const getBookingStatusText = (status: string) => {
    switch (status) {
      case 'confirmed': return 'Confirmé';
      case 'completed': return 'Terminé';
      case 'pending': return 'En attente';
      case 'cancelled': return 'Annulé';
      default: return status;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <Card key={i} className="animate-pulse">
              <CardContent className="p-6">
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/3"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Bonjour {user?.name || 'et bienvenue'} !
        </h1>
        <p className="text-gray-600">Voici un aperçu de votre activité sur La Vida Luca.</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <CalendarIcon className="h-8 w-8 text-vida-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total réservations</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalBookings}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <CheckCircleIcon className="h-8 w-8 text-green-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Activités terminées</p>
                <p className="text-2xl font-bold text-gray-900">{stats.completedActivities}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <ClockIcon className="h-8 w-8 text-vida-warm-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Prochaines activités</p>
                <p className="text-2xl font-bold text-gray-900">{stats.upcomingBookings}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center">
              <ExclamationTriangleIcon className="h-8 w-8 text-vida-sky-500" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Suggestions</p>
                <p className="text-2xl font-bold text-gray-900">{stats.suggestedActivities}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Bookings */}
        <Card>
          <CardHeader>
            <CardTitle>Mes réservations récentes</CardTitle>
          </CardHeader>
          <CardContent>
            {bookings.length === 0 ? (
              <p className="text-gray-500 text-center py-4">
                Aucune réservation pour le moment.
              </p>
            ) : (
              <div className="space-y-3">
                {bookings.slice(0, 5).map((booking) => (
                  <div key={booking.id} className="flex items-center justify-between p-3 border rounded-lg">
                    <div className="flex-1">
                      <p className="font-medium text-sm">Activité #{booking.activity_id}</p>
                      <p className="text-xs text-gray-500">
                        {formatDate(booking.scheduled_date)}
                      </p>
                      {booking.notes && (
                        <p className="text-xs text-gray-600 mt-1">{booking.notes}</p>
                      )}
                    </div>
                    <Badge variant={getBookingStatusColor(booking.status) as any} size="sm">
                      {getBookingStatusText(booking.status)}
                    </Badge>
                  </div>
                ))}
                {bookings.length > 5 && (
                  <Button variant="outline" size="sm" className="w-full">
                    Voir toutes les réservations
                  </Button>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Suggested Activities */}
        <Card>
          <CardHeader>
            <CardTitle>Activités suggérées pour vous</CardTitle>
          </CardHeader>
          <CardContent>
            {suggestedActivities.length === 0 ? (
              <div className="text-center py-4">
                <p className="text-gray-500 mb-3">
                  Complétez votre profil pour recevoir des suggestions personnalisées.
                </p>
                <Button variant="outline" size="sm">
                  Compléter mon profil
                </Button>
              </div>
            ) : (
              <div className="space-y-3">
                {suggestedActivities.slice(0, 3).map((activity) => (
                  <div key={activity.id} className="border rounded-lg p-3">
                    <h4 className="font-medium text-sm mb-1">{activity.title}</h4>
                    <p className="text-xs text-gray-600 mb-2">{activity.summary}</p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <Badge variant="outline" size="sm">
                          {activity.category}
                        </Badge>
                        <span className="text-xs text-gray-500">
                          {Math.floor(activity.duration_min / 60)}h{activity.duration_min % 60 > 0 ? activity.duration_min % 60 + 'min' : ''}
                        </span>
                      </div>
                      <Button variant="outline" size="sm">
                        Voir
                      </Button>
                    </div>
                  </div>
                ))}
                <Button variant="outline" size="sm" className="w-full">
                  Voir toutes les suggestions
                </Button>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}