import React, { useState } from 'react';
import { useAuth, useNotification } from '@/context';
import { Card, CardHeader, CardContent, CardFooter, Button, Input, LoadingOverlay } from '@/components/ui';
import { LoginFormData, loginSchema } from '@/utils/validation';
import { EyeIcon, EyeSlashIcon, UserIcon } from '@heroicons/react/24/outline';

interface LoginFormProps {
  onSuccess?: () => void;
  onSwitchToRegister?: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({
  onSuccess,
  onSwitchToRegister,
}) => {
  const { login, isLoading } = useAuth();
  const { showError } = useNotification();
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: '',
  });
  const [errors, setErrors] = useState<Partial<LoginFormData>>({});
  const [showPassword, setShowPassword] = useState(false);

  const handleInputChange = (field: keyof LoginFormData, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value,
    }));
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({
        ...prev,
        [field]: undefined,
      }));
    }
  };

  const validateForm = (): boolean => {
    try {
      loginSchema.parse(formData);
      setErrors({});
      return true;
    } catch (error: any) {
      const fieldErrors: Partial<LoginFormData> = {};
      error.errors?.forEach((err: any) => {
        const field = err.path[0] as keyof LoginFormData;
        fieldErrors[field] = err.message;
      });
      setErrors(fieldErrors);
      return false;
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    const success = await login(formData.email, formData.password);
    
    if (success) {
      if (onSuccess) {
        onSuccess();
      }
    } else {
      showError('Email ou mot de passe incorrect');
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <LoadingOverlay isLoading={isLoading}>
        <CardHeader>
          <div className="text-center">
            <div className="bg-primary-100 p-3 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <UserIcon className="h-8 w-8 text-primary-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Connexion</h2>
            <p className="text-gray-600 mt-2">
              Connectez-vous à votre compte La Vida Luca
            </p>
          </div>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <Input
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => handleInputChange('email', e.target.value)}
              error={errors.email}
              placeholder="votre.email@exemple.com"
              required
            />

            <div className="relative">
              <Input
                label="Mot de passe"
                type={showPassword ? 'text' : 'password'}
                value={formData.password}
                onChange={(e) => handleInputChange('password', e.target.value)}
                error={errors.password}
                placeholder="Votre mot de passe"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-8 text-gray-400 hover:text-gray-600"
              >
                {showPassword ? (
                  <EyeSlashIcon className="h-5 w-5" />
                ) : (
                  <EyeIcon className="h-5 w-5" />
                )}
              </button>
            </div>
          </CardContent>

          <CardFooter className="space-y-4">
            <Button
              type="submit"
              className="w-full"
              disabled={isLoading}
              isLoading={isLoading}
            >
              Se connecter
            </Button>

            {onSwitchToRegister && (
              <div className="text-center">
                <p className="text-sm text-gray-600">
                  Pas encore de compte ?{' '}
                  <button
                    type="button"
                    onClick={onSwitchToRegister}
                    className="text-primary-600 hover:text-primary-500 font-medium"
                  >
                    Créer un compte
                  </button>
                </p>
              </div>
            )}
          </CardFooter>
        </form>
      </LoadingOverlay>
    </Card>
  );
};