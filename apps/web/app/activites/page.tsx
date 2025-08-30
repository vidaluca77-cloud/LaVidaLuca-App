"use client";
import React, { useState } from "react";

type Activity = {
  title: string;
  category: "agri"|"transfo"|"artisanat"|"nature"|"social";
  duration: number;
  safety: 1|2;
  desc: string;
};

const activities: Activity[] = [
  { title:"Nourrir et soigner les moutons", category:"agri", duration:60, safety:1, desc:"Alimentation, eau, observation et bien-être du troupeau." },
  { title:"Tonte & entretien du troupeau", category:"agri", duration:90, safety:2, desc:"Hygiène, tonte (démonstration) et soins courants." },
  { title:"Soins basse-cour", category:"agri", duration:60, safety:1, desc:"Poules, canards, lapins : alimentation, abris, propreté." },
  { title:"Plantation de cultures", category:"agri", duration:90, safety:1, desc:"Semis, arrosage, paillage, suivi des jeunes plants." },
  { title:"Initiation maraîchage", category:"agri", duration:120, safety:1, desc:"Plan de culture, entretien, récolte respectueuse." },
  { title:"Gestion des clôtures & abris", category:"agri", duration:120, safety:2, desc:"Identifier, réparer et sécuriser parcs et abris." },

  { title:"Fabrication de fromage", category:"transfo", duration:90, safety:2, desc:"Du lait au caillé : hygiène, moulage, affinage (découverte)." },
  { title:"Confitures & conserves", category:"transfo", duration:90, safety:1, desc:"Préparation, stérilisation, mise en pot, étiquetage." },
  { title:"Transformation de la laine", category:"transfo", duration:90, safety:1, desc:"Lavage, cardage et petite création textile." },
  { title:"Fabrication de jus", category:"transfo", duration:90, safety:2, desc:"Du verger à la bouteille : tri, pressage, filtration." },
  { title:"Séchage d'herbes aromatiques", category:"transfo", duration:60, safety:1, desc:"Cueillette, séchage doux et conditionnement." },
  { title:"Pain au four à bois", category:"transfo", duration:120, safety:2, desc:"Pétrissage, façonnage, cuisson : respect des temps." },

  { title:"Construction d'abris", category:"artisanat", duration:120, safety:2, desc:"Petites structures bois : plan, coupe, assemblage." },
  { title:"Réparation & entretien des outils", category:"artisanat", duration:60, safety:1, desc:"Affûtage, graissage, vérifications simples." },
  { title:"Menuiserie simple", category:"artisanat", duration:120, safety:2, desc:"Mesure, coupe, ponçage, finitions." },
  { title:"Peinture & décoration d'espaces", category:"artisanat", duration:90, safety:1, desc:"Préparer, protéger, peindre proprement." },
  { title:"Aménagement d'espaces verts", category:"artisanat", duration:90, safety:1, desc:"Désherbage doux, paillage, plantations." },
  { title:"Panneaux & orientation", category:"artisanat", duration:90, safety:1, desc:"Concevoir et poser une signalétique claire." },

  { title:"Entretien de la rivière", category:"nature", duration:90, safety:2, desc:"Nettoyage doux, observation des berges." },
  { title:"Plantation d'arbres", category:"nature", duration:120, safety:1, desc:"Choix d'essences, tuteurage, paillage, suivi." },
  { title:"Potager écologique", category:"nature", duration:90, safety:1, desc:"Associations, paillis, rotation des cultures." },
  { title:"Compostage", category:"nature", duration:60, safety:1, desc:"Tri, compost et valorisation des déchets verts." },
  { title:"Observation de la faune locale", category:"nature", duration:60, safety:1, desc:"Discrétion, repérage, traces/indices." },
  { title:"Nichoirs & hôtels à insectes", category:"nature", duration:120, safety:1, desc:"Concevoir, fabriquer, installer des abris." },

  { title:"Journée portes ouvertes", category:"social", duration:180, safety:1, desc:"Préparer, accueillir, guider un public." },
  { title:"Visites guidées de la ferme", category:"social", duration:60, safety:1, desc:"Présenter la ferme et répondre simplement." },
  { title:"Ateliers pour enfants", category:"social", duration:90, safety:2, desc:"Jeux, découvertes nature, mini-gestes encadrés." },
  { title:"Cuisine collective (équipe)", category:"social", duration:90, safety:1, desc:"Préparer un repas simple et bon." },
  { title:"Goûter fermier", category:"social", duration:60, safety:1, desc:"Organisation, service, convivialité, propreté." },
  { title:"Participation à un marché local", category:"social", duration:180, safety:1, desc:"Stand, présentation, caisse symbolique (simulation)." }
];

const CAT_LABEL: Record<Activity["category"], string> = {
  agri: "Agriculture",
  transfo: "Transformation",
  artisanat: "Artisanat",
  nature: "Environnement",
  social: "Animation"
};

const CAT_ICONS: Record<Activity["category"], string> = {
  agri: "🌱",
  transfo: "🏭",
  artisanat: "🔨",
  nature: "🌿",
  social: "👥"
};

const CAT_COLORS: Record<Activity["category"], string> = {
  agri: "from-green-100 to-green-200 border-green-200",
  transfo: "from-earth-100 to-earth-200 border-earth-200",
  artisanat: "from-neutral-100 to-neutral-200 border-neutral-200",
  nature: "from-green-50 to-earth-50 border-green-100",
  social: "from-primary-100 to-primary-200 border-primary-200"
};

export default function ActivitesPage(){
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchTerm, setSearchTerm] = useState("");

  const filteredActivities = activities.filter(activity => {
    const matchesCategory = selectedCategory === "all" || activity.category === selectedCategory;
    const matchesSearch = activity.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         activity.desc.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  const categories = ["all", ...Object.keys(CAT_LABEL)] as const;

  return (
    <div className="min-h-screen gradient-bg">
      {/* Navigation */}
      <nav className="container py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-earth-500 rounded-lg"></div>
            <a href="/" className="text-xl font-display font-semibold text-gradient">La Vida Luca</a>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <span className="text-primary-600 font-medium border-b-2 border-primary-600">
              Activités
            </span>
            <a href="/proposer-aide" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Contribuer
            </a>
            <a href="/test-ia" className="btn btn-primary">
              Assistant IA
            </a>
          </div>
        </div>
      </nav>

      <main className="container pb-20">
        {/* Header */}
        <section className="text-center mb-12">
          <h1 className="text-gradient mb-4">
            Catalogue des Activités
          </h1>
          <p className="text-xl text-neutral-600 mb-2 max-w-3xl mx-auto">
            Découvrez nos 30 activités pédagogiques pour la formation en MFR
          </p>
          <p className="text-neutral-500 max-w-2xl mx-auto">
            Consultation uniquement — aucun bouton d'inscription en ligne.
          </p>
        </section>

        {/* Filters */}
        <section className="mb-8">
          <div className="card max-w-4xl mx-auto">
            <div className="mb-6">
              <h3 className="font-display font-semibold text-lg mb-4 text-neutral-800">
                Rechercher et filtrer
              </h3>
              
              {/* Search */}
              <div className="mb-6">
                <input
                  type="text"
                  placeholder="Rechercher une activité..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full px-4 py-3 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                />
              </div>

              {/* Category Filters */}
              <div className="flex flex-wrap gap-2">
                {categories.map(cat => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`px-4 py-2 rounded-lg font-medium transition-all ${
                      selectedCategory === cat
                        ? 'bg-primary-600 text-white shadow-md'
                        : 'bg-neutral-100 text-neutral-600 hover:bg-neutral-200'
                    }`}
                  >
                    {cat === "all" ? "🔍 Toutes" : `${CAT_ICONS[cat as Activity["category"]]} ${CAT_LABEL[cat as Activity["category"]]}`}
                  </button>
                ))}
              </div>
            </div>

            <div className="text-sm text-neutral-500">
              {filteredActivities.length} activité{filteredActivities.length > 1 ? 's' : ''} trouvée{filteredActivities.length > 1 ? 's' : ''}
            </div>
          </div>
        </section>

        {/* Activities Grid */}
        <section>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredActivities.map((activity) => (
              <article key={activity.title} className={`card bg-gradient-to-br ${CAT_COLORS[activity.category]} hover:shadow-lg transition-all duration-200`}>
                <div className="flex items-start justify-between mb-4">
                  <div className="text-2xl">{CAT_ICONS[activity.category]}</div>
                  <div className="flex gap-2">
                    <span className="text-xs px-2 py-1 bg-white/70 rounded-full text-neutral-600">
                      {activity.duration} min
                    </span>
                    <span className={`text-xs px-2 py-1 rounded-full text-white ${
                      activity.safety === 1 ? 'bg-green-500' : 'bg-earth-500'
                    }`}>
                      Niveau {activity.safety}
                    </span>
                  </div>
                </div>

                <h3 className="font-display font-semibold text-lg mb-3 text-neutral-800 leading-tight">
                  {activity.title}
                </h3>
                
                <p className="text-neutral-600 text-sm leading-relaxed mb-4">
                  {activity.desc}
                </p>

                <div className="flex items-center justify-between text-xs">
                  <span className="px-3 py-1 bg-white/50 rounded-full text-neutral-600 font-medium">
                    {CAT_LABEL[activity.category]}
                  </span>
                  <span className="text-neutral-500">
                    {activity.safety === 1 ? "🟢 Sécurité standard" : "🟡 Sécurité renforcée"}
                  </span>
                </div>
              </article>
            ))}
          </div>

          {filteredActivities.length === 0 && (
            <div className="text-center py-12">
              <div className="text-4xl mb-4">🔍</div>
              <h3 className="font-display font-semibold text-xl mb-2 text-neutral-700">
                Aucune activité trouvée
              </h3>
              <p className="text-neutral-500">
                Essayez de modifier vos critères de recherche ou de filtrage.
              </p>
            </div>
          )}
        </section>

        {/* Back to Home */}
        <section className="text-center mt-16">
          <a href="/" className="btn btn-secondary">
            ← Retour à l'accueil
          </a>
        </section>
      </main>
    </div>
  );
}