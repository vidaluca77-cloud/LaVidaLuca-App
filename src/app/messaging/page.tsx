// src/app/messaging/page.tsx
'use client';

import { useState } from 'react';
import { Card, CardHeader, CardTitle, Button, Input } from '@/components/ui';
import { 
  EnvelopeIcon, 
  PaperAirplaneIcon,
  UserIcon,
  MagnifyingGlassIcon 
} from '@heroicons/react/24/outline';

const messages = [
  {
    id: '1',
    sender: 'Marie Dupont',
    subject: 'Préparation activité maraîchage',
    preview: 'Bonjour, voici les éléments à prévoir pour notre séance de demain...',
    date: '2024-01-18',
    read: false,
    avatar: '/api/placeholder/40/40'
  },
  {
    id: '2',
    sender: 'Jean Martin',
    subject: 'Félicitations pour votre progression',
    preview: 'Je tenais à vous féliciter pour votre excellent travail lors de...',
    date: '2024-01-17',
    read: true,
    avatar: '/api/placeholder/40/40'
  },
  {
    id: '3',
    sender: 'Sophie Durand',
    subject: 'Invitation formation apiculture',
    preview: 'Une nouvelle formation en apiculture sera organisée le mois prochain...',
    date: '2024-01-16',
    read: true,
    avatar: '/api/placeholder/40/40'
  }
];

export default function MessagingPage() {
  const [selectedMessage, setSelectedMessage] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [newMessage, setNewMessage] = useState({ to: '', subject: '', content: '' });
  const [showCompose, setShowCompose] = useState(false);

  const selectedMessageData = messages.find(m => m.id === selectedMessage);

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Messagerie</h1>
        <Button onClick={() => setShowCompose(true)}>
          <PaperAirplaneIcon className="w-4 h-4 mr-2" />
          Nouveau message
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Messages List */}
        <div className="lg:col-span-1">
          <Card>
            <CardHeader>
              <div className="flex items-center space-x-4">
                <Input
                  placeholder="Rechercher..."
                  value={searchQuery}
                  onChange={setSearchQuery}
                  className="flex-1"
                />
                <MagnifyingGlassIcon className="w-5 h-5 text-gray-400" />
              </div>
            </CardHeader>
            
            <div className="space-y-2">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`p-4 cursor-pointer border-l-4 transition-colors ${
                    selectedMessage === message.id
                      ? 'border-vida-green bg-vida-green/5'
                      : 'border-transparent hover:bg-gray-50'
                  } ${!message.read ? 'bg-blue-50' : ''}`}
                  onClick={() => setSelectedMessage(message.id)}
                >
                  <div className="flex items-start space-x-3">
                    <div className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center">
                      <UserIcon className="w-4 h-4 text-gray-400" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className={`text-sm font-medium text-gray-900 truncate ${!message.read ? 'font-bold' : ''}`}>
                          {message.sender}
                        </p>
                        <p className="text-xs text-gray-500">{message.date}</p>
                      </div>
                      <p className={`text-sm text-gray-600 truncate ${!message.read ? 'font-semibold' : ''}`}>
                        {message.subject}
                      </p>
                      <p className="text-xs text-gray-500 truncate mt-1">
                        {message.preview}
                      </p>
                    </div>
                    {!message.read && (
                      <div className="w-2 h-2 bg-vida-green rounded-full"></div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Message Content */}
        <div className="lg:col-span-2">
          {showCompose ? (
            <Card>
              <CardHeader>
                <CardTitle>Nouveau message</CardTitle>
              </CardHeader>
              <div className="space-y-4">
                <Input
                  label="Destinataire"
                  placeholder="Nom de l'encadrant..."
                  value={newMessage.to}
                  onChange={(value) => setNewMessage(prev => ({ ...prev, to: value }))}
                />
                <Input
                  label="Sujet"
                  placeholder="Objet du message"
                  value={newMessage.subject}
                  onChange={(value) => setNewMessage(prev => ({ ...prev, subject: value }))}
                />
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Message
                  </label>
                  <textarea
                    value={newMessage.content}
                    onChange={(e) => setNewMessage(prev => ({ ...prev, content: e.target.value }))}
                    placeholder="Votre message..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-vida-green focus:border-transparent"
                    rows={8}
                  />
                </div>
                <div className="flex gap-4">
                  <Button
                    onClick={() => {
                      alert('Message envoyé !');
                      setShowCompose(false);
                      setNewMessage({ to: '', subject: '', content: '' });
                    }}
                    className="flex-1"
                  >
                    Envoyer
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => setShowCompose(false)}
                    className="flex-1"
                  >
                    Annuler
                  </Button>
                </div>
              </div>
            </Card>
          ) : selectedMessageData ? (
            <Card>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center">
                      <UserIcon className="w-5 h-5 text-gray-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{selectedMessageData.sender}</h3>
                      <p className="text-sm text-gray-500">{selectedMessageData.date}</p>
                    </div>
                  </div>
                  <Button size="sm" variant="outline">
                    Répondre
                  </Button>
                </div>
                <h2 className="text-xl font-bold text-gray-900 mt-4">{selectedMessageData.subject}</h2>
              </CardHeader>
              
              <div className="prose max-w-none">
                <p className="text-gray-700 leading-relaxed">
                  Bonjour,
                </p>
                <p className="text-gray-700 leading-relaxed">
                  J'espère que vous allez bien. Je vous écris concernant notre prochaine séance de maraîchage prévue demain à 14h00.
                </p>
                <p className="text-gray-700 leading-relaxed">
                  Voici les éléments à prévoir pour cette activité :
                </p>
                <ul className="text-gray-700">
                  <li>Gants de jardinage</li>
                  <li>Bottes ou chaussures adaptées</li>
                  <li>Vêtements que vous pouvez salir</li>
                  <li>Chapeau ou casquette (protection solaire)</li>
                </ul>
                <p className="text-gray-700 leading-relaxed">
                  Nous travaillerons sur la préparation des parcelles et les semis de légumes de saison. C'est une excellente opportunité d'apprendre les bases du maraîchage biologique.
                </p>
                <p className="text-gray-700 leading-relaxed">
                  N'hésitez pas si vous avez des questions.
                </p>
                <p className="text-gray-700 leading-relaxed">
                  À demain !<br />
                  Marie Dupont
                </p>
              </div>
            </Card>
          ) : (
            <Card className="text-center py-12">
              <EnvelopeIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">Sélectionnez un message</h3>
              <p className="text-gray-500">Choisissez un message dans la liste pour le lire.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}