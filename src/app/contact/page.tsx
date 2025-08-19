"use client";
import { useState } from "react";
import { Button, Input, Card } from '@/components/ui';

export default function Contact() {
  const [ok, setOk] = useState(false);
  
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const data = {
      name: formData.get('name'),
      email: formData.get('email'), 
      message: formData.get('message')
    };
    
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (response.ok) {
        setOk(true);
      }
    } catch (error) {
      console.error('Erreur:', error);
    }
  }

  return (
    <div className="max-w-xl mx-auto">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Contact</h1>
        <p className="text-gray-600">
          Une question ? Une suggestion ? N'hésitez pas à nous contacter !
        </p>
      </div>
      
      {ok ? (
        <Card className="text-center">
          <div className="py-8">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Message envoyé !</h3>
            <p className="text-gray-600">Merci pour votre message. On vous répond très vite !</p>
          </div>
        </Card>
      ) : (
        <Card>
          <form onSubmit={onSubmit} className="space-y-6">
            <Input 
              name="name" 
              label="Nom complet"
              placeholder="Votre nom" 
              required 
            />
            <Input 
              name="email" 
              type="email" 
              label="Email"
              placeholder="votre@email.com" 
              required 
            />
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Message <span className="text-red-500">*</span>
              </label>
              <textarea 
                name="message" 
                placeholder="Votre message..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-vida-green focus:border-transparent"
                rows={6}
                required 
              />
            </div>
            <Button type="submit" className="w-full">
              Envoyer le message
            </Button>
          </form>
        </Card>
      )}
    </div>
  );
}
