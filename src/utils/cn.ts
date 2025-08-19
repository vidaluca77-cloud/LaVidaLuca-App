import { type ClassValue, clsx } from 'clsx';

// Simple className utility - we'll install clsx if needed
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

// Alternative simple implementation if clsx is not available
export function classNames(...classes: (string | undefined | null | boolean)[]): string {
  return classes.filter(Boolean).join(' ');
}