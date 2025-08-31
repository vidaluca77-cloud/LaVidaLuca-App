"use client";
import React, { useState, useEffect } from "react";

type Activity = {
  title: string;
  category: "agri"|"transfo"|"artisanat"|"nature"|"social";
  duration: number;
  safety: 1|2;
  desc: string;
};

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
  const [activities, setActivities] = useState<Activity[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  // Fetch activities from backend
  useEffect(() => {
    const fetchActivities = async () => {
      try {
        setLoading(true);
        const params = new URLSearchParams();
        if (selectedCategory !== "all") {
          params.append("category", selectedCategory);
        }
        if (searchTerm) {
          params.append("search", searchTerm);
        }

        const response = await fetch(`${apiUrl}/api/v1/activities?${params}`);
        if (response.ok) {
          const data = await response.json();
          setActivities(data.data.activities);
          setError("");
        } else {
          setError("Erreur lors du chargement des activités");
        }
      } catch (err) {
        console.error("Error fetching activities:", err);
        setError("Impossible de charger les activités");
      } finally {
        setLoading(false);
      }
    };

    fetchActivities();
  }, [selectedCategory, searchTerm, apiUrl]);

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
            Découvrez nos activités pédagogiques pour la formation en MFR
          </p>
          <p className="text-neutral-500 max-w-2xl mx-auto">
            Données en temps réel depuis notre API - Connexion: {apiUrl}
          </p>
        </section>

        {/* Error Message */}
        {error && (
          <section className="mb-8">
            <div className="card max-w-4xl mx-auto bg-gradient-to-r from-red-50 to-red-100 border-red-200">
              <div className="flex items-center space-x-3">
                <div className="text-2xl">⚠️</div>
                <div>
                  <h3 className="font-display font-semibold text-red-800 mb-1">
                    Erreur de connexion
                  </h3>
                  <p className="text-red-700">{error}</p>
                </div>
              </div>
            </div>
          </section>
        )}

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
              {loading ? "Chargement..." : `${activities.length} activité${activities.length > 1 ? 's' : ''} trouvée${activities.length > 1 ? 's' : ''}`}
            </div>
          </div>
        </section>

        {/* Loading State */}
        {loading && (
          <section className="text-center py-12">
            <div className="text-4xl mb-4">⏳</div>
            <h3 className="font-display font-semibold text-xl mb-2 text-neutral-700">
              Chargement des activités...
            </h3>
            <p className="text-neutral-500">
              Récupération des données depuis l'API
            </p>
          </section>
        )}

        {/* Activities Grid */}
        {!loading && (
          <section>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {activities.map((activity, index) => (
                <article key={`${activity.title}-${index}`} className={`card bg-gradient-to-br ${CAT_COLORS[activity.category]} hover:shadow-lg transition-all duration-200`}>
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

            {!loading && activities.length === 0 && (
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
        )}

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