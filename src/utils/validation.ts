import { z } from 'zod';

// Login form validation schema
export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'L\'email est requis')
    .email('Format d\'email invalide'),
  password: z
    .string()
    .min(1, 'Le mot de passe est requis')
    .min(6, 'Le mot de passe doit contenir au moins 6 caractères'),
});

// Registration form validation schema
export const registerSchema = z.object({
  name: z
    .string()
    .min(1, 'Le nom est requis')
    .min(2, 'Le nom doit contenir au moins 2 caractères'),
  email: z
    .string()
    .min(1, 'L\'email est requis')
    .email('Format d\'email invalide'),
  password: z
    .string()
    .min(1, 'Le mot de passe est requis')
    .min(6, 'Le mot de passe doit contenir au moins 6 caractères'),
  confirmPassword: z
    .string()
    .min(1, 'La confirmation du mot de passe est requise'),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Les mots de passe ne correspondent pas',
  path: ['confirmPassword'],
});

// Booking form validation schema
export const bookingSchema = z.object({
  activityId: z.string().min(1, 'L\'activité est requise'),
  date: z.string().min(1, 'La date est requise'),
  notes: z.string().optional(),
});

// Profile update validation schema
export const profileSchema = z.object({
  bio: z.string().optional(),
  phone: z.string().optional(),
  location: z.string().optional(),
  skills: z.array(z.string()).optional(),
  availability: z.array(z.string()).optional(),
  preferences: z.array(z.string()).optional(),
});

// Contact form validation schema
export const contactSchema = z.object({
  name: z
    .string()
    .min(1, 'Le nom est requis')
    .min(2, 'Le nom doit contenir au moins 2 caractères'),
  email: z
    .string()
    .min(1, 'L\'email est requis')
    .email('Format d\'email invalide'),
  subject: z
    .string()
    .min(1, 'Le sujet est requis')
    .min(5, 'Le sujet doit contenir au moins 5 caractères'),
  message: z
    .string()
    .min(1, 'Le message est requis')
    .min(10, 'Le message doit contenir au moins 10 caractères'),
});

// Type inference for TypeScript
export type LoginFormData = z.infer<typeof loginSchema>;
export type RegisterFormData = z.infer<typeof registerSchema>;
export type BookingFormData = z.infer<typeof bookingSchema>;
export type ProfileFormData = z.infer<typeof profileSchema>;
export type ContactFormData = z.infer<typeof contactSchema>;