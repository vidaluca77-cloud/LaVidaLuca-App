"use client";

import { useState, useRef, useEffect } from 'react';
import { PaperAirplaneIcon, ChatBubbleLeftRightIcon, ClockIcon, HeartIcon } from '@heroicons/react/24/outline';
import { HeartIcon as HeartSolidIcon } from '@heroicons/react/24/solid';

interface Consultation {
  id: string;
  question: string;
  answer: string;
  created_at: string;
  is_helpful?: boolean;
  user_rating?: string;
}

interface ConsultationResponse {
  answer: string;
  confidence?: string;
  sources?: string[];
  consultation_id?: string;
}

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  consultation_id?: string;
}

export default function AgriAssistant() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: `Bonjour ! 👋 Je suis votre assistant agricole intelligent.

Je peux vous aider avec :
• **Problèmes de sol** et nutrition des plantes
• **Maladies et ravageurs** - solutions écologiques
• **Techniques de jardinage** et permaculture
• **Irrigation** et gestion de l'eau
• **Conseils de plantation** selon la saison
• **Agriculture durable** et pratiques bio

Posez-moi votre question agricole !`,
      timestamp: new Date(),
    }
  ]);

  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState<Consultation[]>([]);
  const [showHistory, setShowHistory] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load consultation history on component mount
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await fetch('/api/agricultural-assistant/history');
      if (response.ok) {
        const data = await response.json();
        setHistory(data.consultations || []);
      }
    } catch (error) {
      console.error('Error loading history:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/agricultural-assistant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: inputValue,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data: ConsultationResponse = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: data.answer,
        timestamp: new Date(),
        consultation_id: data.consultation_id,
      };

      setMessages(prev => [...prev, assistantMessage]);
      await loadHistory(); // Refresh history

    } catch (error) {
      console.error('Error getting response:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'Désolé, une erreur est survenue. Veuillez réessayer.',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = async (consultationId: string, isHelpful: boolean) => {
    try {
      await fetch(`/api/agricultural-assistant/feedback/${consultationId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          is_helpful: isHelpful,
        }),
      });
      
      // Update local state
      setHistory(prev => prev.map(consultation => 
        consultation.id === consultationId 
          ? { ...consultation, is_helpful: isHelpful }
          : consultation
      ));
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  const formatTime = (date: Date | string) => {
    const d = typeof date === 'string' ? new Date(date) : date;
    return d.toLocaleTimeString('fr-FR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="flex flex-col lg:flex-row h-screen max-h-[800px] bg-gray-50 rounded-lg overflow-hidden">
      {/* History Sidebar */}
      <div className={`${showHistory ? 'block' : 'hidden'} lg:block lg:w-80 bg-white border-r border-gray-200 flex flex-col`}>
        <div className="p-4 border-b border-gray-200">
          <h3 className="font-semibold text-gray-900 flex items-center">
            <ClockIcon className="w-5 h-5 mr-2" />
            Historique des consultations
          </h3>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-3">
          {history.length === 0 ? (
            <p className="text-gray-500 text-sm text-center">
              Aucune consultation précédente
            </p>
          ) : (
            history.map((consultation) => (
              <div
                key={consultation.id}
                className="bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors"
              >
                <p className="text-sm text-gray-900 font-medium mb-1 line-clamp-2">
                  {consultation.question}
                </p>
                <div className="flex items-center justify-between text-xs text-gray-500">
                  <span>{formatDate(consultation.created_at)}</span>
                  {consultation.is_helpful !== undefined && (
                    <HeartSolidIcon 
                      className={`w-4 h-4 ${consultation.is_helpful ? 'text-red-500' : 'text-gray-300'}`} 
                    />
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-green-600 text-white p-4 flex items-center justify-between">
          <div className="flex items-center">
            <ChatBubbleLeftRightIcon className="w-6 h-6 mr-3" />
            <div>
              <h2 className="font-semibold">Assistant Agricole IA</h2>
              <p className="text-sm text-green-100">Conseils personnalisés pour votre agriculture</p>
            </div>
          </div>
          
          <button
            onClick={() => setShowHistory(!showHistory)}
            className="lg:hidden p-2 hover:bg-green-700 rounded-lg transition-colors"
          >
            <ClockIcon className="w-5 h-5" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  message.type === 'user'
                    ? 'bg-green-600 text-white'
                    : 'bg-white text-gray-900 shadow-sm border border-gray-200'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                
                <div className="flex items-center justify-between mt-2">
                  <span className={`text-xs ${
                    message.type === 'user' ? 'text-green-100' : 'text-gray-500'
                  }`}>
                    {formatTime(message.timestamp)}
                  </span>
                  
                  {message.type === 'assistant' && message.consultation_id && (
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => handleFeedback(message.consultation_id!, true)}
                        className="text-gray-400 hover:text-red-500 transition-colors"
                        title="Utile"
                      >
                        <HeartIcon className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleFeedback(message.consultation_id!, false)}
                        className="text-gray-400 hover:text-gray-600 transition-colors"
                        title="Pas utile"
                      >
                        <HeartIcon className="w-4 h-4 rotate-180" />
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-white text-gray-900 shadow-sm border border-gray-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <span className="text-sm text-gray-500 ml-2">L'assistant réfléchit...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input Form */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Posez votre question agricole..."
              className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent"
              disabled={isLoading}
            />
            <button
              type="submit"
              disabled={isLoading || !inputValue.trim()}
              className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
            >
              <PaperAirplaneIcon className="w-5 h-5" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}