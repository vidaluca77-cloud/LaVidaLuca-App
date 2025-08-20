'use client';

import { useState, useEffect } from 'react';
import { ChatBubbleLeftRightIcon, SparklesIcon, ClockIcon, TrashIcon } from '@heroicons/react/24/outline';

interface Consultation {
  id: number;
  question: string;
  response: string;
  category?: string;
  created_at: string;
}

interface Category {
  value: string;
  label: string;
}

export default function AgriAssistantPage() {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [category, setCategory] = useState('');
  const [history, setHistory] = useState<Consultation[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [sessionId] = useState(() => crypto.randomUUID());

  // Load categories and history on component mount
  useEffect(() => {
    loadCategories();
    loadHistory();
  }, []);

  const loadCategories = async () => {
    try {
      const res = await fetch('/api/agri-assistant/categories');
      const data = await res.json();
      setCategories(data.categories || []);
    } catch (error) {
      console.error('Error loading categories:', error);
    }
  };

  const loadHistory = async () => {
    try {
      const res = await fetch(`/api/agri-assistant/history?session_id=${sessionId}`);
      if (res.ok) {
        const data = await res.json();
        setHistory(data);
      }
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    setResponse('');

    try {
      const res = await fetch('/api/agri-assistant/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question.trim(),
          category: category || null,
          session_id: sessionId,
        }),
      });

      if (!res.ok) {
        throw new Error('Erreur lors de la consultation');
      }

      const data = await res.json();
      setResponse(data.response);
      
      // Add to history locally
      const newConsultation: Consultation = {
        id: Date.now(), // temporary ID
        question: question.trim(),
        response: data.response,
        category: category || undefined,
        created_at: new Date().toISOString(),
      };
      
      setHistory(prev => [newConsultation, ...prev]);
      setQuestion('');
      setCategory('');
    } catch (error) {
      console.error('Error:', error);
      setResponse('Désolé, une erreur est survenue. Veuillez réessayer.');
    } finally {
      setIsLoading(false);
    }
  };

  const deleteConsultation = async (id: number) => {
    try {
      const res = await fetch(`/api/agri-assistant/${id}`, {
        method: 'DELETE',
      });
      
      if (res.ok) {
        setHistory(prev => prev.filter(c => c.id !== id));
      }
    } catch (error) {
      console.error('Error deleting consultation:', error);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="text-center">
        <div className="flex justify-center mb-4">
          <SparklesIcon className="h-12 w-12 text-green-600" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Assistant Agricole IA
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Obtenez des conseils personnalisés pour vos projets agricoles, d'élevage et de jardinage
          grâce à notre assistant intelligent spécialisé.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Consultation Form */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow-md p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Category Selection */}
              <div>
                <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-2">
                  Catégorie (optionnel)
                </label>
                <select
                  id="category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                >
                  <option value="">Sélectionnez une catégorie...</option>
                  {categories.map((cat) => (
                    <option key={cat.value} value={cat.value}>
                      {cat.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Question Input */}
              <div>
                <label htmlFor="question" className="block text-sm font-medium text-gray-700 mb-2">
                  Votre question agricole
                </label>
                <textarea
                  id="question"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Décrivez votre situation ou posez votre question agricole..."
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  required
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={isLoading || !question.trim()}
                className="w-full bg-green-600 text-white py-3 px-4 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Consultation en cours...
                  </>
                ) : (
                  <>
                    <ChatBubbleLeftRightIcon className="h-5 w-5" />
                    Consulter l'assistant
                  </>
                )}
              </button>
            </form>

            {/* Response Display */}
            {response && (
              <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-md">
                <h3 className="text-lg font-medium text-green-800 mb-2 flex items-center gap-2">
                  <SparklesIcon className="h-5 w-5" />
                  Conseil de l'assistant
                </h3>
                <div className="text-green-700 whitespace-pre-wrap">{response}</div>
              </div>
            )}
          </div>
        </div>

        {/* Consultation History */}
        <div className="lg:col-span-1">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <ClockIcon className="h-5 w-5" />
              Historique des consultations
            </h2>
            
            {history.length === 0 ? (
              <p className="text-gray-500 text-center py-8">
                Aucune consultation pour le moment
              </p>
            ) : (
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {history.map((consultation) => (
                  <div
                    key={consultation.id}
                    className="border border-gray-200 rounded-lg p-3 hover:bg-gray-50"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <div className="text-xs text-gray-500">
                        {formatDate(consultation.created_at)}
                      </div>
                      <button
                        onClick={() => deleteConsultation(consultation.id)}
                        className="text-red-400 hover:text-red-600"
                        title="Supprimer"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </div>
                    
                    {consultation.category && (
                      <div className="inline-block px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full mb-2">
                        {categories.find(c => c.value === consultation.category)?.label || consultation.category}
                      </div>
                    )}
                    
                    <div className="text-sm font-medium text-gray-900 mb-1">
                      {consultation.question.length > 100
                        ? `${consultation.question.substring(0, 100)}...`
                        : consultation.question
                      }
                    </div>
                    
                    <div className="text-xs text-gray-600">
                      {consultation.response.length > 150
                        ? `${consultation.response.substring(0, 150)}...`
                        : consultation.response
                      }
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Info Section */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-medium text-blue-800 mb-2">
          Comment utiliser l'assistant agricole ?
        </h3>
        <ul className="text-blue-700 space-y-1 text-sm">
          <li>• Posez des questions spécifiques sur vos cultures, votre élevage ou votre jardin</li>
          <li>• Sélectionnez une catégorie pour des conseils plus précis</li>
          <li>• L'assistant est spécialisé dans l'agriculture française et européenne</li>
          <li>• Vos consultations sont sauvegardées dans votre historique</li>
          <li>• Les conseils sont donnés à titre informatif, consultez un expert pour des décisions importantes</li>
        </ul>
      </div>
    </div>
  );
}