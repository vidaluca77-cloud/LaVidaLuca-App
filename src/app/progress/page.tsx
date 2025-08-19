// src/app/progress/page.tsx
'use client';

import { Card, CardHeader, CardTitle, Button } from '@/components/ui';
import { 
  CheckCircleIcon, 
  ClockIcon,
  StarIcon,
  TrophyIcon,
  AcademicCapIcon 
} from '@heroicons/react/24/outline';

const progressData = {
  overall: {
    completed: 8,
    total: 30,
    percentage: 27
  },
  categories: [
    { name: 'Agriculture', completed: 3, total: 12, percentage: 25, color: 'vida-green' },
    { name: 'Transformation', completed: 2, total: 5, percentage: 40, color: 'vida-earth' },
    { name: 'Artisanat', completed: 1, total: 4, percentage: 25, color: 'vida-warm' },
    { name: 'Environnement', completed: 2, total: 6, percentage: 33, color: 'vida-sky' },
    { name: 'Animation', completed: 0, total: 3, percentage: 0, color: 'gray-400' }
  ],
  recentActivities: [
    {
      id: '1',
      title: 'Soins aux animaux',
      category: 'Agriculture',
      completedAt: '2024-01-15',
      rating: 4.5,
      feedback: 'Excellente maîtrise des gestes de base',
      supervisor: 'Marie Dupont'
    },
    {
      id: '2',
      title: 'Fabrication de fromage',
      category: 'Transformation',
      completedAt: '2024-01-12',
      rating: 4.0,
      feedback: 'Très bon travail, attention à l\'hygiène',
      supervisor: 'Jean Martin'
    },
    {
      id: '3',
      title: 'Compostage',
      category: 'Environnement',
      completedAt: '2024-01-10',
      rating: 5.0,
      feedback: 'Parfait ! Très bonne compréhension du processus',
      supervisor: 'Sophie Durand'
    }
  ],
  upcomingMilestones: [
    { title: 'Première certification Agriculture', progress: 75, needed: 4, completed: 3 },
    { title: 'Badge Transformation', progress: 40, needed: 5, completed: 2 },
    { title: 'Spécialisation Environnement', progress: 33, needed: 6, completed: 2 }
  ]
};

export default function ProgressPage() {
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Mon parcours</h1>
        <p className="text-gray-600 mt-2">Suivez votre progression et vos accomplissements</p>
      </div>

      {/* Overall Progress */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <TrophyIcon className="w-6 h-6 mr-3 text-vida-warm" />
            Progression générale
          </CardTitle>
        </CardHeader>
        
        <div className="flex items-center space-x-8">
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Activités complétées</span>
              <span className="text-sm text-gray-600">
                {progressData.overall.completed}/{progressData.overall.total}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div 
                className="bg-vida-green h-3 rounded-full transition-all duration-300"
                style={{ width: `${progressData.overall.percentage}%` }}
              ></div>
            </div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-vida-green">{progressData.overall.percentage}%</div>
            <div className="text-sm text-gray-600">Complété</div>
          </div>
        </div>
      </Card>

      {/* Category Progress */}
      <Card>
        <CardHeader>
          <CardTitle>Progression par catégorie</CardTitle>
        </CardHeader>
        
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {progressData.categories.map((category, index) => (
            <div key={index} className="p-4 border border-gray-200 rounded-lg">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-medium text-gray-900">{category.name}</h3>
                <span className="text-sm text-gray-600">
                  {category.completed}/{category.total}
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                <div 
                  className={`bg-${category.color} h-2 rounded-full transition-all duration-300`}
                  style={{ width: `${category.percentage}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500">{category.percentage}% complété</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Recent Activities */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <CheckCircleIcon className="w-6 h-6 mr-3 text-green-500" />
              Activités récentes
            </CardTitle>
          </CardHeader>
          
          <div className="space-y-4">
            {progressData.recentActivities.map((activity) => (
              <div key={activity.id} className="p-4 bg-gray-50 rounded-lg">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <h4 className="font-medium text-gray-900">{activity.title}</h4>
                    <p className="text-sm text-gray-600">{activity.category}</p>
                  </div>
                  <div className="flex items-center">
                    <StarIcon className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="text-sm text-gray-600 ml-1">{activity.rating}</span>
                  </div>
                </div>
                <p className="text-sm text-gray-700 mb-2">{activity.feedback}</p>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>Avec {activity.supervisor}</span>
                  <span>{activity.completedAt}</span>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Upcoming Milestones */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <AcademicCapIcon className="w-6 h-6 mr-3 text-vida-green" />
              Prochains objectifs
            </CardTitle>
          </CardHeader>
          
          <div className="space-y-4">
            {progressData.upcomingMilestones.map((milestone, index) => (
              <div key={index} className="p-4 border border-gray-200 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-gray-900">{milestone.title}</h4>
                  <span className="text-sm text-gray-600">
                    {milestone.completed}/{milestone.needed}
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2 mb-2">
                  <div 
                    className="bg-vida-green h-2 rounded-full transition-all duration-300"
                    style={{ width: `${milestone.progress}%` }}
                  ></div>
                </div>
                <p className="text-xs text-gray-500">
                  {milestone.needed - milestone.completed} activités restantes
                </p>
              </div>
            ))}
          </div>
        </Card>
      </div>

      {/* Achievement Suggestions */}
      <Card>
        <CardHeader>
          <CardTitle>Suggestions d'activités</CardTitle>
        </CardHeader>
        
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <div className="p-4 border border-dashed border-gray-300 rounded-lg text-center">
            <ClockIcon className="w-8 h-8 text-gray-400 mx-auto mb-3" />
            <h4 className="font-medium text-gray-900 mb-2">Initiation maraîchage</h4>
            <p className="text-sm text-gray-600 mb-3">Recommandé pour votre progression en Agriculture</p>
            <Button size="sm" variant="outline">
              Réserver
            </Button>
          </div>
          
          <div className="p-4 border border-dashed border-gray-300 rounded-lg text-center">
            <ClockIcon className="w-8 h-8 text-gray-400 mx-auto mb-3" />
            <h4 className="font-medium text-gray-900 mb-2">Apiculture découverte</h4>
            <p className="text-sm text-gray-600 mb-3">Parfait pour débuter en Environnement</p>
            <Button size="sm" variant="outline">
              Réserver
            </Button>
          </div>
          
          <div className="p-4 border border-dashed border-gray-300 rounded-lg text-center">
            <ClockIcon className="w-8 h-8 text-gray-400 mx-auto mb-3" />
            <h4 className="font-medium text-gray-900 mb-2">Travail du bois</h4>
            <p className="text-sm text-gray-600 mb-3">Nouveau dans la catégorie Artisanat</p>
            <Button size="sm" variant="outline">
              Réserver
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}