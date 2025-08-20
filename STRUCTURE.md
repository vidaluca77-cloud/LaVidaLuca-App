# LaVidaLuca-App - Project Structure & Architecture

## 🏗️ Project Overview

LaVidaLuca is a collaborative learning platform dedicated to training young people in MFR (Maisons Familiales Rurales) and developing new agriculture practices. The project is built as a modern monorepo with clear separation of concerns between frontend and backend.

## 📁 Monorepo Structure

```
LaVidaLuca-App/
├── .github/workflows/          # CI/CD GitHub Actions
│   ├── ci.yml                 # Continuous Integration pipeline
│   ├── deploy.yml             # Deployment pipeline
│   └── backend.yml            # Backend-specific workflows
├── .vscode/                   # VSCode workspace configuration
│   ├── settings.json          # Workspace settings
│   ├── launch.json            # Debug configurations
│   ├── extensions.json        # Recommended extensions
│   └── tasks.json             # Build/run tasks
├── apps/                      # Application modules
│   ├── backend/              # FastAPI backend application
│   └── web/                  # Next.js frontend application
├── LaVidaLuca.code-workspace # VSCode workspace file
├── package.json              # Monorepo scripts and dependencies
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore configuration
└── README.md                # Project documentation
```

## 🔧 Backend Architecture (FastAPI)

### Directory Structure
```
apps/backend/
├── alembic/                  # Database migrations
├── app/                      # Main application module
│   ├── api/                 # API routes and endpoints
│   ├── core/                # Core configuration and security
│   ├── models/              # SQLAlchemy database models
│   ├── schemas/             # Pydantic request/response schemas
│   └── services/            # Business logic layer
├── auth/                     # Authentication module
├── docs/                     # API documentation
├── migrations/               # Database migration files
├── monitoring/               # Application monitoring setup
├── routes/                   # API route definitions
├── services/                 # Service layer implementations
├── tests/                    # Unit and integration tests
├── main.py                   # Application entry point
├── config.py                 # Configuration management
├── database.py               # Database connection setup
├── middleware.py             # Custom middleware
├── requirements.txt          # Python dependencies
└── Dockerfile               # Container configuration
```

### Key Features
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migration management
- **JWT Authentication**: Secure user authentication
- **Pydantic**: Data validation and serialization
- **AsyncPG**: Asynchronous PostgreSQL driver
- **Sentry**: Error tracking and monitoring
- **Prometheus**: Metrics collection
- **OpenAPI**: Automatic API documentation

### Configuration
- **Environment-based settings**: Development, testing, production
- **Database pooling**: Optimized connection management
- **CORS configuration**: Cross-origin resource sharing
- **Rate limiting**: Request throttling
- **Security headers**: Enhanced security

## 🌐 Frontend Architecture (Next.js)

### Directory Structure
```
apps/web/
├── app/                      # Next.js App Router
│   ├── (pages)/             # Page routes
│   ├── api/                 # API routes (if needed)
│   ├── components/          # Page-specific components
│   ├── globals.css          # Global styles
│   ├── layout.tsx           # Root layout
│   └── page.tsx             # Home page
├── public/                   # Static assets
│   ├── icons/               # PWA icons
│   ├── images/              # Image assets
│   └── manifest.json        # PWA manifest
├── src/                      # Source code
│   ├── components/          # Reusable UI components
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Utility functions and configs
│   ├── types/               # TypeScript type definitions
│   └── utils/               # Helper functions
├── package.json              # Dependencies and scripts
├── next.config.ts            # Next.js configuration
├── tailwind.config.ts        # Tailwind CSS configuration
├── tsconfig.json             # TypeScript configuration
└── postcss.config.mjs        # PostCSS configuration
```

### Key Features
- **Next.js 15**: React framework with App Router
- **React 19**: Latest React features
- **TypeScript**: Type safety and better DX
- **Tailwind CSS**: Utility-first CSS framework
- **PWA Support**: Progressive Web App capabilities
- **Sentry Integration**: Error tracking
- **ESLint + Prettier**: Code quality and formatting

## 🛠️ Development Environment

### Prerequisites
- **Node.js**: 20+ (LTS recommended)
- **Python**: 3.12+
- **PostgreSQL**: 15+
- **Git**: Latest version

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/vidaluca77-cloud/LaVidaLuca-App.git
   cd LaVidaLuca-App
   ```

2. **Install dependencies**
   ```bash
   npm run setup
   ```

3. **Set up environment variables**
   ```bash
   # Backend
   cd apps/backend
   cp .env.example .env
   # Edit .env with your configuration
   
   # Frontend
   cd ../web
   cp .env.local.example .env.local
   # Edit .env.local with your configuration
   ```

4. **Database setup**
   ```bash
   # Start PostgreSQL service
   # Create database: lavidaluca_dev
   
   # Run migrations
   npm run backend:migrate
   ```

5. **Start development servers**
   ```bash
   # Full stack development
   npm run dev:full
   
   # Or individually:
   npm run dev:web      # Frontend only (port 3000)
   npm run dev:backend  # Backend only (port 8000)
   ```

### VSCode Setup
1. Install recommended extensions from `.vscode/extensions.json`
2. Open the workspace file: `LaVidaLuca.code-workspace`
3. Configure Python interpreter path for backend development

## 📊 Available Scripts

### Monorepo Scripts (Root)
| Script | Description |
|--------|-------------|
| `npm run dev:full` | Start both frontend and backend |
| `npm run dev:web` | Start frontend development server |
| `npm run dev:backend` | Start backend development server |
| `npm run build` | Build frontend for production |
| `npm run lint` | Lint frontend code |
| `npm run test` | Run backend tests |
| `npm run setup` | Install all dependencies |
| `npm run clean` | Clean build artifacts |

### Backend Scripts
| Script | Description |
|--------|-------------|
| `npm run backend:dev` | Start backend with hot reload |
| `npm run backend:test` | Run Python tests |
| `npm run backend:migrate` | Apply database migrations |
| `npm run backend:migration` | Create new migration |
| `npm run backend:docs` | View API documentation info |

### Frontend Scripts
| Script | Description |
|--------|-------------|
| `npm run lint:web` | Lint frontend code |
| `npm run build:web` | Build frontend |
| `npm run type-check:web` | TypeScript type checking |

## 🚀 Deployment

### Backend Deployment (Render)
- **Platform**: Render.com
- **Configuration**: `render.yaml`
- **Environment**: Production settings via environment variables
- **Database**: PostgreSQL on Render
- **Monitoring**: Sentry + Prometheus metrics

### Frontend Deployment (Vercel)
- **Platform**: Vercel
- **Configuration**: `vercel.json` (auto-detected)
- **Environment**: Environment variables via Vercel dashboard
- **CDN**: Automatic global distribution
- **Analytics**: Vercel Analytics integration

### CI/CD Pipeline
- **Trigger**: Push to `main` branch or pull requests
- **Tests**: Automated testing for both frontend and backend
- **Deployment**: Automatic deployment on successful tests
- **Monitoring**: Deployment status and health checks

## 🔍 Monitoring & Observability

### Error Tracking
- **Sentry**: Real-time error tracking and performance monitoring
- **Configuration**: Separate DSNs for frontend and backend
- **Features**: Error grouping, performance insights, release tracking

### Metrics & Logging
- **Prometheus**: Metrics collection for backend
- **Custom Metrics**: Request counts, response times, error rates
- **Health Checks**: Application and database health monitoring
- **Structured Logging**: JSON-formatted logs with correlation IDs

### Development Tools
- **Hot Reload**: Automatic restart on code changes
- **Debug Configuration**: VSCode debug settings for both apps
- **API Documentation**: Swagger UI at `/docs`
- **Database Migrations**: Automatic schema management

## 🔒 Security

### Authentication & Authorization
- **JWT Tokens**: Stateless authentication
- **Token Refresh**: Automatic token renewal
- **Role-based Access**: User permission system
- **CORS Configuration**: Secure cross-origin requests

### Security Measures
- **Input Validation**: Pydantic schemas for API validation
- **SQL Injection Protection**: SQLAlchemy ORM
- **Rate Limiting**: Request throttling
- **Security Headers**: CSRF, XSS protection
- **HTTPS Enforcement**: Secure communication

## 🧪 Testing Strategy

### Backend Testing
- **Unit Tests**: Individual component testing
- **Integration Tests**: API endpoint testing
- **Database Tests**: Repository layer testing
- **Coverage**: Comprehensive test coverage reporting

### Frontend Testing
- **Component Tests**: React component testing
- **E2E Tests**: End-to-end user flows
- **Type Testing**: TypeScript compilation checks
- **Lint Testing**: Code quality verification

## 📚 Documentation

### API Documentation
- **OpenAPI Specification**: Auto-generated from FastAPI
- **Interactive Docs**: Swagger UI interface
- **Response Examples**: Sample API responses
- **Authentication Guide**: JWT integration examples

### Development Guides
- **Setup Instructions**: Environment configuration
- **Coding Standards**: Style guides and best practices
- **Architecture Decisions**: Technical choices documentation
- **Troubleshooting**: Common issues and solutions

## 🤝 Contributing

### Development Workflow
1. Create feature branch from `main`
2. Make changes following coding standards
3. Write/update tests for new features
4. Ensure all tests pass locally
5. Create pull request with description
6. Code review and CI/CD validation
7. Merge to main and deploy

### Code Standards
- **TypeScript**: Strict type checking
- **ESLint**: JavaScript/TypeScript linting
- **Prettier**: Code formatting
- **Black**: Python code formatting
- **Conventional Commits**: Standardized commit messages

## 📞 Support

### Development Environment Issues
- Check VSCode workspace configuration
- Verify Python virtual environment setup
- Ensure PostgreSQL connection
- Review environment variable configuration

### Production Issues
- Check Sentry error reports
- Review deployment logs
- Verify environment variable configuration
- Monitor application metrics

For technical support, please create an issue in the GitHub repository with detailed information about the problem.