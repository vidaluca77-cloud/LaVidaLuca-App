// src/app/farms/page.tsx
import { Card, CardHeader, CardTitle, Button } from '@/components/ui';
import { 
  MapPinIcon, 
  PhoneIcon, 
  EnvelopeIcon,
  StarIcon 
} from '@heroicons/react/24/outline';

const farms = [
  {
    id: '1',
    name: 'Ferme de la Vallée Verte',
    description: 'Ferme pédagogique spécialisée dans l\'agriculture biologique et l\'élevage de poules pondeuses.',
    location: 'Normandie, Calvados (14)',
    specialties: ['Agriculture bio', 'Élevage', 'Maraîchage'],
    capacity: 15,
    supervisor: 'Marie Dupont',
    rating: 4.8,
    contact: {
      email: 'marie@ferme-vallee-verte.fr',
      phone: '02 31 45 67 89'
    },
    image: '/api/placeholder/400/200'
  },
  {
    id: '2',
    name: 'Domaine des Chênes',
    description: 'Exploitation agricole diversifiée proposant des formations en agroécologie et transformation alimentaire.',
    location: 'Bretagne, Ille-et-Vilaine (35)',
    specialties: ['Agroécologie', 'Transformation', 'Apiculture'],
    capacity: 20,
    supervisor: 'Jean Martin',
    rating: 4.6,
    contact: {
      email: 'contact@domaine-chenes.fr',
      phone: '02 99 12 34 56'
    },
    image: '/api/placeholder/400/200'
  },
  {
    id: '3',
    name: 'Ferme du Soleil Levant',
    description: 'Centre de formation axé sur la permaculture et les techniques ancestrales de culture.',
    location: 'Provence, Vaucluse (84)',
    specialties: ['Permaculture', 'Plantes médicinales', 'Artisanat'],
    capacity: 12,
    supervisor: 'Sophie Durand',
    rating: 4.9,
    contact: {
      email: 'sophie@soleil-levant.fr',
      phone: '04 90 78 45 12'
    },
    image: '/api/placeholder/400/200'
  }
];

export default function FarmsPage() {
  return (
    <div className="space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900">Nos lieux d'action</h1>
        <p className="text-gray-600 mt-4 max-w-2xl mx-auto">
          Découvrez les fermes partenaires qui accueillent nos formations. 
          Chaque lieu offre un environnement unique pour apprendre et grandir.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
        {farms.map((farm) => (
          <Card key={farm.id} hover className="overflow-hidden">
            <div className="aspect-video bg-gray-200 mb-4 rounded-lg flex items-center justify-center">
              <span className="text-gray-500">Photo de la ferme</span>
            </div>
            
            <div className="space-y-4">
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-xl font-bold text-gray-900">{farm.name}</h3>
                  <div className="flex items-center">
                    <StarIcon className="w-4 h-4 text-yellow-500 fill-current" />
                    <span className="text-sm text-gray-600 ml-1">{farm.rating}</span>
                  </div>
                </div>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {farm.description}
                </p>
              </div>

              <div className="flex items-center text-sm text-gray-500">
                <MapPinIcon className="w-4 h-4 mr-1" />
                {farm.location}
              </div>

              <div className="space-y-2">
                <div className="flex flex-wrap gap-2">
                  {farm.specialties.map((specialty, index) => (
                    <span 
                      key={index}
                      className="bg-vida-green/10 text-vida-green px-2 py-1 rounded-full text-xs font-medium"
                    >
                      {specialty}
                    </span>
                  ))}
                </div>
                
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Capacité:</span> {farm.capacity} participants
                </div>
                
                <div className="text-sm text-gray-600">
                  <span className="font-medium">Encadrant:</span> {farm.supervisor}
                </div>
              </div>

              <div className="border-t pt-4 space-y-2">
                <div className="flex items-center text-sm text-gray-600">
                  <EnvelopeIcon className="w-4 h-4 mr-2" />
                  {farm.contact.email}
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <PhoneIcon className="w-4 h-4 mr-2" />
                  {farm.contact.phone}
                </div>
              </div>

              <div className="flex gap-2 pt-4">
                <Button size="sm" className="flex-1">
                  Voir les activités
                </Button>
                <Button size="sm" variant="outline" className="flex-1">
                  Contacter
                </Button>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="text-center">
        <Card className="inline-block">
          <div className="text-center p-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4">
              Vous souhaitez devenir partenaire ?
            </h3>
            <p className="text-gray-600 mb-6">
              Rejoignez notre réseau de fermes pédagogiques et contribuez à la formation des jeunes.
            </p>
            <Button>
              Devenir ferme partenaire
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
}