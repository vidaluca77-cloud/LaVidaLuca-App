"use client";
import { useMemo, useState } from "react";
import { useActivityTracking, useGamification } from "@/components/layout/GamificationProvider";
import { 
  ClockIcon, 
  ShieldCheckIcon, 
  StarIcon,
  PlayIcon,
  CheckCircleIcon 
} from "@heroicons/react/24/outline";

type Item = {
  id: string;
  title: string;
  description: string;
  price: string;
  category: "Produits vivants" | "Activités terrain" | "Services" | "Dons en nature";
  departement: string;
  img?: string;
  tags: string[];
};

type Activity = {
  id: string;
  slug: string;
  title: string;
  category: 'agri' | 'transfo' | 'artisanat' | 'nature' | 'social';
  summary: string;
  duration_min: number;
  skill_tags: string[];
  seasonality: string[];
  safety_level: number;
  materials: string[];
};

const DATA: Item[] = [
  { id:"agn-001", title:"Agneau broutard (vivant)", description:"Réservation locale, qualité élevée.", price:"299 € TTC", category:"Produits vivants", departement:"Calvados (14)", tags:["local","réservation"] },
  { id:"jour-001", title:"Journée découverte ferme", description:"Publics jeunes, familles, structures.", price:"Prix libre", category:"Activités terrain", departement:"Calvados (14)", tags:["groupes"] },
  { id:"plant-001", title:"Plants & arbres (saison)", description:"Variétés locales selon stock.", price:"Selon stock", category:"Produits vivants", departement:"Calvados (14)", tags:["pépinière"] },
  { id:"srv-001", title:"Visite pédagogique MFR/lycées", description:"Accueil encadré, objectifs pédagogiques.", price:"Sur devis", category:"Services", departement:"Calvados (14)", tags:["éducation"] },
  { id:"don-001", title:"Dons en nature", description:"Matériel agricole, plants, clôtures, caméras…", price:"—", category:"Dons en nature", departement:"National", tags:["partenariat"] },
];

// Activités pédagogiques avec gamification
const ACTIVITIES: Activity[] = [
  // Agriculture
  { id: '1', slug: 'nourrir-soigner-moutons', title: 'Nourrir et soigner les moutons', category: 'agri', summary: 'Gestes quotidiens : alimentation, eau, observation.', duration_min: 60, skill_tags: ['elevage', 'responsabilite'], seasonality: ['toutes'], safety_level: 1, materials: ['bottes', 'gants'] },
  { id: '2', slug: 'tonte-entretien-troupeau', title: 'Tonte & entretien du troupeau', category: 'agri', summary: 'Hygiène, tonte (démo), soins courants.', duration_min: 90, skill_tags: ['elevage', 'hygiene'], seasonality: ['printemps'], safety_level: 2, materials: ['bottes', 'gants'] },
  { id: '3', slug: 'basse-cour-soins', title: 'Soins basse-cour', category: 'agri', summary: 'Poules/canards/lapins : alimentation, abris, propreté.', duration_min: 60, skill_tags: ['elevage'], seasonality: ['toutes'], safety_level: 1, materials: ['bottes', 'gants'] },
  { id: '4', slug: 'plantation-cultures', title: 'Plantation de cultures', category: 'agri', summary: 'Semis, arrosage, paillage, suivi de plants.', duration_min: 90, skill_tags: ['jardinage'], seasonality: ['printemps', 'ete'], safety_level: 1, materials: ['gants'] },
  { id: '5', slug: 'init-maraichage', title: 'Initiation maraîchage', category: 'agri', summary: 'Plan de culture, entretien, récolte respectueuse.', duration_min: 120, skill_tags: ['jardinage', 'organisation'], seasonality: ['printemps', 'ete', 'automne'], safety_level: 1, materials: ['gants', 'bottes'] },
  { id: '6', slug: 'clotures-abris', title: 'Gestion des clôtures & abris', category: 'agri', summary: 'Identifier, réparer, sécuriser parcs et abris.', duration_min: 120, skill_tags: ['securite', 'bois'], seasonality: ['toutes'], safety_level: 2, materials: ['gants'] },

  // Transformation
  { id: '7', slug: 'fromage', title: 'Fabrication de fromage', category: 'transfo', summary: 'Du lait au caillé : hygiène, moulage, affinage (découverte).', duration_min: 90, skill_tags: ['hygiene', 'precision'], seasonality: ['toutes'], safety_level: 2, materials: ['tablier'] },
  { id: '8', slug: 'conserves', title: 'Confitures & conserves', category: 'transfo', summary: 'Préparation, stérilisation, mise en pot, étiquetage.', duration_min: 90, skill_tags: ['organisation', 'hygiene'], seasonality: ['ete', 'automne'], safety_level: 1, materials: ['tablier'] },
  { id: '9', slug: 'laine', title: 'Transformation de la laine', category: 'transfo', summary: 'Lavage, cardage, petite création textile.', duration_min: 90, skill_tags: ['precision'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier', 'gants'] },
  { id: '10', slug: 'jus', title: 'Fabrication de jus', category: 'transfo', summary: 'Du verger à la bouteille : tri, pressage, filtration.', duration_min: 90, skill_tags: ['hygiene', 'securite'], seasonality: ['automne'], safety_level: 2, materials: ['tablier', 'gants'] },

  // Artisanat
  { id: '11', slug: 'menuiserie-simple', title: 'Menuiserie simple', category: 'artisanat', summary: 'Nichoirs, mangeoires : mesurer, scier, assembler.', duration_min: 120, skill_tags: ['bois', 'precision'], seasonality: ['toutes'], safety_level: 2, materials: ['gants'] },
  { id: '12', slug: 'vannerie', title: 'Vannerie', category: 'artisanat', summary: 'Tressage d\'osier, création de paniers fonctionnels.', duration_min: 120, skill_tags: ['precision'], seasonality: ['toutes'], safety_level: 1, materials: ['gants'] },
  { id: '13', slug: 'poterie-terre', title: 'Poterie & terre', category: 'artisanat', summary: 'Modelage, ustensiles, récipients simples.', duration_min: 90, skill_tags: ['precision'], seasonality: ['toutes'], safety_level: 1, materials: ['tablier'] },

  // Environnement
  { id: '14', slug: 'nichoirs-hotels', title: 'Nichoirs & hôtels à insectes', category: 'nature', summary: 'Concevoir, fabriquer, installer des abris.', duration_min: 120, skill_tags: ['precision', 'pedagogie'], seasonality: ['toutes'], safety_level: 1, materials: ['gants'] },
  { id: '15', slug: 'compostage', title: 'Compostage', category: 'nature', summary: 'Tri, équilibre, retournement, utilisation.', duration_min: 60, skill_tags: ['organisation'], seasonality: ['toutes'], safety_level: 1, materials: ['gants'] },
  { id: '16', slug: 'haies-biodiversite', title: 'Plantation de haies', category: 'nature', summary: 'Essences locales, technique, espacement, protection.', duration_min: 120, skill_tags: ['jardinage'], seasonality: ['automne', 'hiver'], safety_level: 1, materials: ['gants', 'bottes'] },

  // Social
  { id: '17', slug: 'portes-ouvertes', title: 'Journée portes ouvertes', category: 'social', summary: 'Préparer, accueillir, guider un public.', duration_min: 180, skill_tags: ['accueil', 'organisation'], seasonality: ['toutes'], safety_level: 1, materials: [] },
  { id: '18', slug: 'marche-local', title: 'Participation à un marché local', category: 'social', summary: 'Stand, présentation, caisse symbolique (simulation).', duration_min: 180, skill_tags: ['contact', 'compter_simple', 'equipe'], seasonality: ['toutes'], safety_level: 1, materials: [] },
];

const CATEGORIES = ["Toutes","Produits vivants","Activités terrain","Services","Dons en nature","Activités pédagogiques"] as const;
const ACTIVITY_CATEGORIES = ["Toutes","agriculture","transformation","artisanat","environnement","social"] as const;

export default function Catalogue() {
  const [q, setQ] = useState("");
  const [cat, setCat] = useState<typeof CATEGORIES[number]>("Toutes");
  const [view, setView] = useState<'products' | 'activities'>('activities');
  const [activityCat, setActivityCat] = useState<typeof ACTIVITY_CATEGORIES[number]>("Toutes");
  
  const { userProgress, getUserLevel } = useGamification();
  const { trackActivityStarted, trackActivityCompletion } = useActivityTracking();

  const items = useMemo(() => {
    return DATA.filter(it => {
      const okCat = cat === "Toutes" || it.category === cat;
      const okQ = (it.title + it.description + it.departement + it.tags.join(" "))
        .toLowerCase().includes(q.toLowerCase());
      return okCat && okQ;
    });
  }, [q, cat]);

  const activities = useMemo(() => {
    return ACTIVITIES.filter(activity => {
      const okCat = activityCat === "Toutes" || activity.category === activityCat;
      const okQ = (activity.title + activity.summary + activity.skill_tags.join(" ") + activity.materials.join(" "))
        .toLowerCase().includes(q.toLowerCase());
      return okCat && okQ;
    });
  }, [q, activityCat]);

  const handleActivityStart = async (activity: Activity) => {
    await trackActivityStarted(activity.id, activity.category);
  };

  const handleActivityComplete = async (activity: Activity) => {
    await trackActivityCompletion(
      activity.id,
      activity.category,
      activity.skill_tags,
      activity.duration_min,
      activity.safety_level
    );
  };

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h${mins > 0 ? `${mins}m` : ''}`;
    }
    return `${mins}min`;
  };

  const getSafetyColor = (level: number) => {
    switch (level) {
      case 1: return 'bg-green-100 text-green-800';
      case 2: return 'bg-yellow-100 text-yellow-800';
      case 3: return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSafetyText = (level: number) => {
    switch (level) {
      case 1: return 'Facile';
      case 2: return 'Attention';
      case 3: return 'Expert';
      default: return 'Non défini';
    }
  };

  const getCategoryDisplayName = (category: string) => {
    const names = {
      agri: 'Agriculture',
      transfo: 'Transformation',
      artisanat: 'Artisanat',
      nature: 'Environnement',
      social: 'Animation'
    };
    return names[category as keyof typeof names] || category;
  };

  return (
    <div className="space-y-8">
      <header>
        <h1 className="text-3xl font-bold">Catalogue</h1>
        <p className="opacity-80">Découvrez nos produits et activités pédagogiques.</p>
        
        {userProgress && (
          <div className="mt-4 flex items-center gap-4 text-sm">
            <div className="flex items-center gap-2 bg-green-50 px-3 py-1 rounded-full">
              <StarIcon className="w-4 h-4 text-green-600" />
              <span className="text-green-800">Niveau {getUserLevel()}</span>
            </div>
            <div className="flex items-center gap-2 bg-blue-50 px-3 py-1 rounded-full">
              <CheckCircleIcon className="w-4 h-4 text-blue-600" />
              <span className="text-blue-800">{userProgress.stats.totalActivities} activités terminées</span>
            </div>
          </div>
        )}
      </header>

      {/* View Toggle */}
      <div className="flex gap-2 bg-gray-100 p-1 rounded-lg w-fit">
        <button
          onClick={() => setView('activities')}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            view === 'activities'
              ? 'bg-white text-green-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Activités pédagogiques
        </button>
        <button
          onClick={() => setView('products')}
          className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
            view === 'products'
              ? 'bg-white text-green-600 shadow-sm'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          Produits & Services
        </button>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col gap-3 sm:flex-row">
        <input
          value={q}
          onChange={e=>setQ(e.target.value)}
          placeholder="Rechercher…"
          className="w-full rounded border px-3 py-2"
        />
        <select
          value={view === 'activities' ? activityCat : cat}
          onChange={e => {
            if (view === 'activities') {
              setActivityCat(e.target.value as any);
            } else {
              setCat(e.target.value as any);
            }
          }}
          className="rounded border px-3 py-2"
        >
          {(view === 'activities' ? ACTIVITY_CATEGORIES : CATEGORIES).map(c => (
            <option key={c} value={c}>
              {view === 'activities' && c !== 'Toutes' ? getCategoryDisplayName(c) : c}
            </option>
          ))}
        </select>
      </div>

      {/* Content */}
      {view === 'activities' ? (
        activities.length === 0 ? (
          <div className="rounded border p-6">Aucune activité trouvée.</div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {activities.map(activity => (
              <div key={activity.id} className="rounded-lg border p-5 flex flex-col bg-gradient-to-br from-white to-green-50">
                {/* Activity Header */}
                <div className="flex items-start justify-between mb-3">
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-green-100 text-green-800">
                    {getCategoryDisplayName(activity.category)}
                  </span>
                  <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs ${getSafetyColor(activity.safety_level)}`}>
                    {getSafetyText(activity.safety_level)}
                  </span>
                </div>

                <h3 className="font-semibold text-lg mb-2">{activity.title}</h3>
                <p className="text-sm text-gray-600 mb-4 flex-1">{activity.summary}</p>

                {/* Activity Stats */}
                <div className="space-y-3 mb-4">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <ClockIcon className="w-4 h-4" />
                    <span>{formatDuration(activity.duration_min)}</span>
                  </div>

                  {activity.skill_tags.length > 0 && (
                    <div>
                      <p className="text-xs font-medium text-gray-500 mb-1">Compétences développées :</p>
                      <div className="flex flex-wrap gap-1">
                        {activity.skill_tags.slice(0, 3).map(skill => (
                          <span key={skill} className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-100 text-blue-800">
                            {skill}
                          </span>
                        ))}
                        {activity.skill_tags.length > 3 && (
                          <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-gray-100 text-gray-600">
                            +{activity.skill_tags.length - 3}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {activity.materials.length > 0 && (
                    <div>
                      <p className="text-xs font-medium text-gray-500 mb-1">Matériel requis :</p>
                      <p className="text-xs text-gray-600">{activity.materials.join(', ')}</p>
                    </div>
                  )}
                </div>

                {/* Action Buttons */}
                <div className="space-y-2">
                  <button 
                    onClick={() => handleActivityStart(activity)}
                    className="w-full flex items-center justify-center gap-2 bg-green-500 text-white py-2 rounded-lg font-medium hover:bg-green-600 transition-colors"
                  >
                    <PlayIcon className="w-4 h-4" />
                    Commencer l'activité
                  </button>
                  <button 
                    onClick={() => handleActivityComplete(activity)}
                    className="w-full flex items-center justify-center gap-2 bg-blue-500 text-white py-2 rounded-lg font-medium hover:bg-blue-600 transition-colors"
                  >
                    <CheckCircleIcon className="w-4 h-4" />
                    Marquer comme terminée
                  </button>
                </div>
              </div>
            ))}
          </div>
        )
      ) : (
        items.length === 0 ? (
          <div className="rounded border p-6">Aucun résultat.</div>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {items.map(it=>(
              <div key={it.id} className="rounded-lg border p-5 flex flex-col">
                <div className="h-40 w-full rounded bg-gray-100 mb-4 flex items-center justify-center text-sm opacity-60">
                  Image
                </div>
                <h3 className="font-semibold">{it.title}</h3>
                <p className="mt-1 text-sm opacity-80">{it.description}</p>
                <div className="mt-3 text-sm font-medium">{it.price}</div>
                <div className="mt-2 text-xs opacity-70">{it.departement}</div>
                <div className="mt-3 flex flex-wrap gap-2">
                  {it.tags.map(t=>(
                    <span key={t} className="rounded border px-2 py-1 text-xs">{t}</span>
                  ))}
                </div>
                <a href="/contact" className="mt-4 inline-block rounded bg-emerald-500 px-4 py-2 text-white text-center">
                  Contacter
                </a>
              </div>
            ))}
          </div>
        )
      )}
    </div>
  );
}
