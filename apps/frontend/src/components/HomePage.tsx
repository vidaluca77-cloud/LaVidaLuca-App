'use client';

import React from 'react';
import { HeartIcon, AcademicCapIcon, GlobeAltIcon } from '@heroicons/react/24/outline';
import { useAuth } from '../hooks/useAuth';
import Link from 'next/link';

const HomePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-4xl mx-auto">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-4xl font-bold mb-4 text-gray-900">
          La Vida Luca
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Réseau de fermes autonomes & pédagogiques — formation, insertion et agriculture vivante
        </p>
        
        {!user ? (
          <div className="flex gap-4 justify-center">
            <Link 
              href="/rejoindre"
              className="bg-vida-green text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors"
            >
              Rejoindre le projet
            </Link>
            <Link 
              href="/catalogue"
              className="border border-vida-green text-vida-green px-6 py-3 rounded-lg hover:bg-green-50 transition-colors"
            >
              Découvrir nos activités
            </Link>
          </div>
        ) : (
          <div className="flex gap-4 justify-center">
            <Link 
              href="/catalogue"
              className="bg-vida-green text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors"
            >
              Voir mes recommandations
            </Link>
            <Link 
              href="/profil"
              className="border border-vida-green text-vida-green px-6 py-3 rounded-lg hover:bg-green-50 transition-colors"
            >
              Mon profil
            </Link>
          </div>
        )}
      </section>

      {/* Vision Section */}
      <section className="py-12">
        <h2 className="text-3xl font-bold text-center mb-8">Notre Vision</h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="mb-4 flex justify-center">
              <AcademicCapIcon className="w-12 h-12 text-vida-green" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Formation</h3>
            <p className="text-gray-600">
              Former et accompagner les jeunes en MFR via un catalogue de 30 activités agricoles, artisanales et environnementales.
            </p>
          </div>
          
          <div className="text-center">
            <div className="mb-4 flex justify-center">
              <GlobeAltIcon className="w-12 h-12 text-vida-green" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Agriculture Nouvelle</h3>
            <p className="text-gray-600">
              Développer une agriculture durable, autonome et innovante pour l'avenir.
            </p>
          </div>
          
          <div className="text-center">
            <div className="mb-4 flex justify-center">
              <HeartIcon className="w-12 h-12 text-vida-green" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Insertion Sociale</h3>
            <p className="text-gray-600">
              Favoriser l'insertion sociale par la pratique, la responsabilité et l'engagement.
            </p>
          </div>
        </div>
      </section>

      {/* Activities Preview */}
      <section className="py-12 bg-gray-50 rounded-lg">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold mb-4">Nos Domaines d'Activité</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Découvrez notre catalogue de 30 activités spécialement conçues pour la formation en Maison Familiale Rurale.
          </p>
        </div>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4 max-w-4xl mx-auto">
          {[
            { name: 'Agriculture', color: 'bg-vida-green', desc: 'Élevage, cultures, soins aux animaux' },
            { name: 'Transformation', color: 'bg-vida-warm', desc: 'Produits fermiers, conservation' },
            { name: 'Artisanat', color: 'bg-vida-earth', desc: 'Savoir-faire traditionnels' },
            { name: 'Nature', color: 'bg-green-500', desc: 'Écologie, permaculture' },
            { name: 'Social', color: 'bg-vida-sky', desc: 'Échanges, pédagogie' },
          ].map((category) => (
            <div key={category.name} className="bg-white p-4 rounded-lg shadow-sm">
              <div className={`w-8 h-8 ${category.color} rounded mb-2`}></div>
              <h3 className="font-semibold">{category.name}</h3>
              <p className="text-sm text-gray-600">{category.desc}</p>
            </div>
          ))}
        </div>
        
        <div className="text-center mt-8">
          <Link 
            href="/catalogue"
            className="bg-vida-green text-white px-6 py-3 rounded-lg hover:bg-green-600 transition-colors inline-block"
          >
            Voir toutes les activités
          </Link>
        </div>
      </section>

      {/* Call to Action */}
      {!user && (
        <section className="py-12 text-center">
          <h2 className="text-2xl font-bold mb-4">Prêt à vous lancer ?</h2>
          <p className="text-gray-600 mb-6">
            Rejoignez notre communauté et découvrez les activités qui vous correspondent.
          </p>
          <Link 
            href="/rejoindre"
            className="bg-vida-green text-white px-8 py-3 rounded-lg hover:bg-green-600 transition-colors inline-block"
          >
            Créer mon profil
          </Link>
        </section>
      )}
    </div>
  );
};

export default HomePage;