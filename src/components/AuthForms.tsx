'use client';

import React, { useState } from 'react';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';
import { Card, CardContent, CardHeader, CardTitle, Button, Input } from '@/components/ui';
import { LoginCredentials, RegisterData } from '@/types';
import { useAuth } from '@/contexts/AuthContext';

interface AuthFormsProps {
  mode: 'login' | 'register';
  onModeChange: (mode: 'login' | 'register') => void;
  onSuccess?: () => void;
}

interface FormErrors {
  [key: string]: string;
}

export function AuthForms({ mode, onModeChange, onSuccess }: AuthFormsProps) {
  const { login, register, error: authError, isLoading, clearError } = useAuth();
  
  const [loginData, setLoginData] = useState<LoginCredentials>({
    email: '',
    password: ''
  });
  
  const [registerData, setRegisterData] = useState<RegisterData>({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  
  const [errors, setErrors] = useState<FormErrors>({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const validateEmail = (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePassword = (password: string): boolean => {
    return password.length >= 8;
  };

  const validateLoginForm = (): boolean => {
    const newErrors: FormErrors = {};
    
    if (!loginData.email) {
      newErrors.email = 'L\'email est requis';
    } else if (!validateEmail(loginData.email)) {
      newErrors.email = 'Format d\'email invalide';
    }
    
    if (!loginData.password) {
      newErrors.password = 'Le mot de passe est requis';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateRegisterForm = (): boolean => {
    const newErrors: FormErrors = {};
    
    if (!registerData.name.trim()) {
      newErrors.name = 'Le nom est requis';
    } else if (registerData.name.trim().length < 2) {
      newErrors.name = 'Le nom doit contenir au moins 2 caractères';
    }
    
    if (!registerData.email) {
      newErrors.email = 'L\'email est requis';
    } else if (!validateEmail(registerData.email)) {
      newErrors.email = 'Format d\'email invalide';
    }
    
    if (!registerData.password) {
      newErrors.password = 'Le mot de passe est requis';
    } else if (!validatePassword(registerData.password)) {
      newErrors.password = 'Le mot de passe doit contenir au moins 8 caractères';
    }
    
    if (!registerData.confirmPassword) {
      newErrors.confirmPassword = 'Confirmez votre mot de passe';
    } else if (registerData.password !== registerData.confirmPassword) {
      newErrors.confirmPassword = 'Les mots de passe ne correspondent pas';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    
    if (!validateLoginForm()) return;
    
    try {
      await login(loginData);
      onSuccess?.();
    } catch (err) {
      // Error is handled by the AuthContext
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    
    if (!validateRegisterForm()) return;
    
    try {
      await register(registerData);
      onSuccess?.();
    } catch (err) {
      // Error is handled by the AuthContext
    }
  };

  const handleModeChange = (newMode: 'login' | 'register') => {
    clearError();
    setErrors({});
    onModeChange(newMode);
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle className="text-center">
          {mode === 'login' ? 'Connexion' : 'Inscription'}
        </CardTitle>
      </CardHeader>
      <CardContent>
        {mode === 'login' ? (
          <form onSubmit={handleLogin} className="space-y-4">
            <Input
              type="email"
              label="Email"
              value={loginData.email}
              onChange={(e) => setLoginData(prev => ({ ...prev, email: e.target.value }))}
              error={errors.email}
              placeholder="votre@email.com"
              required
            />
            
            <div className="relative">
              <Input
                type={showPassword ? 'text' : 'password'}
                label="Mot de passe"
                value={loginData.password}
                onChange={(e) => setLoginData(prev => ({ ...prev, password: e.target.value }))}
                error={errors.password}
                placeholder="••••••••"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-8 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? (
                  <EyeSlashIcon className="w-5 h-5" />
                ) : (
                  <EyeIcon className="w-5 h-5" />
                )}
              </button>
            </div>
            
            {authError && (
              <div className="bg-red-50 border border-red-200 p-3 rounded-lg">
                <p className="text-sm text-red-700">{authError}</p>
              </div>
            )}
            
            <Button
              type="submit"
              loading={isLoading}
              className="w-full"
            >
              Se connecter
            </Button>
          </form>
        ) : (
          <form onSubmit={handleRegister} className="space-y-4">
            <Input
              type="text"
              label="Nom complet"
              value={registerData.name}
              onChange={(e) => setRegisterData(prev => ({ ...prev, name: e.target.value }))}
              error={errors.name}
              placeholder="Jean Dupont"
              required
            />
            
            <Input
              type="email"
              label="Email"
              value={registerData.email}
              onChange={(e) => setRegisterData(prev => ({ ...prev, email: e.target.value }))}
              error={errors.email}
              placeholder="votre@email.com"
              required
            />
            
            <div className="relative">
              <Input
                type={showPassword ? 'text' : 'password'}
                label="Mot de passe"
                value={registerData.password}
                onChange={(e) => setRegisterData(prev => ({ ...prev, password: e.target.value }))}
                error={errors.password}
                placeholder="••••••••"
                helperText="Au moins 8 caractères"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-8 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? (
                  <EyeSlashIcon className="w-5 h-5" />
                ) : (
                  <EyeIcon className="w-5 h-5" />
                )}
              </button>
            </div>
            
            <div className="relative">
              <Input
                type={showConfirmPassword ? 'text' : 'password'}
                label="Confirmer le mot de passe"
                value={registerData.confirmPassword}
                onChange={(e) => setRegisterData(prev => ({ ...prev, confirmPassword: e.target.value }))}
                error={errors.confirmPassword}
                placeholder="••••••••"
                required
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-8 text-gray-400 hover:text-gray-600"
              >
                {showConfirmPassword ? (
                  <EyeSlashIcon className="w-5 h-5" />
                ) : (
                  <EyeIcon className="w-5 h-5" />
                )}
              </button>
            </div>
            
            {authError && (
              <div className="bg-red-50 border border-red-200 p-3 rounded-lg">
                <p className="text-sm text-red-700">{authError}</p>
              </div>
            )}
            
            <Button
              type="submit"
              loading={isLoading}
              className="w-full"
            >
              S'inscrire
            </Button>
          </form>
        )}
        
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            {mode === 'login' ? (
              <>
                Pas encore de compte ?{' '}
                <button
                  onClick={() => handleModeChange('register')}
                  className="text-vida-500 hover:text-vida-600 font-medium"
                >
                  S'inscrire
                </button>
              </>
            ) : (
              <>
                Déjà un compte ?{' '}
                <button
                  onClick={() => handleModeChange('login')}
                  className="text-vida-500 hover:text-vida-600 font-medium"
                >
                  Se connecter
                </button>
              </>
            )}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}