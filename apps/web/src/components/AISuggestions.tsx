'use client'

import React, { useState } from 'react'
import { useGenerateSuggestionsMutation } from '../lib/api/suggestionsApi'
import { useSelector } from 'react-redux'
import type { RootState } from '../lib/store'

interface UserPreferences {
  skills: string[]
  interests: string[]
  experience_level: 'beginner' | 'intermediate' | 'advanced'
  available_time: number
  location_preference: string
  learning_goals: string[]
}

export default function AISuggestions() {
  const [preferences, setPreferences] = useState<UserPreferences>({
    skills: [],
    interests: [],
    experience_level: 'beginner',
    available_time: 60,
    location_preference: '',
    learning_goals: []
  })
  const [query, setQuery] = useState('')
  const [generateSuggestions, { data: suggestions, isLoading, error }] = useGenerateSuggestionsMutation()
  
  const { isAuthenticated } = useSelector((state: RootState) => state.auth)

  const skillOptions = [
    'agriculture', 'elevage', 'transformation', 'artisanat', 'menuiserie',
    'jardinage', 'apiculture', 'fromagerie', 'boulangerie', 'mecanique',
    'electricite', 'plomberie', 'maconnerie', 'informatique', 'comptabilite'
  ]

  const interestOptions = [
    'agri', 'transfo', 'artisanat', 'nature', 'social', 'technique',
    'commercial', 'gestion', 'environnement', 'innovation', 'tradition'
  ]

  const learningGoalOptions = [
    'obtenir_diplome', 'competences_professionnelles', 'reconversion',
    'perfectionnement', 'creation_entreprise', 'developpement_personnel'
  ]

  const handleSkillToggle = (skill: string) => {
    setPreferences(prev => ({
      ...prev,
      skills: prev.skills.includes(skill)
        ? prev.skills.filter(s => s !== skill)
        : [...prev.skills, skill]
    }))
  }

  const handleInterestToggle = (interest: string) => {
    setPreferences(prev => ({
      ...prev,
      interests: prev.interests.includes(interest)
        ? prev.interests.filter(i => i !== interest)
        : [...prev.interests, interest]
    }))
  }

  const handleGoalToggle = (goal: string) => {
    setPreferences(prev => ({
      ...prev,
      learning_goals: prev.learning_goals.includes(goal)
        ? prev.learning_goals.filter(g => g !== goal)
        : [...prev.learning_goals, goal]
    }))
  }

  const handleGenerateSuggestions = async () => {
    if (!query.trim()) return

    try {
      await generateSuggestions({
        preferences: JSON.stringify(preferences),
        limit: 5
      }).unwrap()
    } catch (err) {
      console.error('Error generating suggestions:', err)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreWidth = (score: number) => {
    return `${score}%`
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-lg shadow-lg">
        <div className="p-6 border-b border-gray-200">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">
            🤖 Suggestions IA Personnalisées
          </h1>
          <p className="text-gray-600">
            Décrivez vos objectifs et préférences pour recevoir des suggestions d'activités adaptées
          </p>
        </div>

        <div className="p-6">
          {/* Query Input */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Que souhaitez-vous apprendre ou accomplir ?
            </label>
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ex: Je veux apprendre l'élevage de chèvres pour créer ma fromagerie..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 h-24 resize-none"
            />
          </div>

          {/* Preferences Form */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            {/* Skills */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Compétences actuelles
              </label>
              <div className="flex flex-wrap gap-2">
                {skillOptions.map((skill) => (
                  <button
                    key={skill}
                    onClick={() => handleSkillToggle(skill)}
                    className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                      preferences.skills.includes(skill)
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {skill}
                  </button>
                ))}
              </div>
            </div>

            {/* Interests */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Centres d'intérêt
              </label>
              <div className="flex flex-wrap gap-2">
                {interestOptions.map((interest) => (
                  <button
                    key={interest}
                    onClick={() => handleInterestToggle(interest)}
                    className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                      preferences.interests.includes(interest)
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {interest}
                  </button>
                ))}
              </div>
            </div>

            {/* Experience Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Niveau d'expérience
              </label>
              <select
                value={preferences.experience_level}
                onChange={(e) => setPreferences({
                  ...preferences,
                  experience_level: e.target.value as UserPreferences['experience_level']
                })}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="beginner">Débutant</option>
                <option value="intermediate">Intermédiaire</option>
                <option value="advanced">Avancé</option>
              </select>
            </div>

            {/* Available Time */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Temps disponible (minutes)
              </label>
              <input
                type="range"
                min="30"
                max="240"
                step="15"
                value={preferences.available_time}
                onChange={(e) => setPreferences({
                  ...preferences,
                  available_time: parseInt(e.target.value)
                })}
                className="w-full"
              />
              <div className="text-center text-sm text-gray-600 mt-1">
                {preferences.available_time} minutes
              </div>
            </div>

            {/* Learning Goals */}
            <div className="lg:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Objectifs d'apprentissage
              </label>
              <div className="flex flex-wrap gap-2">
                {learningGoalOptions.map((goal) => (
                  <button
                    key={goal}
                    onClick={() => handleGoalToggle(goal)}
                    className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                      preferences.learning_goals.includes(goal)
                        ? 'bg-purple-600 text-white'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {goal.replace('_', ' ')}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Generate Button */}
          <div className="flex justify-center">
            <button
              onClick={handleGenerateSuggestions}
              disabled={!query.trim() || isLoading}
              className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium rounded-lg hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Génération en cours...
                </div>
              ) : (
                '✨ Générer des suggestions'
              )}
            </button>
          </div>
        </div>

        {/* Results */}
        {error && (
          <div className="p-6 border-t border-gray-200">
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <div className="text-red-800">
                Erreur lors de la génération des suggestions. Veuillez réessayer.
              </div>
            </div>
          </div>
        )}

        {suggestions && suggestions.length > 0 && (
          <div className="p-6 border-t border-gray-200">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Suggestions pour vous
            </h2>
            <div className="space-y-4">
              {suggestions.map((suggestion, index) => (
                <div key={index} className="bg-gray-50 rounded-lg p-4 border border-gray-200">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">
                        {suggestion.activity.title}
                      </h3>
                      <div className="flex items-center gap-4 mt-1 text-sm text-gray-600">
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">
                          {suggestion.activity.category}
                        </span>
                        <span>{suggestion.activity.duration_min} min</span>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className={`text-lg font-bold ${getScoreColor(suggestion.score)}`}>
                        {suggestion.score}%
                      </div>
                      <div className="w-20 bg-gray-200 rounded-full h-2 mt-1">
                        <div
                          className="bg-gradient-to-r from-blue-500 to-green-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: getScoreWidth(suggestion.score) }}
                        ></div>
                      </div>
                    </div>
                  </div>

                  <p className="text-gray-700 mb-3">
                    {suggestion.activity.summary}
                  </p>

                  {suggestion.reasons && suggestion.reasons.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">
                        Pourquoi cette activité vous convient :
                      </h4>
                      <ul className="list-disc list-inside text-sm text-gray-600 space-y-1">
                        {suggestion.reasons.map((reason, reasonIndex) => (
                          <li key={reasonIndex}>{reason}</li>
                        ))}
                      </ul>
                    </div>
                  )}

                  <div className="mt-4 flex gap-2">
                    <button className="px-4 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700">
                      Voir les détails
                    </button>
                    <button className="px-4 py-2 border border-gray-300 text-gray-700 text-sm rounded-md hover:bg-gray-50">
                      Sauvegarder
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Authentication Notice */}
        {!isAuthenticated && (
          <div className="p-6 border-t border-gray-200 bg-yellow-50">
            <div className="flex items-center gap-3">
              <div className="text-yellow-600">
                ℹ️
              </div>
              <div>
                <div className="font-medium text-yellow-800">
                  Connexion recommandée
                </div>
                <div className="text-yellow-700 text-sm">
                  Connectez-vous pour sauvegarder vos préférences et recevoir des suggestions encore plus personnalisées.
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}