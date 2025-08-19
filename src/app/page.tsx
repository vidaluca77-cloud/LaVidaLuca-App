'use client'

import React, { useState, useEffect } from 'react';
import { HeartIcon, AcademicCapIcon, GlobeAltIcon, SparklesIcon } from '@heroicons/react/24/outline';
import { useAuth } from '@/contexts/AuthContext';
import { useRecommendations } from '@/hooks/useRecommendations';
import { useActivities } from '@/hooks/useActivities';
import RecommendationCard from '@/components/RecommendationCard';
import ActivityCard from '@/components/ActivityCard';

export default function Home() {
  const { user } = useAuth();
  const { recommendations, loading: recLoading } = useRecommendations(5);
  const { activities, loading: activitiesLoading } = useActivities({ limit: 6 });

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center py-16">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            <span className="text-vida-green">La Vida Luca</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            Plateforme collaborative basée sur IA pour la formation des jeunes en MFR, 
            le développement d'une agriculture nouvelle et l'insertion sociale.
          </p>
          
          <div className="grid md:grid-cols-3 gap-8 mt-12">
            <div className="text-center">
              <div className="w-16 h-16 bg-vida-green/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <AcademicCapIcon className="h-8 w-8 text-vida-green" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Formation</h3>
              <p className="text-gray-600">30 activités agricoles, artisanales et environnementales</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-vida-earth/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <GlobeAltIcon className="h-8 w-8 text-vida-earth" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Agriculture Nouvelle</h3>
              <p className="text-gray-600">Durable, autonome et innovante</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-vida-warm/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <HeartIcon className="h-8 w-8 text-vida-warm" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Insertion Sociale</h3>
              <p className="text-gray-600">Par la pratique et la responsabilité</p>
            </div>
          </div>
        </div>
      </section>

      {/* Recommendations Section (for logged-in users) */}
      {user && (
        <section>
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center">
              <SparklesIcon className="h-6 w-6 text-vida-green mr-2" />
              <h2 className="text-2xl font-bold">Recommandations personnalisées</h2>
            </div>
          </div>
          
          {recLoading ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="animate-pulse">
                  <div className="bg-gray-200 rounded-lg h-64"></div>
                </div>
              ))}
            </div>
          ) : recommendations.length > 0 ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {recommendations.slice(0, 3).map((recommendation, index) => (
                <RecommendationCard
                  key={recommendation.activity.id}
                  recommendation={recommendation}
                  onSelect={(activity) => {
                    // Navigate to activity detail
                    window.location.href = `/activites/${activity.id}`;
                  }}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-12 bg-gray-50 rounded-lg">
              <p className="text-gray-600">
                Complétez votre profil pour obtenir des recommandations personnalisées !
              </p>
            </div>
          )}
        </section>
      )}

      {/* Featured Activities */}
      <section>
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold">Activités à la une</h2>
          <a 
            href="/activites"
            className="text-vida-green hover:text-vida-green/80 font-medium"
          >
            Voir toutes les activités →
          </a>
        </div>
        
        {activitiesLoading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="animate-pulse">
                <div className="bg-gray-200 rounded-lg h-64"></div>
              </div>
            ))}
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {activities.slice(0, 6).map((activity) => (
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
        )}
      </section>

      {/* Call to Action */}
      <section className="bg-gradient-to-r from-vida-green to-vida-sky rounded-2xl p-8 md:p-12 text-white text-center">
        <h2 className="text-2xl md:text-3xl font-bold mb-4">
          Prêt à rejoindre l'aventure ?
        </h2>
        <p className="text-lg mb-8 opacity-90">
          Découvrez nos formations pratiques et contribuez au développement d'une agriculture nouvelle.
        </p>
        
        {user ? (
          <a
            href="/dashboard"
            className="inline-block bg-white text-vida-green px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
          >
            Accéder à mon dashboard
          </a>
        ) : (
          <div className="space-x-4">
            <button
              onClick={() => {
                // This would trigger the auth modal from Navigation
                const registerBtn = document.querySelector('[data-auth="register"]') as HTMLButtonElement;
                registerBtn?.click();
              }}
              className="inline-block bg-white text-vida-green px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              S'inscrire maintenant
            </button>
            <a
              href="/activites"
              className="inline-block border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-vida-green transition-colors"
            >
              Explorer les activités
            </a>
          </div>
        )}
      </section>
    </div>
  );
}