"use client";

import { useState, useEffect } from "react";

interface Consultation {
  id: string;
  question: string;
  answer: string;
  category?: string;
  confidence_score?: number;
  created_at: string;
  session_id?: string;
}

interface ConsultationHistory {
  consultations: Consultation[];
  total_count: number;
  showing: number;
}

export default function AgriAssistant() {
  const [question, setQuestion] = useState("");
  const [context, setContext] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [currentConsultation, setCurrentConsultation] = useState<Consultation | null>(null);
  const [history, setHistory] = useState<ConsultationHistory | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Load consultation history on component mount
  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await fetch("/api/agri-assistant/history");
      if (response.ok) {
        const data = await response.json();
        setHistory(data);
      }
    } catch (err) {
      console.error("Error loading history:", err);
    }
  };

  const submitQuestion = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    if (!question.trim()) {
      setError("Veuillez poser une question");
      return;
    }

    setIsLoading(true);
    setError(null);
    setCurrentConsultation(null);

    try {
      const response = await fetch("/api/agri-assistant", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: question.trim(),
          context: context.trim() || undefined,
        }),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la consultation");
      }

      const consultation = await response.json();
      setCurrentConsultation(consultation);
      
      // Reload history to include the new consultation
      await loadHistory();
      
      // Clear the form
      setQuestion("");
      setContext("");
      
    } catch (err) {
      setError(err instanceof Error ? err.message : "Une erreur est survenue");
    } finally {
      setIsLoading(false);
    }
  };

  const formatAnswer = (answer: string) => {
    // Split answer into lines and format as markdown-like
    return answer.split('\n').map((line, index) => {
      const trimmedLine = line.trim();
      
      if (trimmedLine.startsWith('**') && trimmedLine.endsWith('**')) {
        // Bold headers
        return (
          <h3 key={index} className="font-bold text-lg mt-4 mb-2 text-green-800">
            {trimmedLine.slice(2, -2)}
          </h3>
        );
      } else if (trimmedLine.match(/^\d+\./)) {
        // Numbered lists
        return (
          <li key={index} className="ml-4 mb-2">
            {trimmedLine}
          </li>
        );
      } else if (trimmedLine) {
        // Regular paragraphs
        return (
          <p key={index} className="mb-2">
            {trimmedLine}
          </p>
        );
      } else {
        // Empty lines
        return <br key={index} />;
      }
    });
  };

  const getCategoryIcon = (category?: string) => {
    switch (category) {
      case 'sol': return '🌱';
      case 'plantes': return '🌿';
      case 'ravageurs': return '🐛';
      case 'irrigation': return '💧';
      case 'planification': return '📅';
      default: return '🌾';
    }
  };

  const getCategoryLabel = (category?: string) => {
    switch (category) {
      case 'sol': return 'Sol et compost';
      case 'plantes': return 'Plantes et cultures';
      case 'ravageurs': return 'Ravageurs et maladies';
      case 'irrigation': return 'Irrigation et arrosage';
      case 'planification': return 'Planification';
      default: return 'Général';
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-green-800 mb-4">
          🌾 Assistant Agricole IA
        </h1>
        <p className="text-lg text-gray-600">
          Obtenez des conseils personnalisés pour votre jardin et vos cultures
        </p>
      </div>

      {/* Question Form */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <h2 className="text-2xl font-semibold mb-4 text-green-700">
          Posez votre question agricole
        </h2>
        
        <form onSubmit={submitQuestion} className="space-y-4">
          <div>
            <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
              Votre question *
            </label>
            <textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ex: Comment améliorer un sol argileux ? Que faire contre les pucerons ?"
              className="w-full border border-gray-300 rounded-md px-3 py-2 h-24 focus:ring-2 focus:ring-green-500 focus:border-transparent"
              required
              disabled={isLoading}
            />
          </div>
          
          <div>
            <label htmlFor="context" className="block text-sm font-medium text-gray-700 mb-2">
              Contexte additionnel (optionnel)
            </label>
            <textarea
              id="context"
              value={context}
              onChange={(e) => setContext(e.target.value)}
              placeholder="Ex: Mon jardin est en région parisienne, sol argileux, exposition sud..."
              className="w-full border border-gray-300 rounded-md px-3 py-2 h-20 focus:ring-2 focus:ring-green-500 focus:border-transparent"
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading || !question.trim()}
            className="w-full bg-green-600 text-white py-3 px-6 rounded-md font-semibold hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? "🤖 Réflexion en cours..." : "🚀 Obtenir des conseils"}
          </button>
        </form>
      </div>

      {/* Current Consultation Result */}
      {currentConsultation && (
        <div className="bg-green-50 rounded-lg shadow-md p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-semibold text-green-800">
              Conseil de l'assistant IA
            </h2>
            <div className="flex items-center space-x-4">
              <span className="bg-green-200 text-green-800 px-3 py-1 rounded-full text-sm">
                {getCategoryIcon(currentConsultation.category)} {getCategoryLabel(currentConsultation.category)}
              </span>
              {currentConsultation.confidence_score && (
                <span className="text-sm text-gray-600">
                  Confiance: {Math.round(currentConsultation.confidence_score * 100)}%
                </span>
              )}
            </div>
          </div>
          
          <div className="bg-white rounded-md p-4 mb-4">
            <h3 className="font-semibold text-gray-800 mb-2">Votre question:</h3>
            <p className="text-gray-700 italic">"{currentConsultation.question}"</p>
          </div>
          
          <div className="text-gray-800 leading-relaxed">
            {formatAnswer(currentConsultation.answer)}
          </div>
        </div>
      )}

      {/* Consultation History */}
      {history && history.consultations.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-semibold text-green-700 mb-4">
            📚 Historique des consultations
          </h2>
          
          <div className="space-y-4">
            {history.consultations.map((consultation) => (
              <div key={consultation.id} className="border border-gray-200 rounded-md p-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded text-sm">
                    {getCategoryIcon(consultation.category)} {getCategoryLabel(consultation.category)}
                  </span>
                  <span className="text-sm text-gray-500">
                    {new Date(consultation.created_at).toLocaleDateString('fr-FR', {
                      day: 'numeric',
                      month: 'short',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                </div>
                
                <h3 className="font-medium text-gray-800 mb-2">
                  "{consultation.question}"
                </h3>
                
                <div className="text-sm text-gray-600 line-clamp-3">
                  {consultation.answer.split('\n')[0]}...
                </div>
                
                {consultation.confidence_score && (
                  <div className="mt-2 text-xs text-gray-500">
                    Confiance: {Math.round(consultation.confidence_score * 100)}%
                  </div>
                )}
              </div>
            ))}
          </div>
          
          {history.total_count > history.showing && (
            <div className="mt-4 text-center">
              <p className="text-sm text-gray-600">
                Affichage de {history.showing} sur {history.total_count} consultations
              </p>
            </div>
          )}
        </div>
      )}

      {/* Quick Tips */}
      <div className="mt-8 bg-blue-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold text-blue-800 mb-4">
          💡 Conseils pour de meilleures réponses
        </h2>
        <ul className="space-y-2 text-blue-700">
          <li>• Soyez précis dans vos questions (type de sol, région, problème observé)</li>
          <li>• Mentionnez votre niveau d'expérience en jardinage</li>
          <li>• Décrivez les conditions de votre jardin (exposition, climat)</li>
          <li>• N'hésitez pas à poser des questions de suivi pour approfondir</li>
        </ul>
      </div>
    </div>
  );
}