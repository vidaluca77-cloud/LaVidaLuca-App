'use client'

import React, { useState, useEffect } from 'react';
import { 
  ChatBubbleLeftIcon, 
  PaperAirplaneIcon, 
  ExclamationTriangleIcon,
  ClockIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';

// Types
interface Consultation {
  id: number;
  question: string;
  response: string;
  context?: Record<string, any>;
  model_used: string;
  tokens_used?: number;
  created_at: string;
}

interface ConsultationRequest {
  question: string;
  context?: Record<string, any>;
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isLoading?: boolean;
}

export default function AgriAssistantPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Bonjour ! Je suis votre assistant agricole IA. Je peux vous aider avec vos questions sur l\'agriculture, l\'élevage, la viticulture, et bien plus encore. Que puis-je faire pour vous ?',
      timestamp: new Date(),
    }
  ]);
  
  const [question, setQuestion] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [context, setContext] = useState({
    cropType: '',
    region: '',
    farmingMethod: ''
  });

  const sendMessage = async () => {
    if (!question.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: question,
      timestamp: new Date(),
    };

    const loadingMessage: Message = {
      id: (Date.now() + 1).toString(),
      type: 'assistant',
      content: '',
      timestamp: new Date(),
      isLoading: true,
    };

    setMessages(prev => [...prev, userMessage, loadingMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const requestData: ConsultationRequest = {
        question,
        context: Object.fromEntries(
          Object.entries(context).filter(([, value]) => value.trim() !== '')
        )
      };

      const response = await fetch('/api/agri-assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Erreur de communication avec le serveur');
      }

      const consultation: Consultation = await response.json();
      
      const assistantMessage: Message = {
        id: (Date.now() + 2).toString(),
        type: 'assistant',
        content: consultation.response,
        timestamp: new Date(),
      };

      setMessages(prev => prev.slice(0, -1).concat(assistantMessage));
      setQuestion('');

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Une erreur inattendue s\'est produite');
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTimestamp = (date: Date) => {
    return date.toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center space-x-3">
            <div className="bg-green-100 p-3 rounded-full">
              <SparklesIcon className="h-8 w-8 text-green-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Assistant Agricole IA</h1>
              <p className="text-gray-600">Posez vos questions sur l'agriculture et l'élevage</p>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-4">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 h-[calc(100vh-200px)] flex flex-col">
          
          {/* Context Panel */}
          <div className="border-b border-gray-200 p-4 bg-gray-50">
            <details className="group">
              <summary className="cursor-pointer text-sm font-medium text-gray-700 flex items-center">
                Contexte (optionnel)
                <span className="ml-2 transition-transform group-open:rotate-180">▼</span>
              </summary>
              <div className="mt-3 grid grid-cols-1 md:grid-cols-3 gap-3">
                <input
                  type="text"
                  placeholder="Type de culture"
                  value={context.cropType}
                  onChange={(e) => setContext(prev => ({ ...prev, cropType: e.target.value }))}
                  className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <input
                  type="text"
                  placeholder="Région"
                  value={context.region}
                  onChange={(e) => setContext(prev => ({ ...prev, region: e.target.value }))}
                  className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
                <input
                  type="text"
                  placeholder="Méthode (bio, conventionnel...)"
                  value={context.farmingMethod}
                  onChange={(e) => setContext(prev => ({ ...prev, farmingMethod: e.target.value }))}
                  className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
                />
              </div>
            </details>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-3xl ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
                  <div
                    className={`px-4 py-3 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    {message.isLoading ? (
                      <div className="flex items-center space-x-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-600"></div>
                        <span className="text-sm text-gray-600">L'assistant réfléchit...</span>
                      </div>
                    ) : (
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">
                        {message.content}
                      </div>
                    )}
                  </div>
                  <div
                    className={`mt-1 text-xs text-gray-500 ${
                      message.type === 'user' ? 'text-right' : 'text-left'
                    }`}
                  >
                    <ClockIcon className="inline w-3 h-3 mr-1" />
                    {formatTimestamp(message.timestamp)}
                  </div>
                </div>
                <div
                  className={`flex-shrink-0 ${
                    message.type === 'user' ? 'order-1 ml-3' : 'order-2 mr-3'
                  }`}
                >
                  <div
                    className={`w-8 h-8 rounded-full flex items-center justify-center ${
                      message.type === 'user'
                        ? 'bg-green-600'
                        : 'bg-gray-200'
                    }`}
                  >
                    {message.type === 'user' ? (
                      <span className="text-white font-medium text-sm">U</span>
                    ) : (
                      <SparklesIcon className="w-4 h-4 text-gray-600" />
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Error Display */}
          {error && (
            <div className="mx-4 mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
              <div className="flex items-center">
                <ExclamationTriangleIcon className="h-5 w-5 text-red-400 mr-2" />
                <span className="text-sm text-red-800">{error}</span>
              </div>
            </div>
          )}

          {/* Input */}
          <div className="border-t border-gray-200 p-4">
            <div className="flex space-x-3">
              <div className="flex-1">
                <textarea
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Posez votre question sur l'agriculture..."
                  rows={2}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md resize-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
                  disabled={isLoading}
                />
              </div>
              <button
                onClick={sendMessage}
                disabled={!question.trim() || isLoading}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200 flex items-center space-x-2"
              >
                <PaperAirplaneIcon className="h-4 w-4" />
                <span className="hidden sm:inline">Envoyer</span>
              </button>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              Appuyez sur Entrée pour envoyer, Maj+Entrée pour une nouvelle ligne
            </div>
          </div>
        </div>

        {/* Examples */}
        <div className="mt-6 bg-white rounded-lg shadow-sm border border-gray-200 p-4">
          <h3 className="font-medium text-gray-900 mb-3">Exemples de questions :</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
            <button
              onClick={() => setQuestion("Comment traiter le mildiou sur les tomates ?")}
              className="text-left p-2 rounded border border-gray-200 hover:bg-gray-50 transition-colors"
              disabled={isLoading}
            >
              "Comment traiter le mildiou sur les tomates ?"
            </button>
            <button
              onClick={() => setQuestion("Quelle rotation des cultures recommandez-vous pour un potager bio ?")}
              className="text-left p-2 rounded border border-gray-200 hover:bg-gray-50 transition-colors"
              disabled={isLoading}
            >
              "Quelle rotation des cultures recommandez-vous ?"
            </button>
            <button
              onClick={() => setQuestion("Comment améliorer la fertilité de mon sol ?")}
              className="text-left p-2 rounded border border-gray-200 hover:bg-gray-50 transition-colors"
              disabled={isLoading}
            >
              "Comment améliorer la fertilité de mon sol ?"
            </button>
            <button
              onClick={() => setQuestion("Quand planter les pommes de terre en région parisienne ?")}
              className="text-left p-2 rounded border border-gray-200 hover:bg-gray-50 transition-colors"
              disabled={isLoading}
            >
              "Quand planter les pommes de terre ?"
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}