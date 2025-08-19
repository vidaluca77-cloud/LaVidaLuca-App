/**
 * Test setup configuration for La Vida Luca App
 * This file contains setup utilities and configurations for React Testing Library
 */

import { configure } from '@testing-library/react';
import '@testing-library/jest-dom';

// Configure React Testing Library
configure({
  // Throw helpful errors if accessibility queries fail
  testIdAttribute: 'data-testid',
  // Increase the timeout for async utils
  asyncUtilTimeout: 5000,
  // Show debugging info when tests fail
  getElementError: (message, container) => {
    const error = new Error(
      `${message}\n\nDebugging info:\n${container.innerHTML}`
    );
    error.name = 'TestingLibraryElementError';
    return error;
  }
});

// Global test environment setup
beforeEach(() => {
  // Clear all mocks before each test
  jest.clearAllMocks();
  
  // Reset any DOM mutations
  document.body.innerHTML = '';
  
  // Reset window location
  delete (window as any).location;
  (window as any).location = {
    href: 'http://localhost:3000',
    origin: 'http://localhost:3000',
    pathname: '/',
    search: '',
    hash: '',
  };
});

afterEach(() => {
  // Clean up after each test
  jest.clearAllTimers();
  jest.useRealTimers();
});

// Mock window.matchMedia for responsive design tests
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(), // deprecated
    removeListener: jest.fn(), // deprecated
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock window.scrollTo for scroll-related tests
Object.defineProperty(window, 'scrollTo', {
  writable: true,
  value: jest.fn(),
});

// Mock HTMLElement.scrollIntoView
Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
  writable: true,
  value: jest.fn(),
});

export {};