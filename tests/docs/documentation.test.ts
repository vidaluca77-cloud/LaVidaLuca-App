/**
 * Test suite for documentation structure and content
 */

import fs from 'fs';
import path from 'path';

describe('Documentation Tests', () => {
  const readmeContent = fs.readFileSync(
    path.join(process.cwd(), 'README.md'), 
    'utf-8'
  );

  test('README should have main sections', () => {
    const expectedSections = [
      '# La Vida Luca - Documentation',
      '## Vue d\'ensemble',
      '## Architecture',
      '## Installation',
      '## Scripts disponibles',
      '## Structure du projet',
      '## Déploiement',
      '## Monitoring et Observabilité',
      '## API et Intégrations',
      '## Tests',
      '## Contribution',
      '## Sécurité',
      '## Performance',
      '## Support et Contact',
      '## Roadmap'
    ];

    expectedSections.forEach(section => {
      expect(readmeContent).toContain(section);
    });
  });

  test('README should contain installation instructions', () => {
    expect(readmeContent).toContain('git clone');
    expect(readmeContent).toContain('npm install');
    expect(readmeContent).toContain('npm run dev');
  });

  test('README should contain environment variables documentation', () => {
    expect(readmeContent).toContain('NEXT_PUBLIC_API_URL');
    expect(readmeContent).toContain('NEXT_PUBLIC_SENTRY_DSN');
    expect(readmeContent).toContain('.env.local');
  });

  test('README should contain architecture diagram', () => {
    expect(readmeContent).toContain('```mermaid');
    expect(readmeContent).toContain('graph TB');
    expect(readmeContent).toContain('Next.js Frontend');
    expect(readmeContent).toContain('PostgreSQL');
    expect(readmeContent).toContain('Sentry');
  });

  test('README should contain deployment instructions', () => {
    expect(readmeContent).toContain('Vercel');
    expect(readmeContent).toContain('git push origin main');
    expect(readmeContent).toContain('vercel --prod');
  });

  test('README should contain monitoring information', () => {
    expect(readmeContent).toContain('Sentry');
    expect(readmeContent).toContain('métriques');
    expect(readmeContent).toContain('performance');
    expect(readmeContent).toContain('alertes');
  });

  test('README should contain performance targets', () => {
    expect(readmeContent).toContain('FCP');
    expect(readmeContent).toContain('LCP');
    expect(readmeContent).toContain('CLS');
    expect(readmeContent).toContain('FID');
  });

  test('README should contain contribution guidelines', () => {
    expect(readmeContent).toContain('Fork');
    expect(readmeContent).toContain('Pull Request');
    expect(readmeContent).toContain('ESLint');
    expect(readmeContent).toContain('TypeScript');
  });

  test('README should contain contact information', () => {
    expect(readmeContent).toContain('tech@lavidaluca.fr');
    expect(readmeContent).toContain('GitHub Issues');
  });
});

describe('Configuration Files', () => {
  test('Sentry configuration files should exist', () => {
    const sentryClientConfig = path.join(process.cwd(), 'sentry.client.config.ts');
    const sentryServerConfig = path.join(process.cwd(), 'sentry.server.config.ts');
    const sentryEdgeConfig = path.join(process.cwd(), 'sentry.edge.config.ts');

    expect(fs.existsSync(sentryClientConfig)).toBe(true);
    expect(fs.existsSync(sentryServerConfig)).toBe(true);
    expect(fs.existsSync(sentryEdgeConfig)).toBe(true);
  });

  test('Monitoring files should exist', () => {
    const alertsFile = path.join(process.cwd(), 'src/monitoring/alerts.ts');
    const performanceFile = path.join(process.cwd(), 'src/monitoring/performance.ts');
    const dashboardFile = path.join(process.cwd(), 'src/monitoring/dashboard.ts');

    expect(fs.existsSync(alertsFile)).toBe(true);
    expect(fs.existsSync(performanceFile)).toBe(true);
    expect(fs.existsSync(dashboardFile)).toBe(true);
  });

  test('Backend monitoring structure should exist', () => {
    const loggerFile = path.join(process.cwd(), 'backend/monitoring/logger.py');
    const metricsFile = path.join(process.cwd(), 'backend/monitoring/metrics.py');
    const openApiFile = path.join(process.cwd(), 'backend/docs/openapi.py');

    expect(fs.existsSync(loggerFile)).toBe(true);
    expect(fs.existsSync(metricsFile)).toBe(true);
    expect(fs.existsSync(openApiFile)).toBe(true);
  });

  test('Package.json should contain correct scripts', () => {
    const packageJson = JSON.parse(
      fs.readFileSync(path.join(process.cwd(), 'package.json'), 'utf-8')
    );

    expect(packageJson.scripts).toHaveProperty('dev');
    expect(packageJson.scripts).toHaveProperty('build');
    expect(packageJson.scripts).toHaveProperty('start');
    expect(packageJson.scripts).toHaveProperty('lint');
    expect(packageJson.scripts).toHaveProperty('type-check');
    expect(packageJson.scripts).toHaveProperty('test');
  });

  test('Package.json should contain Sentry dependency', () => {
    const packageJson = JSON.parse(
      fs.readFileSync(path.join(process.cwd(), 'package.json'), 'utf-8')
    );

    expect(packageJson.dependencies).toHaveProperty('@sentry/nextjs');
  });
});