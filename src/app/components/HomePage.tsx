'use client';

import React from 'react';
import { HeartIcon, AcademicCapIcon, GlobeAltIcon } from '@heroicons/react/24/outline';

const HomePage = () => (
  <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-amber-50">
    {/* Header */}
    <header className="bg-white/90 backdrop-blur-sm border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">VL</span>
            </div>
            <span className="font-bold text-xl text-gray-900">La Vida Luca</span>
          </div>
          
          <nav className="hidden md:flex space-x-8">
            <a href="#mission" className="text-gray-700 hover:text-green-500 font-medium">
              Notre mission
            </a>
            <a href="#activites" className="text-gray-700 hover:text-green-500 font-medium">
              Activités
            </a>
            <a href="#contact" className="text-gray-700 hover:text-green-500 font-medium">
              Contact
            </a>
          </nav>
        </div>
      </div>
    </header>

    {/* Hero Section */}
    <section className="relative py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            <span className="text-green-500">Le cœur</span> avant l'argent
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Réseau national de fermes pédagogiques dédiées à la formation des jeunes 
            et au développement d'une agriculture vivante et respectueuse.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="bg-green-500 text-white px-8 py-4 rounded-lg font-medium hover:bg-green-600 transition-colors">
              Proposer mon aide
            </button>
            <button className="bg-white text-green-500 border-2 border-green-500 px-8 py-4 rounded-lg font-medium hover:bg-green-50 transition-colors">
              Découvrir nos activités
            </button>
          </div>
        </div>
      </div>
    </section>

    {/* Mission Section */}
    <section id="mission" className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Notre mission
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Trois piliers fondamentaux guident notre action quotidienne
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center p-8">
            <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-6">
              <AcademicCapIcon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Formation des jeunes</h3>
            <p className="text-gray-600">
              Partenariats avec les Maisons Familiales Rurales pour offrir aux élèves 
              une formation pratique et humaine dans un cadre authentique.
            </p>
          </div>

          <div className="text-center p-8">
            <div className="w-16 h-16 bg-amber-600 rounded-full flex items-center justify-center mx-auto mb-6">
              <GlobeAltIcon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Agriculture vivante</h3>
            <p className="text-gray-600">
              Développement de pratiques agricoles durables respectueuses 
              de l'environnement et du bien-être animal.
            </p>
          </div>

          <div className="text-center p-8">
            <div className="w-16 h-16 bg-amber-400 rounded-full flex items-center justify-center mx-auto mb-6">
              <HeartIcon className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-4">Insertion sociale</h3>
            <p className="text-gray-600">
              Accompagnement personnalisé de chaque jeune vers l'autonomie 
              et l'épanouissement personnel et professionnel.
            </p>
          </div>
        </div>
      </div>
    </section>

    {/* Contact */}
    <section id="contact" className="py-20 bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">
          Rejoignez l'aventure La Vida Luca
        </h2>
        <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Snapchat</h3>
            <p className="text-green-500 font-medium">@lavidaluca77</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h3 className="font-semibold text-gray-900 mb-2">Email</h3>
            <p className="text-green-500 font-medium">vidaluca77@gmail.com</p>
          </div>
        </div>
      </div>
    </section>
  </div>
);

export default HomePage;