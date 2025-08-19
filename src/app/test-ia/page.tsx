"use client";

import { useState } from "react";

// Types
interface UserProfile {
  skills: string[];
  availability: string[];
  location: string;
  preferences: string[];
}

interface Activity {
  id: string;
  title: string;
  category: string;
  summary: string;
  duration_min: number;
  skill_tags: string[];
  safety_level: number;
  compatibility_score?: number;
}

interface GuideResponse {
  suggestions: Activity[];
  safety_guide: {
    rules: string[];
    checklist: string[];
    safety_level: number;
    required_materials: string[];
  };
  personalized_tips: string[];
}

interface ChatMessage {
  message: string;
  isUser: boolean;
  timestamp: Date;
}

export default function TestIA() {
  // États pour le profil utilisateur
  const [profile, setProfile] = useState<UserProfile>({
    skills: [],
    availability: [],
    location: "",
    preferences: []
  });

  // États pour les résultats
  const [guideResult, setGuideResult] = useState<GuideResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // États pour le chat
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);

  // Configuration API
  const API_BASE_URL = process.env.NEXT_PUBLIC_IA_API_URL || "http://localhost:8000";

  // Options disponibles
  const skillOptions = [
    'elevage', 'hygiene', 'soins_animaux', 'sol', 'plantes', 'organisation',
    'securite', 'bois', 'precision', 'creativite', 'patience', 'endurance',
    'ecologie', 'accueil', 'pedagogie', 'expression', 'equipe'
  ];

  const availabilityOptions = [
    'weekend', 'semaine', 'matin', 'apres-midi', 'vacances'
  ];

  const categoryOptions = [
    'agri', 'artisanat', 'nature', 'social'
  ];

  // Handlers pour le profil
  const handleSkillToggle = (skill: string) => {
    setProfile(prev => ({
      ...prev,
      skills: prev.skills.includes(skill)
        ? prev.skills.filter(s => s !== skill)
        : [...prev.skills, skill]
    }));
  };

  const handleAvailabilityToggle = (availability: string) => {
    setProfile(prev => ({
      ...prev,
      availability: prev.availability.includes(availability)
        ? prev.availability.filter(a => a !== availability)
        : [...prev.availability, availability]
    }));
  };

  const handlePreferenceToggle = (preference: string) => {
    setProfile(prev => ({
      ...prev,
      preferences: prev.preferences.includes(preference)
        ? prev.preferences.filter(p => p !== preference)
        : [...prev.preferences, preference]
    }));
  };

  // Test de l'endpoint /guide
  const testGuideEndpoint = async () => {
    setLoading(true);
    setError(null);
    setGuideResult(null);

    try {
      const response = await fetch(`${API_BASE_URL}/guide`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ profile })
      });

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data: GuideResponse = await response.json();
      setGuideResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  // Test de l'endpoint /chat
  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage: ChatMessage = {
      message: chatInput,
      isUser: true,
      timestamp: new Date()
    };

    setChatMessages(prev => [...prev, userMessage]);
    setChatLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: chatInput })
      });

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      const aiMessage: ChatMessage = {
        message: data.response,
        isUser: false,
        timestamp: new Date()
      };

      setChatMessages(prev => [...prev, aiMessage]);
    } catch (err) {
      const errorMessage: ChatMessage = {
        message: `Erreur: ${err instanceof Error ? err.message : 'Erreur inconnue'}`,
        isUser: false,
        timestamp: new Date()
      };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setChatLoading(false);
      setChatInput("");
    }
  };

  // Test de l'endpoint /health
  const testHealthEndpoint = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const data = await response.json();
      
      const healthMessage: ChatMessage = {
        message: `✅ API disponible - Status: ${data.status}, Version: ${data.version}`,
        isUser: false,
        timestamp: new Date()
      };
      setChatMessages(prev => [...prev, healthMessage]);
    } catch (err) {
      const errorMessage: ChatMessage = {
        message: `❌ API non disponible: ${err instanceof Error ? err.message : 'Erreur inconnue'}`,
        isUser: false,
        timestamp: new Date()
      };
      setChatMessages(prev => [...prev, errorMessage]);
    }
  };

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (hours > 0) {
      return `${hours}h${mins > 0 ? mins.toString().padStart(2, '0') : ''}`;
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

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Test de l'IA La Vida Luca
        </h1>
        <p className="text-gray-600">
          Interface de test pour les endpoints de l'API IA
        </p>
        <div className="mt-4">
          <button
            onClick={testHealthEndpoint}
            className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Tester la connexion API
          </button>
        </div>
      </div>

      {/* Configuration du profil */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Configuration du profil utilisateur
        </h2>

        {/* Compétences */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-700 mb-3">Compétences</h3>
          <div className="flex flex-wrap gap-2">
            {skillOptions.map(skill => (
              <button
                key={skill}
                onClick={() => handleSkillToggle(skill)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  profile.skills.includes(skill)
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {skill}
              </button>
            ))}
          </div>
        </div>

        {/* Disponibilités */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-700 mb-3">Disponibilités</h3>
          <div className="flex flex-wrap gap-2">
            {availabilityOptions.map(availability => (
              <button
                key={availability}
                onClick={() => handleAvailabilityToggle(availability)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  profile.availability.includes(availability)
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {availability}
              </button>
            ))}
          </div>
        </div>

        {/* Préférences de catégories */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-700 mb-3">Préférences</h3>
          <div className="flex flex-wrap gap-2">
            {categoryOptions.map(category => (
              <button
                key={category}
                onClick={() => handlePreferenceToggle(category)}
                className={`px-3 py-1 rounded-full text-sm transition-colors ${
                  profile.preferences.includes(category)
                    ? 'bg-purple-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Localisation */}
        <div className="mb-6">
          <h3 className="text-lg font-medium text-gray-700 mb-3">Localisation</h3>
          <input
            type="text"
            value={profile.location}
            onChange={(e) => setProfile(prev => ({ ...prev, location: e.target.value }))}
            placeholder="Ex: Ferme de Bel Air, Lyon..."
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>

        {/* Bouton de test */}
        <button
          onClick={testGuideEndpoint}
          disabled={loading}
          className="w-full bg-green-500 text-white py-3 px-4 rounded-lg font-medium hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Test en cours...' : 'Tester l\'endpoint /guide'}
        </button>
      </div>

      {/* Résultats du guide */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h3 className="text-red-800 font-medium">Erreur</h3>
          <p className="text-red-600">{error}</p>
        </div>
      )}

      {guideResult && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">
            Résultats du guide personnalisé
          </h2>

          {/* Suggestions d'activités */}
          <div className="mb-6">
            <h3 className="text-lg font-medium text-gray-700 mb-3">
              Activités suggérées ({guideResult.suggestions.length})
            </h3>
            <div className="space-y-4">
              {guideResult.suggestions.map((activity, index) => (
                <div key={activity.id} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-medium text-gray-900">{activity.title}</h4>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 rounded-full text-xs ${getSafetyColor(activity.safety_level)}`}>
                        {getSafetyText(activity.safety_level)}
                      </span>
                      <span className="text-sm text-gray-500">
                        Score: {(activity.compatibility_score! * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm mb-2">{activity.summary}</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span>⏱️ {formatDuration(activity.duration_min)}</span>
                    <span>🏷️ {activity.category}</span>
                    <span>🔧 {activity.skill_tags.join(', ')}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Guide de sécurité */}
          {guideResult.safety_guide && (
            <div className="mb-6">
              <h3 className="text-lg font-medium text-gray-700 mb-3">Guide de sécurité</h3>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="mb-4">
                  <h4 className="font-medium text-gray-900 mb-2">Règles de sécurité</h4>
                  <ul className="space-y-1">
                    {guideResult.safety_guide.rules.map((rule, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <span className="text-red-500 mr-2">•</span>
                        {rule}
                      </li>
                    ))}
                  </ul>
                </div>
                <div className="mb-4">
                  <h4 className="font-medium text-gray-900 mb-2">Checklist</h4>
                  <ul className="space-y-1">
                    {guideResult.safety_guide.checklist.map((item, index) => (
                      <li key={index} className="text-sm text-gray-600 flex items-start">
                        <span className="text-green-500 mr-2">✓</span>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
                {guideResult.safety_guide.required_materials.length > 0 && (
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Matériel requis</h4>
                    <div className="flex flex-wrap gap-2">
                      {guideResult.safety_guide.required_materials.map((material, index) => (
                        <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                          {material}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Conseils personnalisés */}
          {guideResult.personalized_tips.length > 0 && (
            <div>
              <h3 className="text-lg font-medium text-gray-700 mb-3">Conseils personnalisés</h3>
              <ul className="space-y-2">
                {guideResult.personalized_tips.map((tip, index) => (
                  <li key={index} className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-sm text-amber-800">
                    💡 {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Chat avec l'IA */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          Chat avec l'IA
        </h2>

        {/* Messages */}
        <div className="bg-gray-50 rounded-lg p-4 h-64 overflow-y-auto mb-4">
          {chatMessages.length === 0 ? (
            <p className="text-gray-500 text-center py-8">
              Commencez une conversation avec l'IA...
            </p>
          ) : (
            <div className="space-y-3">
              {chatMessages.map((message, index) => (
                <div key={index} className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    message.isUser
                      ? 'bg-green-500 text-white'
                      : 'bg-white border border-gray-200 text-gray-800'
                  }`}>
                    <p className="text-sm">{message.message}</p>
                    <p className="text-xs opacity-70 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </p>
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div className="flex justify-start">
                  <div className="bg-white border border-gray-200 text-gray-800 px-4 py-2 rounded-lg">
                    <p className="text-sm">L'IA réfléchit...</p>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input de chat */}
        <div className="flex space-x-2">
          <input
            type="text"
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
            placeholder="Posez votre question à l'IA..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
            disabled={chatLoading}
          />
          <button
            onClick={sendChatMessage}
            disabled={chatLoading || !chatInput.trim()}
            className="bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Envoyer
          </button>
        </div>
      </div>
    </div>
  );
}