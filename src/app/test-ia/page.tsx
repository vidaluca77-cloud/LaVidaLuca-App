"use client";

import { useState } from "react";

// Interface pour les réponses de l'API
interface HealthResponse {
  status: string;
  message: string;
  version: string;
}

interface GuideResponse {
  culture: string;
  conseils: string[];
  calendrier: string[];
  ressources: string[];
  niveau_difficulte: string;
}

interface ChatResponse {
  reponse: string;
  suggestions: string[];
  ressources_utiles: string[];
}

export default function TestIAPage() {
  const [apiUrl, setApiUrl] = useState(
    process.env.NEXT_PUBLIC_IA_API_URL || "http://localhost:8000"
  );
  const [healthData, setHealthData] = useState<HealthResponse | null>(null);
  const [guideData, setGuideData] = useState<GuideResponse | null>(null);
  const [chatData, setChatData] = useState<ChatResponse | null>(null);
  const [loading, setLoading] = useState<{
    health: boolean;
    guide: boolean;
    chat: boolean;
  }>({
    health: false,
    guide: false,
    chat: false,
  });
  const [errors, setErrors] = useState<{
    health?: string;
    guide?: string;
    chat?: string;
  }>({});

  // Test de l'endpoint /health
  const testHealth = async () => {
    setLoading((prev) => ({ ...prev, health: true }));
    setErrors((prev) => ({ ...prev, health: undefined }));

    try {
      const response = await fetch(`${apiUrl}/health`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      setHealthData(data);
    } catch (error) {
      setErrors((prev) => ({
        ...prev,
        health: error instanceof Error ? error.message : "Erreur inconnue",
      }));
    } finally {
      setLoading((prev) => ({ ...prev, health: false }));
    }
  };

  // Test de l'endpoint /guide
  const testGuide = async () => {
    setLoading((prev) => ({ ...prev, guide: true }));
    setErrors((prev) => ({ ...prev, guide: undefined }));

    try {
      const response = await fetch(`${apiUrl}/guide`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          culture: "tomates",
          saison: "printemps",
          region: "Provence",
          niveau: "débutant",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      setGuideData(data);
    } catch (error) {
      setErrors((prev) => ({
        ...prev,
        guide: error instanceof Error ? error.message : "Erreur inconnue",
      }));
    } finally {
      setLoading((prev) => ({ ...prev, guide: false }));
    }
  };

  // Test de l'endpoint /chat
  const testChat = async () => {
    setLoading((prev) => ({ ...prev, chat: true }));
    setErrors((prev) => ({ ...prev, chat: undefined }));

    try {
      const response = await fetch(`${apiUrl}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: "Bonjour, j'ai besoin d'aide pour débuter en agriculture",
          contexte: "formation MFR",
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      setChatData(data);
    } catch (error) {
      setErrors((prev) => ({
        ...prev,
        chat: error instanceof Error ? error.message : "Erreur inconnue",
      }));
    } finally {
      setLoading((prev) => ({ ...prev, chat: false }));
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="mx-auto max-w-4xl px-4">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
            Test de l'API IA - La Vida Luca
          </h1>

          {/* Configuration de l'URL */}
          <div className="mb-8 p-6 bg-blue-50 rounded-lg">
            <h2 className="text-lg font-semibold text-blue-900 mb-4">
              Configuration API
            </h2>
            <div className="flex gap-4 items-end">
              <div className="flex-1">
                <label
                  htmlFor="api-url"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  URL de l'API IA
                </label>
                <input
                  id="api-url"
                  type="text"
                  value={apiUrl}
                  onChange={(e) => setApiUrl(e.target.value)}
                  className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="http://localhost:8000"
                />
              </div>
            </div>
          </div>

          {/* Tests des endpoints */}
          <div className="space-y-8">
            {/* Test Health */}
            <div className="border border-gray-200 rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold text-gray-900">
                  Test /health
                </h3>
                <button
                  onClick={testHealth}
                  disabled={loading.health}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading.health ? "Test en cours..." : "Tester"}
                </button>
              </div>

              {errors.health && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-red-800">Erreur: {errors.health}</p>
                </div>
              )}

              {healthData && (
                <div className="bg-green-50 border border-green-200 rounded-md p-4">
                  <h4 className="font-semibold text-green-800 mb-2">
                    Réponse:
                  </h4>
                  <pre className="text-sm text-green-700 whitespace-pre-wrap">
                    {JSON.stringify(healthData, null, 2)}
                  </pre>
                </div>
              )}
            </div>

            {/* Test Guide */}
            <div className="border border-gray-200 rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold text-gray-900">
                  Test /guide
                </h3>
                <button
                  onClick={testGuide}
                  disabled={loading.guide}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading.guide ? "Test en cours..." : "Tester"}
                </button>
              </div>

              <div className="mb-4 p-4 bg-gray-50 rounded-md">
                <p className="text-sm text-gray-600">
                  <strong>Paramètres du test:</strong> culture=tomates,
                  saison=printemps, région=Provence, niveau=débutant
                </p>
              </div>

              {errors.guide && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-red-800">Erreur: {errors.guide}</p>
                </div>
              )}

              {guideData && (
                <div className="bg-blue-50 border border-blue-200 rounded-md p-4">
                  <h4 className="font-semibold text-blue-800 mb-4">
                    Guide pour {guideData.culture}:
                  </h4>
                  <div className="space-y-4 text-blue-700">
                    <div>
                      <h5 className="font-medium">Conseils:</h5>
                      <ul className="list-disc list-inside ml-4">
                        {guideData.conseils.map((conseil, index) => (
                          <li key={index} className="text-sm">
                            {conseil}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5 className="font-medium">Ressources:</h5>
                      <ul className="list-disc list-inside ml-4">
                        {guideData.ressources.map((ressource, index) => (
                          <li key={index} className="text-sm">
                            {ressource}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Test Chat */}
            <div className="border border-gray-200 rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-semibold text-gray-900">
                  Test /chat
                </h3>
                <button
                  onClick={testChat}
                  disabled={loading.chat}
                  className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading.chat ? "Test en cours..." : "Tester"}
                </button>
              </div>

              <div className="mb-4 p-4 bg-gray-50 rounded-md">
                <p className="text-sm text-gray-600">
                  <strong>Message du test:</strong> "Bonjour, j'ai besoin d'aide
                  pour débuter en agriculture"
                </p>
              </div>

              {errors.chat && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-red-8">Erreur: {errors.chat}</p>
                </div>
              )}

              {chatData && (
                <div className="bg-purple-50 border border-purple-200 rounded-md p-4">
                  <h4 className="font-semibold text-purple-800 mb-4">
                    Réponse du chat:
                  </h4>
                  <div className="space-y-4 text-purple-700">
                    <div>
                      <h5 className="font-medium">Réponse:</h5>
                      <p className="text-sm">{chatData.reponse}</p>
                    </div>
                    <div>
                      <h5 className="font-medium">Suggestions:</h5>
                      <ul className="list-disc list-inside ml-4">
                        {chatData.suggestions.map((suggestion, index) => (
                          <li key={index} className="text-sm">
                            {suggestion}
                          </li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <h5 className="font-medium">Ressources utiles:</h5>
                      <ul className="list-disc list-inside ml-4">
                        {chatData.ressources_utiles.map((ressource, index) => (
                          <li key={index} className="text-sm">
                            {ressource}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Instructions */}
          <div className="mt-8 p-6 bg-yellow-50 border border-yellow-200 rounded-lg">
            <h3 className="text-lg font-semibold text-yellow-800 mb-2">
              Instructions
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-sm text-yellow-700">
              <li>
                Assurez-vous que l'API FastAPI est démarrée sur le port configuré
              </li>
              <li>
                Pour démarrer l'API en local: <code>cd apps/ia && python main.py</code>
              </li>
              <li>Testez chaque endpoint pour vérifier le bon fonctionnement</li>
              <li>
                Vérifiez que les réponses correspondent aux attentes
              </li>
              <li>
                En cas d'erreur CORS, vérifiez la configuration ALLOWED_ORIGINS
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>
  );
}