# Configuration Overview

This document describes the project configuration and setup for La Vida Luca App.

## Dependencies

### Core Dependencies

- **Next.js 14.0.4**: React framework with app router
- **React 18.2.0**: UI library
- **TypeScript 5.3.3**: Type safety
- **Tailwind CSS 3.4.0**: Utility-first CSS framework

### Development Dependencies

- **ESLint**: Code linting with TypeScript support
- **Prettier**: Code formatting
- **Jest**: Testing framework
- **React Testing Library**: Component testing utilities

## Scripts

- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run ESLint
- `npm run lint:fix`: Auto-fix ESLint issues
- `npm run type-check`: TypeScript type checking
- `npm run test`: Run tests
- `npm run test:watch`: Run tests in watch mode
- `npm run test:coverage`: Run tests with coverage
- `npm run format`: Format code with Prettier
- `npm run format:check`: Check formatting

## Configuration Files

### TypeScript (`tsconfig.json`)

- Configured for Next.js 14 with app router
- Path mapping for `@/*` imports
- Includes Jest DOM types

### ESLint (`.eslintrc.json`)

- Next.js recommended rules
- TypeScript support
- Prettier integration
- Disabled `react/no-unescaped-entities` for French content

### Prettier (`.prettierrc.json`)

- Single quotes for JavaScript
- Semicolons enabled
- 80 character line width
- 2 space indentation

### Jest (`jest.config.js`)

- Next.js integration
- jsdom environment for React testing
- Path mapping support
- Coverage thresholds: 70% for all metrics

## Directory Structure

```
├── __tests__/              # Test files
├── .github/workflows/      # CI/CD workflows
├── src/
│   ├── app/               # Next.js app router pages
│   ├── components/        # Reusable components
│   └── utils/             # Utility functions
├── types/                 # TypeScript type declarations
└── public/               # Static assets
```

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`):

- Runs on Node.js 18.x and 20.x
- Type checking
- ESLint validation
- Prettier format check
- Test execution with coverage
- Production build verification

## Getting Started

1. Install dependencies: `npm install`
2. Run development server: `npm run dev`
3. Run tests: `npm run test`
4. Build for production: `npm run build`
