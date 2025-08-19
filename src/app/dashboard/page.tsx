'use client';

import React from 'react';
import { Dashboard } from '@/components/Dashboard';
import { useAuth } from '@/contexts/AuthContext';
import { AuthForms } from '@/components/AuthForms';

export default function DashboardPage() {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Accès Dashboard</h1>
            <p className="text-gray-600">Connectez-vous pour accéder à votre tableau de bord</p>
          </div>
          <AuthForms
            mode="login"
            onModeChange={() => {}}
            onSuccess={() => window.location.reload()}
          />
        </div>
      </div>
    );
  }

  return (
    <div>
      <Dashboard userProfile={user?.profile} />
    </div>
  );
}