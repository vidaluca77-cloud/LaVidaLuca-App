/**
 * Test utilities and helpers for La Vida Luca App
 * This file contains reusable testing utilities and custom render functions
 */

import React, { ReactElement } from 'react';
import { render, RenderOptions, RenderResult } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

/**
 * Custom render function that wraps RTL's render with common providers
 */
export const renderWithProviders = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
): RenderResult => {
  // Wrapper component that includes common providers
  const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return <>{children}</>;
  };

  return render(ui, { wrapper: Wrapper, ...options });
};

/**
 * Creates a user event instance with default configuration
 */
export const createUser = () => {
  return userEvent.setup({
    // Advance timers automatically for user interactions
    advanceTimers: jest.advanceTimersByTime,
  });
};

/**
 * Mock data factories for testing
 */
export const mockData = {
  /**
   * Creates a mock user profile for testing
   */
  userProfile: (overrides = {}) => ({
    skills: ['elevage', 'hygiene'],
    availability: ['weekend', 'matin'],
    location: 'Ile-de-France',
    preferences: ['agri', 'nature'],
    ...overrides,
  }),

  /**
   * Creates a mock activity for testing
   */
  activity: (overrides = {}) => ({
    id: '1',
    slug: 'test-activity',
    title: 'Test Activity',
    category: 'agri' as const,
    summary: 'A test activity for unit testing',
    duration_min: 60,
    skill_tags: ['test_skill'],
    seasonality: ['toutes'],
    safety_level: 1,
    materials: ['gants'],
    ...overrides,
  }),

  /**
   * Creates a mock suggestion for testing
   */
  suggestion: (overrides = {}) => ({
    activity: mockData.activity(),
    score: 85,
    reasons: ['Test reason 1', 'Test reason 2'],
    ...overrides,
  }),
};

/**
 * Utility to wait for async operations in tests
 */
export const waitForAsync = () => new Promise(resolve => setTimeout(resolve, 0));

/**
 * Mock implementations for common functions
 */
export const mockFunctions = {
  /**
   * Mock console methods
   */
  mockConsole: () => {
    const originalConsole = { ...console };
    beforeEach(() => {
      jest.spyOn(console, 'log').mockImplementation();
      jest.spyOn(console, 'warn').mockImplementation();
      jest.spyOn(console, 'error').mockImplementation();
    });
    
    afterEach(() => {
      Object.assign(console, originalConsole);
    });
  },

  /**
   * Mock localStorage
   */
  mockLocalStorage: () => {
    const localStorageMock = {
      getItem: jest.fn(),
      setItem: jest.fn(),
      removeItem: jest.fn(),
      clear: jest.fn(),
    };
    
    Object.defineProperty(window, 'localStorage', {
      value: localStorageMock,
      writable: true,
    });
    
    return localStorageMock;
  },

  /**
   * Mock fetch API
   */
  mockFetch: () => {
    const mockFetch = jest.fn();
    global.fetch = mockFetch;
    return mockFetch;
  },
};

/**
 * Common test assertions
 */
export const assertions = {
  /**
   * Assert that an element has proper accessibility attributes
   */
  hasAccessibilityAttrs: (element: HTMLElement) => {
    // Check for basic accessibility
    const hasAriaLabel = element.hasAttribute('aria-label');
    const hasAriaLabelledBy = element.hasAttribute('aria-labelledby');
    const hasTitle = element.hasAttribute('title');
    const hasAltText = element.hasAttribute('alt');
    
    expect(hasAriaLabel || hasAriaLabelledBy || hasTitle || hasAltText).toBe(true);
  },

  /**
   * Assert that a form element is properly labeled
   */
  hasFormLabel: (element: HTMLElement) => {
    const hasLabel = element.closest('label') || 
                   document.querySelector(`label[for="${element.id}"]`) ||
                   element.hasAttribute('aria-label') ||
                   element.hasAttribute('aria-labelledby');
    
    expect(hasLabel).toBeTruthy();
  },
};

/**
 * Common test scenarios
 */
export const scenarios = {
  /**
   * Test responsive behavior by mocking different screen sizes
   */
  testResponsive: (component: ReactElement, tests: { [breakpoint: string]: () => void }) => {
    Object.entries(tests).forEach(([breakpoint, test]) => {
      describe(`on ${breakpoint}`, () => {
        beforeEach(() => {
          // Mock different screen sizes
          const queries = {
            mobile: '(max-width: 768px)',
            tablet: '(min-width: 768px) and (max-width: 1024px)',
            desktop: '(min-width: 1024px)',
          };
          
          window.matchMedia = jest.fn().mockImplementation(query => ({
            matches: query === queries[breakpoint as keyof typeof queries],
            media: query,
            onchange: null,
            addListener: jest.fn(),
            removeListener: jest.fn(),
            addEventListener: jest.fn(),
            removeEventListener: jest.fn(),
            dispatchEvent: jest.fn(),
          }));
        });
        
        test();
      });
    });
  },

  /**
   * Test keyboard navigation
   */
  testKeyboardNav: async (user: ReturnType<typeof createUser>, startElement: HTMLElement) => {
    const focusableElements = startElement.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    for (let i = 0; i < focusableElements.length; i++) {
      await user.tab();
      expect(focusableElements[i]).toHaveFocus();
    }
  },
};

/**
 * Re-export everything from RTL for convenience
 */
export * from '@testing-library/react';
export { userEvent };

/**
 * Default export of the custom render function
 */
export default renderWithProviders;