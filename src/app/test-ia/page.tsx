"use client";

import { useState } from "react";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface GuideResponse {
  activite: string;
  conseils: string[];
  materiel_necessaire: string[];
  etapes: string[];
  conseils_securite: string[];
  adapte_au_profil: boolean;
}

export default function TestIA() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: "Bonjour ! Je suis l'assistant IA de La Vida Luca 🌾\n\nJe peux t'aider avec les activités, la sécurité, le matériel et répondre à tes questions sur le projet.\n\nQue veux-tu savoir ?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [selectedActivity, setSelectedActivity] = useState("");
  const [guide, setGuide] = useState<GuideResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [apiUrl, setApiUrl] = useState(
    process.env.NEXT_PUBLIC_IA_API_URL || "http://localhost:8000"
  );

  const activities = [
    { id: "semis-plantation", name: "Semis & plantation" },
    { id: "elevage-soins", name: "Soins aux animaux d'élevage" },
  ];

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: inputMessage,
          contexte: "Test frontend Next.js",
          historique: messages.slice(-5).map(m => ({
            role: m.role,
            content: m.content
          }))
        }),
      });

      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status}`);
      }

      const data = await response.json();
      
      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: data.reponse,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error("Erreur lors de l'envoi du message:", error);
      const errorMessage: ChatMessage = {
        role: "assistant",
        content: `❌ Erreur de connexion à l'API: ${error instanceof Error ? error.message : 'Erreur inconnue'}\n\nVérifiez que l'API IA est démarrée sur ${apiUrl}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const getGuide = async () => {
    if (!selectedActivity) return;

    setIsLoading(true);
    try {
      const response = await fetch(`${apiUrl}/guide`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          activite_id: selectedActivity,
          profil_utilisateur: {
            niveau: "debutant",
            contexte: "test_frontend"
          },
          contexte: "Test depuis Next.js"
        }),
      });

      if (!response.ok) {
        throw new Error(`Erreur API: ${response.status}`);
      }

      const data = await response.json();
      setGuide(data);
    } catch (error) {
      console.error("Erreur lors de la récupération du guide:", error);
      alert(`Erreur: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    } finally {
      setIsLoading(false);
    }
  };

  const testApiHealth = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${apiUrl}/health`);
      const data = await response.json();
      alert(`✅ API connectée !\n\nStatus: ${data.status}\nService: ${data.service}\nVersion: ${data.version}`);
    } catch (error) {
      alert(`❌ Impossible de se connecter à l'API:\n${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Test de l'API IA - La Vida Luca
          </h1>
          <p className="text-gray-600">
            Interface de test pour les fonctionnalités IA du projet
          </p>
        </header>

        {/* Configuration API */}
        <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Configuration API</h2>
          <div className="flex gap-4 items-end">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                URL de l'API IA
              </label>
              <input
                type="text"
                value={apiUrl}
                onChange={(e) => setApiUrl(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-vida-green"
                placeholder="http://localhost:8000"
              />
            </div>
            <button
              onClick={testApiHealth}
              disabled={isLoading}
              className="px-4 py-2 bg-vida-green text-white rounded-md hover:bg-green-600 disabled:opacity-50"
            >
              {isLoading ? "Test..." : "Tester connexion"}
            </button>
          </div>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Chat IA */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-6 border-b">
              <h2 className="text-xl font-semibold">Chat avec l'IA</h2>
            </div>
            
            <div className="h-96 overflow-y-auto p-6 space-y-4">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2 ${
                      message.role === "user"
                        ? "bg-vida-green text-white"
                        : "bg-gray-100 text-gray-900"
                    }`}
                  >
                    <div className="whitespace-pre-wrap">{message.content}</div>
                    <div className="text-xs opacity-70 mt-1">
                      {message.timestamp.toLocaleTimeString()}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg px-4 py-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="p-6 border-t">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                  placeholder="Posez votre question..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-vida-green"
                  disabled={isLoading}
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !inputMessage.trim()}
                  className="px-4 py-2 bg-vida-green text-white rounded-md hover:bg-green-600 disabled:opacity-50"
                >
                  Envoyer
                </button>
              </div>
            </div>
          </div>

          {/* Guide d'activité */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="p-6 border-b">
              <h2 className="text-xl font-semibold">Guide d'activité</h2>
            </div>
            
            <div className="p-6">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Choisir une activité
                </label>
                <div className="flex gap-2">
                  <select
                    value={selectedActivity}
                    onChange={(e) => setSelectedActivity(e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-vida-green"
                  >
                    <option value="">Sélectionner une activité</option>
                    {activities.map((activity) => (
                      <option key={activity.id} value={activity.id}>
                        {activity.name}
                      </option>
                    ))}
                  </select>
                  <button
                    onClick={getGuide}
                    disabled={isLoading || !selectedActivity}
                    className="px-4 py-2 bg-vida-green text-white rounded-md hover:bg-green-600 disabled:opacity-50"
                  >
                    {isLoading ? "Chargement..." : "Obtenir le guide"}
                  </button>
                </div>
              </div>

              {guide && (
                <div className="space-y-4">
                  <div>
                    <h3 className="font-semibold text-lg text-vida-green">
                      {guide.activite}
                    </h3>
                    {guide.adapte_au_profil && (
                      <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full mt-1">
                        ✓ Adapté à votre profil
                      </span>
                    )}
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Conseils</h4>
                    <ul className="list-disc list-inside space-y-1 text-sm text-gray-700">
                      {guide.conseils.map((conseil, index) => (
                        <li key={index}>{conseil}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Matériel nécessaire</h4>
                    <div className="flex flex-wrap gap-2">
                      {guide.materiel_necessaire.map((materiel, index) => (
                        <span
                          key={index}
                          className="bg-gray-100 text-gray-800 text-xs px-2 py-1 rounded"
                        >
                          {materiel}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-2">Étapes</h4>
                    <ol className="list-decimal list-inside space-y-1 text-sm text-gray-700">
                      {guide.etapes.map((etape, index) => (
                        <li key={index}>{etape}</li>
                      ))}
                    </ol>
                  </div>

                  <div>
                    <h4 className="font-semibold text-red-700 mb-2">⚠️ Sécurité</h4>
                    <ul className="list-disc list-inside space-y-1 text-sm text-red-600">
                      {guide.conseils_securite.map((conseil, index) => (
                        <li key={index}>{conseil}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}