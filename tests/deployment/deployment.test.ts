/**
 * Tests de validation des configurations de déploiement
 */

import { readFileSync } from 'fs';
import { join } from 'path';

const projectRoot = join(__dirname, '../..');

describe('Deployment Configuration Tests', () => {
  describe('Vercel Configuration', () => {
    let vercelConfig: any;

    beforeAll(() => {
      const vercelConfigPath = join(projectRoot, 'vercel.json');
      const configContent = readFileSync(vercelConfigPath, 'utf-8');
      vercelConfig = JSON.parse(configContent);
    });

    test('should have proper vercel.json structure', () => {
      expect(vercelConfig).toHaveProperty('version', 2);
      expect(vercelConfig).toHaveProperty('builds');
      expect(vercelConfig).toHaveProperty('routes');
      expect(vercelConfig).toHaveProperty('headers');
    });

    test('should configure API routes properly', () => {
      const apiRoute = vercelConfig.routes.find((route: any) => 
        route.src === '/api/(.*)'
      );
      expect(apiRoute).toBeDefined();
      expect(apiRoute.dest).toContain('lavidaluca-backend.onrender.com');
    });

    test('should have security headers configured', () => {
      const headers = vercelConfig.headers[0].headers;
      const headerKeys = headers.map((h: any) => h.key);
      
      expect(headerKeys).toContain('X-Content-Type-Options');
      expect(headerKeys).toContain('X-Frame-Options');
      expect(headerKeys).toContain('Content-Security-Policy');
      expect(headerKeys).toContain('X-XSS-Protection');
    });

    test('should have production environment variables', () => {
      expect(vercelConfig.env).toHaveProperty('NEXT_PUBLIC_API_URL');
      expect(vercelConfig.env).toHaveProperty('NEXT_PUBLIC_ENVIRONMENT', 'production');
    });
  });

  describe('Render Configuration', () => {
    let renderConfig: string;

    beforeAll(() => {
      const renderConfigPath = join(projectRoot, 'apps/backend/render.yaml');
      renderConfig = readFileSync(renderConfigPath, 'utf-8');
    });

    test('should have proper render.yaml structure', () => {
      expect(renderConfig).toContain('version: "1"');
      expect(renderConfig).toContain('services:');
      expect(renderConfig).toContain('databases:');
    });

    test('should configure backend service properly', () => {
      expect(renderConfig).toContain('name: lavidaluca-backend');
      expect(renderConfig).toContain('runtime: python3');
      expect(renderConfig).toContain('healthCheckPath: /health');
    });

    test('should have security environment variables', () => {
      expect(renderConfig).toContain('JWT_SECRET_KEY');
      expect(renderConfig).toContain('CORS_ORIGINS');
      expect(renderConfig).toContain('TRUSTED_HOSTS');
      expect(renderConfig).toContain('RATE_LIMIT_REQUESTS_PER_MINUTE');
    });

    test('should configure database properly', () => {
      expect(renderConfig).toContain('name: lavidaluca-db');
      expect(renderConfig).toContain('postgresMajorVersion: 15');
    });
  });

  describe('Deployment Documentation', () => {
    test('should have deployment documentation', () => {
      const deploymentDocPath = join(projectRoot, 'DEPLOYMENT.md');
      expect(() => readFileSync(deploymentDocPath, 'utf-8')).not.toThrow();
    });

    test('should have deployment check script', () => {
      const scriptPath = join(projectRoot, 'scripts/check-deployment.sh');
      expect(() => readFileSync(scriptPath, 'utf-8')).not.toThrow();
    });
  });

  describe('Package.json Scripts', () => {
    let packageJson: any;

    beforeAll(() => {
      const packagePath = join(projectRoot, 'package.json');
      const packageContent = readFileSync(packagePath, 'utf-8');
      packageJson = JSON.parse(packageContent);
    });

    test('should have deployment-related scripts', () => {
      expect(packageJson.scripts).toHaveProperty('deploy:check');
      expect(packageJson.scripts).toHaveProperty('deploy:validate');
      expect(packageJson.scripts).toHaveProperty('deploy:docs');
    });
  });
});