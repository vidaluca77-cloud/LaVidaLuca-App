// Jest setup file for La Vida Luca App
const React = require('react');
require('@testing-library/jest-dom');

// Mock console methods in test environment
global.console = {
  ...console,
  // Uncomment to suppress logs during tests
  // log: jest.fn(),
  // warn: jest.fn(),
  // error: jest.fn(),
};

// Mock Next.js router
jest.mock('next/router', () => ({
  useRouter: () => ({
    route: '/',
    pathname: '/',
    query: {},
    asPath: '/',
    push: jest.fn(),
    replace: jest.fn(),
    back: jest.fn(),
  }),
}));

// Mock Next.js navigation
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
    back: jest.fn(),
    forward: jest.fn(),
    refresh: jest.fn(),
    prefetch: jest.fn(),
  }),
  usePathname: () => '/',
  useSearchParams: () => new URLSearchParams(),
}));

// Mock Heroicons
jest.mock('@heroicons/react/24/outline', () => ({
  HeartIcon: () => React.createElement('svg', { 'data-testid': 'heart-icon' }),
  AcademicCapIcon: () => React.createElement('svg', { 'data-testid': 'academic-cap-icon' }),
  GlobeAltIcon: () => React.createElement('svg', { 'data-testid': 'globe-alt-icon' }),
  MapPinIcon: () => React.createElement('svg', { 'data-testid': 'map-pin-icon' }),
  ClockIcon: () => React.createElement('svg', { 'data-testid': 'clock-icon' }),
  ShieldCheckIcon: () => React.createElement('svg', { 'data-testid': 'shield-check-icon' }),
  UserGroupIcon: () => React.createElement('svg', { 'data-testid': 'user-group-icon' }),
  StarIcon: () => React.createElement('svg', { 'data-testid': 'star-icon' }),
  ExclamationTriangleIcon: () => React.createElement('svg', { 'data-testid': 'exclamation-triangle-icon' }),
  WifiIcon: () => React.createElement('svg', { 'data-testid': 'wifi-icon' }),
  SignalIcon: () => React.createElement('svg', { 'data-testid': 'signal-icon' }),
  NoSymbolIcon: () => React.createElement('svg', { 'data-testid': 'no-symbol-icon' }),
  ArrowPathIcon: () => React.createElement('svg', { 'data-testid': 'arrow-path-icon' }),
  XMarkIcon: () => React.createElement('svg', { 'data-testid': 'x-mark-icon' }),
}));

// Mock monitoring module
jest.mock('./src/monitoring/performance', () => ({}));

// Mock environment variables for testing
process.env.NODE_ENV = 'test';
process.env.NEXT_PUBLIC_SENTRY_DSN = 'https://test@sentry.io/123456';

// Global test utilities
global.sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  observe() { return null; }
  disconnect() { return null; }
  unobserve() { return null; }
};

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  observe() { return null; }
  disconnect() { return null; }
  unobserve() { return null; }
};