// src/components/features/auth/LoginForm.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button, Input, Card } from '@/components/ui';
import { supabase } from '@/lib/supabase';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const { error } = await supabase.auth.signInWithPassword({
        email,
        password,
      });

      if (error) {
        setError(error.message);
      } else {
        router.push('/dashboard');
      }
    } catch (err) {
      setError('Une erreur inattendue s\'est produite');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Connexion</h1>
          <p className="text-gray-600 mt-2">Accédez à votre espace La Vida Luca</p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <Input
          label="Email"
          type="email"
          value={email}
          onChange={setEmail}
          required
          placeholder="votre@email.com"
        />

        <Input
          label="Mot de passe"
          type="password"
          value={password}
          onChange={setPassword}
          required
          placeholder="Votre mot de passe"
        />

        <Button
          type="submit"
          className="w-full"
          loading={loading}
          disabled={!email || !password}
        >
          Se connecter
        </Button>

        <div className="text-center text-sm text-gray-600">
          Pas encore de compte ?{' '}
          <a href="/auth/register" className="text-vida-green hover:underline">
            S'inscrire
          </a>
        </div>
      </form>
    </Card>
  );
}