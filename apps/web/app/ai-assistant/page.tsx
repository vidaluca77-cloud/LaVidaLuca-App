"use client";
import React, { useState, useEffect } from "react";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

interface ActivityRecommendation {
  activity: {
    id: string;
    title: string;
    description: string;
    category: string;
    duration: number;
  };
  score: number;
  reasons: string[];
}

export default function AIAssistantPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: "Bonjour ! Je suis votre assistant IA spécialisé en agriculture et permaculture. Comment puis-je vous aider aujourd'hui ?",
      timestamp: new Date(),
    },
  ]);
  const [currentMessage, setCurrentMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [recommendations, setRecommendations] = useState<ActivityRecommendation[]>([]);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentMessage.trim() || loading) return;

    const userMessage: ChatMessage = {
      role: "user",
      content: currentMessage.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage("");
    setLoading(true);
    setError("");

    try {
      // Send to guide endpoint
      const guideResponse = await fetch(`${apiUrl}/api/v1/guide`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userMessage.content,
        }),
      });

      if (guideResponse.ok) {
        const guideData = await guideResponse.json();
        
        const assistantMessage: ChatMessage = {
          role: "assistant",
          content: guideData.answer || guideData.response || "Je n'ai pas pu traiter votre demande.",
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, assistantMessage]);

        // If user is logged in, also try to get activity recommendations
        if (isLoggedIn && userMessage.content.toLowerCase().includes("activité")) {
          await getActivityRecommendations(userMessage.content);
        }
      } else {
        throw new Error("Failed to get AI response");
      }
    } catch (err) {
      console.error("Error:", err);
      setError("Erreur de connexion. Veuillez réessayer.");
      
      // Fallback response
      const fallbackMessage: ChatMessage = {
        role: "assistant",
        content: "Je rencontre une difficulté technique. Pouvez-vous reformuler votre question ?",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, fallbackMessage]);
    } finally {
      setLoading(false);
    }
  };

  const getActivityRecommendations = async (userQuery: string) => {
    if (!isLoggedIn) return;

    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`${apiUrl}/api/v1/suggestions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          request: userQuery,
          max_suggestions: 3,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setRecommendations(data.data || []);
      }
    } catch (err) {
      console.error("Error getting recommendations:", err);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: "assistant",
        content: "Conversation effacée. Comment puis-je vous aider ?",
        timestamp: new Date(),
      },
    ]);
    setRecommendations([]);
    setError("");
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString("fr-FR", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const quickQuestions = [
    "Comment améliorer mon sol argileux ?",
    "Quelles activités pour débuter en permaculture ?",
    "Conseils pour un potager d'hiver",
    "Comment faire du compost rapidement ?",
    "Activités de jardinage pour les enfants",
  ];

  return (
    <div className="min-h-screen gradient-bg">
      {/* Navigation */}
      <nav className="container py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-green-500 to-earth-500 rounded-lg"></div>
            <a href="/" className="text-xl font-display font-semibold text-gradient">
              La Vida Luca
            </a>
          </div>
          <div className="hidden md:flex items-center space-x-8">
            <a href="/activites" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Activités
            </a>
            <a href="/proposer-aide" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
              Contribuer
            </a>
            {isLoggedIn && (
              <a href="/dashboard" className="text-neutral-700 hover:text-primary-600 transition-colors font-medium">
                Dashboard
              </a>
            )}
            <span className="text-primary-600 font-medium border-b-2 border-primary-600">
              Assistant IA
            </span>
          </div>
        </div>
      </nav>

      <main className="container pb-20">
        {/* Header */}
        <section className="text-center mb-8">
          <h1 className="text-gradient mb-4">
            Assistant IA Avancé
          </h1>
          <p className="text-xl text-neutral-600 mb-2 max-w-3xl mx-auto">
            Votre conseiller en agriculture, permaculture et vie durable
          </p>
          <p className="text-neutral-500 max-w-2xl mx-auto">
            Posez vos questions et obtenez des conseils personnalisés ainsi que des recommandations d'activités
          </p>
        </section>

        <div className="max-w-6xl mx-auto grid lg:grid-cols-3 gap-8">
          {/* Chat Interface */}
          <div className="lg:col-span-2">
            <div className="card h-[600px] flex flex-col">
              {/* Chat Header */}
              <div className="flex items-center justify-between p-4 border-b border-neutral-200">
                <h3 className="font-display font-semibold text-lg text-neutral-800">
                  💬 Conversation
                </h3>
                <button
                  onClick={clearChat}
                  className="text-sm text-neutral-500 hover:text-neutral-700 transition-colors"
                >
                  Effacer
                </button>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg ${
                        message.role === "user"
                          ? "bg-primary-600 text-white"
                          : "bg-neutral-100 text-neutral-800"
                      }`}
                    >
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">
                        {message.content}
                      </div>
                      <div
                        className={`text-xs mt-2 ${
                          message.role === "user" ? "text-primary-100" : "text-neutral-500"
                        }`}
                      >
                        {formatTime(message.timestamp)}
                      </div>
                    </div>
                  </div>
                ))}

                {loading && (
                  <div className="flex justify-start">
                    <div className="bg-neutral-100 px-4 py-3 rounded-lg max-w-xs">
                      <div className="flex items-center space-x-2">
                        <div className="animate-spin w-4 h-4 border-2 border-neutral-400 border-t-transparent rounded-full"></div>
                        <span className="text-sm text-neutral-600">Réflexion en cours...</span>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Error Message */}
              {error && (
                <div className="p-4 bg-red-50 border-t border-red-200">
                  <p className="text-red-700 text-sm">{error}</p>
                </div>
              )}

              {/* Message Input */}
              <form onSubmit={sendMessage} className="border-t border-neutral-200 p-4">
                <div className="flex space-x-4">
                  <input
                    type="text"
                    value={currentMessage}
                    onChange={(e) => setCurrentMessage(e.target.value)}
                    placeholder="Tapez votre question..."
                    className="flex-1 px-4 py-2 border border-neutral-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                    disabled={loading}
                  />
                  <button
                    type="submit"
                    disabled={loading || !currentMessage.trim()}
                    className={`btn btn-primary px-6 ${
                      loading || !currentMessage.trim() ? "opacity-50 cursor-not-allowed" : ""
                    }`}
                  >
                    Envoyer
                  </button>
                </div>
              </form>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Questions */}
            <div className="card">
              <h3 className="font-display font-semibold text-lg mb-4 text-neutral-800">
                💡 Questions rapides
              </h3>
              <div className="space-y-2">
                {quickQuestions.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => setCurrentMessage(question)}
                    className="w-full text-left p-3 border border-neutral-200 rounded-lg hover:bg-neutral-50 hover:border-primary-300 transition-all text-sm"
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>

            {/* Activity Recommendations */}
            {recommendations.length > 0 && (
              <div className="card">
                <h3 className="font-display font-semibold text-lg mb-4 text-neutral-800">
                  🎯 Activités recommandées
                </h3>
                <div className="space-y-3">
                  {recommendations.map((rec, index) => (
                    <div key={index} className="p-3 border border-neutral-200 rounded-lg hover:bg-neutral-50 transition-colors">
                      <h4 className="font-medium text-neutral-800 mb-1 text-sm">
                        {rec.activity.title}
                      </h4>
                      <p className="text-xs text-neutral-600 mb-2">
                        {rec.activity.description.substring(0, 80)}...
                      </p>
                      <div className="flex items-center justify-between text-xs">
                        <span className="text-primary-600">⭐ {Math.round(rec.score * 100)}%</span>
                        <span className="text-neutral-500">{rec.activity.duration} min</span>
                      </div>
                    </div>
                  ))}
                </div>
                <div className="mt-4">
                  <a href="/activites" className="btn btn-secondary w-full text-center">
                    Voir toutes les activités
                  </a>
                </div>
              </div>
            )}

            {/* User Status */}
            <div className="card">
              <h3 className="font-display font-semibold text-lg mb-4 text-neutral-800">
                👤 Statut utilisateur
              </h3>
              {isLoggedIn ? (
                <div className="space-y-2">
                  <div className="flex items-center text-green-600">
                    <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                    Connecté
                  </div>
                  <p className="text-sm text-neutral-600">
                    Vous bénéficiez de recommandations personnalisées
                  </p>
                  <a href="/dashboard" className="btn btn-primary w-full text-center">
                    Mon Dashboard
                  </a>
                </div>
              ) : (
                <div className="space-y-2">
                  <div className="flex items-center text-neutral-500">
                    <span className="w-2 h-2 bg-neutral-400 rounded-full mr-2"></span>
                    Non connecté
                  </div>
                  <p className="text-sm text-neutral-600">
                    Connectez-vous pour des conseils personnalisés
                  </p>
                  <a href="/auth" className="btn btn-primary w-full text-center">
                    Se connecter
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>

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