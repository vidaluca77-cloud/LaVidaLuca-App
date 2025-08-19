'use client';

import React, { useState } from 'react';
import { AuthForms } from '@/components/AuthForms';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';

export default function AuthPage() {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  if (isAuthenticated) {
    router.push('/dashboard');
    return null;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {mode === 'login' ? 'Bienvenue' : 'Rejoignez-nous'}
          </h1>
          <p className="text-gray-600">
            {mode === 'login' 
              ? 'Connectez-vous à votre compte La Vida Luca' 
              : 'Créez votre compte pour commencer votre aventure'}
          </p>
        </div>
        <AuthForms
          mode={mode}
          onModeChange={setMode}
          onSuccess={() => router.push('/dashboard')}
        />
      </div>
    </div>
  );
}