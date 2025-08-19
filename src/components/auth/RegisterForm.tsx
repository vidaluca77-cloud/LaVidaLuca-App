import React, { useState } from 'react';
import { useAuth, useNotification } from '@/context';
import { Card, CardHeader, CardContent, CardFooter, Button, Input, LoadingOverlay } from '@/components/ui';
import { RegisterFormData, registerSchema } from '@/utils/validation';
import { EyeIcon, EyeSlashIcon, UserPlusIcon } from '@heroicons/react/24/outline';

interface RegisterFormProps {
  onSuccess?: () => void;
  onSwitchToLogin?: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({
  onSuccess,
  onSwitchToLogin,
}) => {
  const { register, isLoading } = useAuth();
  const { showError } = useNotification();
  const [formData, setFormData] = useState<RegisterFormData>({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [errors, setErrors] = useState<Partial<RegisterFormData>>({});
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const handleInputChange = (field: keyof RegisterFormData, value: string) => {
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
      registerSchema.parse(formData);
      setErrors({});
      return true;
    } catch (error: any) {
      const fieldErrors: Partial<RegisterFormData> = {};
      error.errors?.forEach((err: any) => {
        const field = err.path[0] as keyof RegisterFormData;
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

    const success = await register(formData.email, formData.password, formData.name);
    
    if (success) {
      if (onSuccess) {
        onSuccess();
      }
    } else {
      showError('Erreur lors de la création du compte');
    }
  };

  return (
    <Card className="w-full max-w-md mx-auto">
      <LoadingOverlay isLoading={isLoading}>
        <CardHeader>
          <div className="text-center">
            <div className="bg-primary-100 p-3 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
              <UserPlusIcon className="h-8 w-8 text-primary-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Créer un compte</h2>
            <p className="text-gray-600 mt-2">
              Rejoignez La Vida Luca et découvrez nos activités
            </p>
          </div>
        </CardHeader>

        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            <Input
              label="Nom complet"
              type="text"
              value={formData.name}
              onChange={(e) => handleInputChange('name', e.target.value)}
              error={errors.name}
              placeholder="Votre nom et prénom"
              required
            />

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
                helperText="Minimum 6 caractères"
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

            <div className="relative">
              <Input
                label="Confirmer le mot de passe"
                type={showConfirmPassword ? 'text' : 'password'}
                value={formData.confirmPassword}
                onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                error={errors.confirmPassword}
                placeholder="Confirmer votre mot de passe"
                required
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-8 text-gray-400 hover:text-gray-600"
              >
                {showConfirmPassword ? (
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
              Créer mon compte
            </Button>

            {onSwitchToLogin && (
              <div className="text-center">
                <p className="text-sm text-gray-600">
                  Déjà un compte ?{' '}
                  <button
                    type="button"
                    onClick={onSwitchToLogin}
                    className="text-primary-600 hover:text-primary-500 font-medium"
                  >
                    Se connecter
                  </button>
                </p>
              </div>
            )}

            <div className="text-center">
              <p className="text-xs text-gray-500">
                En créant un compte, vous acceptez nos conditions d'utilisation
                et notre politique de confidentialité.
              </p>
            </div>
          </CardFooter>
        </form>
      </LoadingOverlay>
    </Card>
  );
};