'use client';

import React, { useState, useMemo } from 'react';
import { useActivities } from '@/hooks/useActivities';
import ActivityCard from '@/components/ActivityCard';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';

const CATEGORIES = [
  { id: 'all', name: 'Toutes les activités' },
  { id: 'agri', name: 'Agriculture' },
  { id: 'transfo', name: 'Transformation' },
  { id: 'artisanat', name: 'Artisanat' },
  { id: 'nature', name: 'Environnement' },
  { id: 'social', name: 'Animation' },
];

export default function ActivitiesPage() {
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [showFilters, setShowFilters] = useState(false);
  
  const { activities, loading, error } = useActivities({
    category: selectedCategory === 'all' ? undefined : selectedCategory,
    search: search || undefined,
  });

  const filteredActivities = useMemo(() => {
    return activities.filter(activity => {
      const matchesSearch = !search || 
        activity.title.toLowerCase().includes(search.toLowerCase()) ||
        activity.summary.toLowerCase().includes(search.toLowerCase()) ||
        activity.skill_tags.some(tag => tag.toLowerCase().includes(search.toLowerCase()));
      
      const matchesCategory = selectedCategory === 'all' || activity.category === selectedCategory;
      
      return matchesSearch && matchesCategory;
    });
  }, [activities, search, selectedCategory]);

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">Erreur lors du chargement des activités: {error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-4">Catalogue d'activités</h1>
        <p className="text-gray-600">
          Découvrez nos 30 activités de formation agricole, artisanale et environnementale.
        </p>
      </div>

      {/* Search and Filters */}
      <div className="space-y-4">
        {/* Search Bar */}
        <div className="relative">
          <MagnifyingGlassIcon className="h-5 w-5 absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Rechercher une activité..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-vida-green focus:border-vida-green"
          />
        </div>

        {/* Category Filter */}
        <div className="flex flex-wrap gap-2">
          {CATEGORIES.map((category) => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                selectedCategory === category.id
                  ? 'bg-vida-green text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {category.name}
            </button>
          ))}
        </div>

        {/* Advanced Filters Toggle */}
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center text-sm text-gray-600 hover:text-gray-800"
        >
          <FunnelIcon className="h-4 w-4 mr-1" />
          Filtres avancés
        </button>

        {/* Advanced Filters */}
        {showFilters && (
          <div className="bg-gray-50 rounded-lg p-4 space-y-4">
            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Durée maximale
                </label>
                <select className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-vida-green">
                  <option value="">Toutes durées</option>
                  <option value="60">1 heure max</option>
                  <option value="90">1h30 max</option>
                  <option value="120">2 heures max</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Niveau de difficulté
                </label>
                <select className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-vida-green">
                  <option value="">Tous niveaux</option>
                  <option value="1">Débutant</option>
                  <option value="2">Intermédiaire</option>
                  <option value="3">Avancé</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Saisonnalité
                </label>
                <select className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-vida-green">
                  <option value="">Toute l'année</option>
                  <option value="printemps">Printemps</option>
                  <option value="ete">Été</option>
                  <option value="automne">Automne</option>
                  <option value="hiver">Hiver</option>
                </select>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Results */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <p className="text-gray-600">
            {loading ? 'Chargement...' : `${filteredActivities.length} activité(s) trouvée(s)`}
          </p>
        </div>

        {loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="bg-gray-200 rounded-lg h-80"></div>
              </div>
            ))}
          </div>
        ) : filteredActivities.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredActivities.map((activity) => (
              <ActivityCard
                key={activity.id}
                activity={activity}
                showStats={true}
                onSelect={(activity) => {
                  window.location.href = `/activites/${activity.id}`;
                }}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <p className="text-gray-600">
              Aucune activité ne correspond à vos critères de recherche.
            </p>
            <button
              onClick={() => {
                setSearch('');
                setSelectedCategory('all');
              }}
              className="mt-4 text-vida-green hover:text-vida-green/80 font-medium"
            >
              Réinitialiser les filtres
            </button>
          </div>
        )}
      </div>
    </div>
  );
}