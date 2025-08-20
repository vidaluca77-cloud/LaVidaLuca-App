"use client"

import { useState, useRef, useEffect } from 'react'
import { PaperAirplaneIcon, SparklesIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline'

import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Assistant Agricole | La Vida Luca',
  description: 'Votre expert en agriculture durable, permaculture et techniques écologiques. Posez vos questions et obtenez des conseils personnalisés !',
  keywords: ['agriculture', 'permaculture', 'jardinage', 'écologie', 'durable', 'conseils agricoles'],
}

interface Message {
  id: string
  type: 'user' | 'assistant'
  content: string
  timestamp: Date
  category?: string
  tags?: string[]
}

interface Category {
  id: string
  name: string
  description: string
  icon: string
}

export default function AssistantAgricolePage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [categories, setCategories] = useState<Category[]>([])
  const [selectedCategory, setSelectedCategory] = useState<string>('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  // Scroll to bottom when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load categories on component mount
  useEffect(() => {
    const loadCategories = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/consultations/categories')
        if (response.ok) {
          const data = await response.json()
          setCategories(data.categories)
        }
      } catch (error) {
        console.error('Error loading categories:', error)
      }
    }
    loadCategories()
  }, [])

  // Add welcome message on first load
  useEffect(() => {
    if (messages.length === 0) {
      const welcomeMessage: Message = {
        id: 'welcome',
        type: 'assistant',
        content: `🌾 **Bienvenue dans l'Assistant Agricole La Vida Luca !**

Je suis votre expert en agriculture durable et permaculture. Je peux vous aider avec :

🌱 **Gestion des sols** - Fertilité, compostage, analyses
🍅 **Cultures** - Rotation, associations, calendrier
🐛 **Biocontrôle** - Lutte naturelle contre les ravageurs
🌿 **Permaculture** - Design écologique, autonomie
🐄 **Élevage** - Bien-être animal, médecines naturelles
💧 **Irrigation** - Économie d'eau, techniques adaptées
🌡️ **Climat** - Adaptation, variétés résistantes

**Posez-moi votre première question pour commencer !**`,
        timestamp: new Date()
      }
      setMessages([welcomeMessage])
    }
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/v1/consultations/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: inputValue,
          context: selectedCategory ? `Catégorie sélectionnée: ${selectedCategory}` : undefined
        })
      })

      if (response.ok) {
        const data = await response.json()
        const assistantMessage: Message = {
          id: Date.now().toString() + '_assistant',
          type: 'assistant',
          content: data.answer,
          timestamp: new Date(),
          category: data.category,
          tags: data.tags
        }
        setMessages(prev => [...prev, assistantMessage])
      } else {
        throw new Error('Failed to get response')
      }
    } catch (error) {
      console.error('Error:', error)
      const errorMessage: Message = {
        id: Date.now().toString() + '_error',
        type: 'assistant',
        content: "Désolé, une erreur s'est produite. Veuillez réessayer.",
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleCategorySelect = (categoryId: string) => {
    setSelectedCategory(categoryId === selectedCategory ? '' : categoryId)
  }

  const clearHistory = () => {
    setMessages([])
    setSelectedCategory('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <SparklesIcon className="h-8 w-8 text-green-600" />
            <h1 className="text-3xl font-bold text-gray-900">Assistant Agricole</h1>
            <ChatBubbleLeftRightIcon className="h-8 w-8 text-green-600" />
          </div>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Votre expert en agriculture durable, permaculture et techniques écologiques.
            Posez vos questions et obtenez des conseils personnalisés !
          </p>
        </div>

        {/* Categories */}
        {categories.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-3">Catégories disponibles :</h3>
            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => handleCategorySelect(category.id)}
                  className={`px-3 py-2 rounded-full text-sm font-medium transition-colors ${
                    selectedCategory === category.id
                      ? 'bg-green-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-green-100 border border-gray-200'
                  }`}
                  title={category.description}
                >
                  {category.icon} {category.name}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Chat Interface */}
        <div className="max-w-4xl mx-auto">
          {/* Messages */}
          <div className="bg-white rounded-lg shadow-lg mb-4">
            <div className="h-96 overflow-y-auto p-6 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-4 ${
                      message.type === 'user'
                        ? 'bg-green-600 text-white'
                        : 'bg-gray-100 text-gray-900'
                    }`}
                  >
                    <div className="whitespace-pre-wrap text-sm leading-relaxed">
                      {message.content}
                    </div>
                    {message.tags && message.tags.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {message.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 text-xs bg-green-200 text-green-800 rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                    <div className="text-xs opacity-70 mt-2">
                      {message.timestamp.toLocaleTimeString('fr-FR', {
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </div>
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-gray-100 rounded-lg p-4 max-w-[80%]">
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-green-600"></div>
                      <span className="text-sm text-gray-600">L'assistant réfléchit...</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-4">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Posez votre question agricole..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                <PaperAirplaneIcon className="h-5 w-5" />
                Envoyer
              </button>
            </div>
            
            {/* Actions */}
            <div className="flex justify-between items-center mt-3 pt-3 border-t border-gray-200">
              <div className="text-xs text-gray-500">
                {selectedCategory && (
                  <span>Catégorie sélectionnée: {categories.find(c => c.id === selectedCategory)?.name}</span>
                )}
              </div>
              <button
                type="button"
                onClick={clearHistory}
                className="text-xs text-gray-500 hover:text-gray-700 transition-colors"
              >
                Effacer l'historique
              </button>
            </div>
          </form>

          {/* Examples */}
          <div className="mt-6 bg-white rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-3">Exemples de questions :</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {[
                "Comment améliorer un sol argileux compact ?",
                "Quelles associations de légumes dans mon potager ?",
                "Comment lutter contre les pucerons naturellement ?",
                "Quelle rotation pour mes parcelles céréalières ?",
                "Comment débuter en permaculture ?",
                "Mes poules perdent leurs plumes, que faire ?"
              ].map((example, index) => (
                <button
                  key={index}
                  onClick={() => setInputValue(example)}
                  className="text-left p-3 border border-gray-200 rounded-lg hover:bg-green-50 hover:border-green-300 transition-colors text-sm"
                >
                  "{example}"
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}