// src/components/ui/Input.tsx
import { ForwardedRef, forwardRef } from 'react';

interface InputProps {
  label?: string;
  placeholder?: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel';
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
  required?: boolean;
  disabled?: boolean;
  error?: string;
  className?: string;
  name?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  function Input({
    label,
    placeholder,
    type = 'text',
    value,
    defaultValue,
    onChange,
    required = false,
    disabled = false,
    error,
    className = '',
    name,
  }, ref: ForwardedRef<HTMLInputElement>) {
    return (
      <div className={`space-y-1 ${className}`}>
        {label && (
          <label className="block text-sm font-medium text-gray-700">
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <input
          ref={ref}
          type={type}
          name={name}
          placeholder={placeholder}
          value={value}
          defaultValue={defaultValue}
          onChange={(e) => onChange?.(e.target.value)}
          required={required}
          disabled={disabled}
          className={`
            w-full px-3 py-2 border rounded-lg shadow-sm placeholder-gray-400
            focus:outline-none focus:ring-2 focus:ring-vida-green focus:border-transparent
            disabled:bg-gray-50 disabled:cursor-not-allowed
            ${error ? 'border-red-300 focus:ring-red-500' : 'border-gray-300'}
          `}
        />
        {error && (
          <p className="text-sm text-red-600">{error}</p>
        )}
      </div>
    );
  }
);