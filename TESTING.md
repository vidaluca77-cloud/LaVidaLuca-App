# Frontend Testing Documentation

## Overview

This document describes the comprehensive frontend testing setup for La Vida Luca App, including unit tests, integration tests, and automated testing workflows.

## Testing Stack

- **Jest**: Test runner and assertion library
- **React Testing Library**: Component testing utilities
- **User Event**: User interaction simulation
- **JSDOM**: DOM implementation for Node.js
- **Babel**: JavaScript transpilation for JSX/TypeScript

## Test Structure

### Unit Tests (`src/app/__tests__/`)

Component-specific tests that verify individual component behavior:

- **contact.test.tsx**: Contact form validation, submission, and error handling (9 tests)
- **catalogue.test.tsx**: Product filtering, search functionality, and display logic (11 tests)
- **layout.test.tsx**: Navigation, HTML structure, and accessibility (11 tests)
- **page.test.tsx**: Home page components, routing, and user interactions (12 tests)

### Integration Tests (`tests/integration/`)

End-to-end user flow tests that verify complete user journeys:

- **activity-browsing.test.tsx**: Complete catalog browsing flow (6 tests)
- **contact-submission.test.tsx**: Full contact form submission process (7 tests)
- **user-onboarding.test.tsx**: Multi-step onboarding and AI matching flow (4 tests)

## Running Tests

### Local Development

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test pattern
npm test -- --testPathPatterns="contact"
```

### Component Tests Only

```bash
npm test -- --testPathPatterns="src/app/__tests__"
```

### Integration Tests Only

```bash
npm test -- --testPathPatterns="tests/integration"
```

## Test Coverage

Current coverage for main components:

- **Contact Component**: 100% statement coverage
- **Catalogue Component**: 100% statement coverage  
- **Layout Component**: 100% statement coverage
- **Main Page Component**: 78% statement coverage
- **Overall App Coverage**: 77.77% statement coverage

Coverage reports are generated in the `coverage/` directory and include:
- HTML report: `coverage/lcov-report/index.html`
- LCOV format: `coverage/lcov.info`
- Text summary in terminal

## GitHub Actions Workflow

### Automated Testing Jobs

1. **Main Test Suite**: Runs on Node.js 18.x and 20.x
   - Linting with ESLint
   - TypeScript type checking
   - Full test suite with coverage
   - Application build verification

2. **Component Tests**: Focused component testing
   - Runs unit tests for all React components
   - Uploads coverage to Codecov

3. **Integration Tests**: User flow validation
   - Tests complete user journeys
   - Validates critical application paths

4. **Accessibility Tests**: 
   - Lighthouse CI for accessibility scoring
   - Minimum 90% accessibility score required

5. **Security Tests**:
   - npm audit for dependency vulnerabilities
   - Snyk security scanning

6. **Performance Tests**:
   - Bundle size analysis
   - Lighthouse performance scoring

### Workflow Triggers

Tests run automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual workflow dispatch

## Test Configuration

### Jest Configuration (`jest.config.js`)

```javascript
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy'
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
    '!src/app/globals.css'
  ]
}
```

### Test Setup (`jest.setup.js`)

Global test configuration including:
- React Testing Library matchers
- Next.js router mocking
- Fetch API mocking
- Performance Observer mocking
- IntersectionObserver mocking

## Writing Tests

### Component Test Example

```typescript
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import MyComponent from '../MyComponent';

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });

  it('handles user interaction', async () => {
    const user = userEvent.setup();
    render(<MyComponent />);
    
    await user.click(screen.getByRole('button'));
    expect(screen.getByText('Updated Text')).toBeInTheDocument();
  });
});
```

### Integration Test Example

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

describe('User Flow', () => {
  it('completes full user journey', async () => {
    const user = userEvent.setup();
    render(<App />);
    
    // Step 1: Navigate to page
    await user.click(screen.getByText('Start Journey'));
    
    // Step 2: Fill form
    await user.type(screen.getByLabelText('Name'), 'Test User');
    
    // Step 3: Submit and verify
    await user.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(screen.getByText('Success Message')).toBeInTheDocument();
    });
  });
});
```

## Best Practices

### Test Isolation
- Each test is independent and can run in any order
- Mock external dependencies (APIs, routers, etc.)
- Clean up after each test

### User-Centric Testing
- Test behavior, not implementation details
- Use semantic queries (getByRole, getByLabelText)
- Simulate real user interactions

### Comprehensive Coverage
- Test happy paths and error scenarios
- Include edge cases and boundary conditions
- Verify accessibility and responsive behavior

### Performance
- Keep tests fast and focused
- Use appropriate waiting strategies
- Mock heavy dependencies

## Accessibility Testing

### Automated Checks
- Lighthouse CI runs accessibility audits
- Minimum 90% accessibility score required
- Tests run on multiple pages

### Manual Testing Guidelines
- Test with keyboard navigation
- Verify screen reader compatibility
- Check color contrast ratios
- Validate ARIA labels and roles

## Continuous Improvement

### Monitoring
- Coverage reports track test completeness
- Failed tests are investigated and fixed quickly
- Performance metrics monitored over time

### Maintenance
- Tests are updated when components change
- New features include corresponding tests
- Regular review of test suite effectiveness

## Troubleshooting

### Common Issues

1. **JSDOM Limitations**: Some browser APIs not available
   - Solution: Mock missing APIs in jest.setup.js

2. **Async Timing**: Tests failing due to timing issues
   - Solution: Use waitFor() for async operations

3. **Component Mocking**: External components causing issues
   - Solution: Mock complex dependencies

### Debug Tips

```bash
# Run single test file
npm test -- contact.test.tsx

# Run with verbose output
npm test -- --verbose

# Run with coverage
npm test -- --coverage

# Debug specific test
npm test -- --testNamePattern="specific test name"
```

## Future Enhancements

- Add visual regression testing
- Implement E2E testing with Playwright
- Add API contract testing
- Enhance performance testing suite
- Add cross-browser testing