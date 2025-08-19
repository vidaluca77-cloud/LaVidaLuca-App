import fs from 'fs'
import path from 'path'

describe('Project structure', () => {
  it('should have the correct monorepo structure', () => {
    const rootDir = path.resolve(__dirname, '../../..')
    
    // Check main directories exist
    expect(fs.existsSync(path.join(rootDir, 'apps'))).toBe(true)
    expect(fs.existsSync(path.join(rootDir, 'apps/frontend'))).toBe(true)
    expect(fs.existsSync(path.join(rootDir, 'apps/backend'))).toBe(true)
    expect(fs.existsSync(path.join(rootDir, 'packages'))).toBe(true)
    expect(fs.existsSync(path.join(rootDir, 'packages/shared'))).toBe(true)
    expect(fs.existsSync(path.join(rootDir, '.github/workflows'))).toBe(true)
  })

  it('should have required configuration files', () => {
    const rootDir = path.resolve(__dirname, '../../..')
    
    // Check config files exist
    expect(fs.existsSync(path.join(rootDir, 'tsconfig.json'))).toBe(true)
    expect(fs.existsSync(path.join(rootDir, '.eslintrc.js'))).toBe(true)
    expect(fs.existsSync(path.join(rootDir, 'docker-compose.yml'))).toBe(true)
    expect(fs.existsSync(path.join(rootDir, '.github/workflows/ci.yml'))).toBe(true)
  })

  it('should have backend files', () => {
    const backendDir = path.resolve(__dirname, '../../../apps/backend')
    
    expect(fs.existsSync(path.join(backendDir, 'Dockerfile'))).toBe(true)
    expect(fs.existsSync(path.join(backendDir, 'requirements.txt'))).toBe(true)
    expect(fs.existsSync(path.join(backendDir, 'src/main.py'))).toBe(true)
    expect(fs.existsSync(path.join(backendDir, 'tests'))).toBe(true)
  })
})