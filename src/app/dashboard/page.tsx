// src/app/dashboard/page.tsx
import { Card, CardHeader, CardTitle, Button } from '@/components/ui';
import { 
  AcademicCapIcon, 
  CalendarDaysIcon, 
  ChartBarIcon,
  UserIcon 
} from '@heroicons/react/24/outline';

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Tableau de bord</h1>
          <p className="text-gray-600 mt-2">Bienvenue dans votre espace La Vida Luca</p>
        </div>
        <Button variant="primary">
          Nouvelle réservation
        </Button>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card hover>
          <div className="flex items-center">
            <div className="p-2 bg-vida-green/10 rounded-lg">
              <AcademicCapIcon className="w-6 h-6 text-vida-green" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Activités disponibles</p>
              <p className="text-2xl font-bold text-gray-900">30</p>
            </div>
          </div>
        </Card>

        <Card hover>
          <div className="flex items-center">
            <div className="p-2 bg-vida-earth/10 rounded-lg">
              <CalendarDaysIcon className="w-6 h-6 text-vida-earth" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Réservations actives</p>
              <p className="text-2xl font-bold text-gray-900">3</p>
            </div>
          </div>
        </Card>

        <Card hover>
          <div className="flex items-center">
            <div className="p-2 bg-vida-sky/10 rounded-lg">
              <ChartBarIcon className="w-6 h-6 text-vida-sky" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Progression</p>
              <p className="text-2xl font-bold text-gray-900">45%</p>
            </div>
          </div>
        </Card>

        <Card hover>
          <div className="flex items-center">
            <div className="p-2 bg-vida-warm/10 rounded-lg">
              <UserIcon className="w-6 h-6 text-vida-warm" />
            </div>
            <div className="ml-3">
              <p className="text-sm font-medium text-gray-600">Encadrants</p>
              <p className="text-2xl font-bold text-gray-900">12</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Recent Activities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Activités récentes</CardTitle>
          </CardHeader>
          <div className="space-y-4">
            {[
              { title: 'Soins aux animaux', date: '15 Jan 2024', status: 'Complété' },
              { title: 'Plantation de cultures', date: '12 Jan 2024', status: 'En cours' },
              { title: 'Fabrication de fromage', date: '10 Jan 2024', status: 'Programmé' },
            ].map((activity, index) => (
              <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{activity.title}</p>
                  <p className="text-sm text-gray-600">{activity.date}</p>
                </div>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                  activity.status === 'Complété' ? 'bg-green-100 text-green-800' :
                  activity.status === 'En cours' ? 'bg-blue-100 text-blue-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {activity.status}
                </span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Prochaines réservations</CardTitle>
          </CardHeader>
          <div className="space-y-4">
            {[
              { title: 'Initiation maraîchage', date: '20 Jan 2024', time: '14:00', supervisor: 'Marie Dupont' },
              { title: 'Compostage', date: '22 Jan 2024', time: '09:00', supervisor: 'Jean Martin' },
            ].map((booking, index) => (
              <div key={index} className="p-3 border border-gray-200 rounded-lg">
                <div className="flex justify-between items-start">
                  <div>
                    <p className="font-medium text-gray-900">{booking.title}</p>
                    <p className="text-sm text-gray-600">{booking.date} à {booking.time}</p>
                    <p className="text-sm text-gray-500">Avec {booking.supervisor}</p>
                  </div>
                  <Button size="sm" variant="outline">
                    Détails
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
}