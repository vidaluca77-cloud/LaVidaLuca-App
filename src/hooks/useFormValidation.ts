import { useState, useCallback } from 'react';

export interface ValidationRule {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  custom?: (value: any) => string | undefined;
}

export interface ValidationSchema {
  [key: string]: ValidationRule;
}

export interface FormErrors {
  [key: string]: string;
}

export function useFormValidation<T extends Record<string, any>>(
  initialValues: T,
  validationSchema: ValidationSchema
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<FormErrors>({});
  const [touched, setTouchedState] = useState<Record<string, boolean>>({});

  const validateField = useCallback((name: string, value: any): string | undefined => {
    const rule = validationSchema[name];
    if (!rule) return undefined;

    // Required validation
    if (rule.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
      return 'Ce champ est requis';
    }

    // Skip other validations if field is empty and not required
    if (!value && !rule.required) return undefined;

    // Min length validation
    if (rule.minLength && typeof value === 'string' && value.length < rule.minLength) {
      return `Ce champ doit contenir au moins ${rule.minLength} caractères`;
    }

    // Max length validation
    if (rule.maxLength && typeof value === 'string' && value.length > rule.maxLength) {
      return `Ce champ ne peut pas dépasser ${rule.maxLength} caractères`;
    }

    // Pattern validation
    if (rule.pattern && typeof value === 'string' && !rule.pattern.test(value)) {
      return 'Format invalide';
    }

    // Custom validation
    if (rule.custom) {
      return rule.custom(value);
    }

    return undefined;
  }, [validationSchema]);

  const validateForm = useCallback((): boolean => {
    const newErrors: FormErrors = {};
    let isValid = true;

    Object.keys(validationSchema).forEach(fieldName => {
      const error = validateField(fieldName, values[fieldName]);
      if (error) {
        newErrors[fieldName] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  }, [values, validateField, validationSchema]);

  const setValue = useCallback((name: string, value: any) => {
    setValues(prev => ({ ...prev, [name]: value }));
    
    // Validate field if it has been touched
    if (touched[name]) {
      const error = validateField(name, value);
      setErrors(prev => ({
        ...prev,
        [name]: error || ''
      }));
    }
  }, [touched, validateField]);

  const setTouched = useCallback((name: string, isTouched: boolean = true) => {
    setTouchedState(prev => ({ ...prev, [name]: isTouched }));
    
    if (isTouched) {
      const error = validateField(name, values[name]);
      setErrors(prev => ({
        ...prev,
        [name]: error || ''
      }));
    }
  }, [values, validateField]);

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouchedState({});
  }, [initialValues]);

  const handleChange = useCallback((name: string) => (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    setValue(name, e.target.value);
  }, [setValue]);

  const handleBlur = useCallback((name: string) => () => {
    setTouched(name, true);
  }, [setTouched]);

  return {
    values,
    errors,
    touched,
    setValue,
    setTouched,
    validateForm,
    reset,
    handleChange,
    handleBlur,
    isValid: Object.keys(errors).length === 0 && Object.keys(touched).length > 0
  };
}

// Common validation patterns
export const validationPatterns = {
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  phone: /^(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}$/,
  postalCode: /^\d{5}$/
};

// Common validation rules
export const commonRules = {
  required: { required: true },
  email: { 
    required: true, 
    pattern: validationPatterns.email,
    custom: (value: string) => {
      if (value && !validationPatterns.email.test(value)) {
        return 'Adresse email invalide';
      }
    }
  },
  password: { 
    required: true, 
    minLength: 8,
    custom: (value: string) => {
      if (value && value.length < 8) {
        return 'Le mot de passe doit contenir au moins 8 caractères';
      }
    }
  },
  phone: {
    pattern: validationPatterns.phone,
    custom: (value: string) => {
      if (value && !validationPatterns.phone.test(value)) {
        return 'Numéro de téléphone invalide';
      }
    }
  }
};