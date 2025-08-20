"use client";
import { useState } from "react";
import { useConnectionStatus } from "@/hooks/useConnectionStatus";
import { offlineQueue } from "@/lib/offline-queue";

export default function Contact() {
  const [ok, setOk] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { isOnline } = useConnectionStatus();
  
  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setIsSubmitting(true);
    
    const data = Object.fromEntries(new FormData(e.currentTarget) as any);
    
    try {
      if (isOnline) {
        // Try direct submission when online
        const response = await fetch("/api/contact", { 
          method: "POST", 
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data) 
        });
        
        if (response.ok) {
          setOk(true);
        } else {
          throw new Error('Server error');
        }
      } else {
        // Queue for offline submission
        await offlineQueue.enqueue('CONTACT_FORM_SUBMIT', data, {
          priority: 'high',
          metadata: { 
            form: 'contact',
            timestamp: new Date().toISOString() 
          }
        });
        setOk(true);
      }
    } catch (error) {
      // Fallback to queue if direct submission fails
      await offlineQueue.enqueue('CONTACT_FORM_SUBMIT', data, {
        priority: 'high',
        metadata: { 
          form: 'contact',
          timestamp: new Date().toISOString(),
          fallback: true
        }
      });
      setOk(true);
    } finally {
      setIsSubmitting(false);
    }
  }
  
  return (
    <div className="max-w-xl">
      <h1 className="text-3xl font-bold mb-4">Contact</h1>
      
      {!isOnline && (
        <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
          <p className="text-sm text-yellow-700">
            📱 Mode hors ligne activé. Votre message sera envoyé automatiquement lors de la reconnexion.
          </p>
        </div>
      )}
      
      {ok ? (
        <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
          <p className="text-green-800 font-medium">
            ✅ Merci ! {isOnline ? 'Votre message a été envoyé.' : 'Votre message sera envoyé dès la reconnexion.'}
          </p>
          <button 
            onClick={() => setOk(false)}
            className="mt-2 text-sm text-green-600 hover:text-green-800 underline"
          >
            Envoyer un autre message
          </button>
        </div>
      ) : (
        <form onSubmit={onSubmit} className="space-y-3">
          <input 
            name="name" 
            placeholder="Nom" 
            className="w-full border px-3 py-2 rounded focus:ring-2 focus:ring-green-500 focus:border-green-500" 
            required 
            disabled={isSubmitting}
          />
          <input 
            name="email" 
            type="email" 
            placeholder="Email" 
            className="w-full border px-3 py-2 rounded focus:ring-2 focus:ring-green-500 focus:border-green-500" 
            required 
            disabled={isSubmitting}
          />
          <textarea 
            name="message" 
            placeholder="Ton message" 
            className="w-full border px-3 py-2 rounded h-28 focus:ring-2 focus:ring-green-500 focus:border-green-500" 
            required 
            disabled={isSubmitting}
          />
          <button 
            type="submit"
            disabled={isSubmitting}
            className="border border-green-600 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {isSubmitting ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Envoi en cours...
              </>
            ) : (
              `Envoyer${!isOnline ? ' (Hors ligne)' : ''}`
            )}
          </button>
        </form>
      )}
    </div>
  );
}
