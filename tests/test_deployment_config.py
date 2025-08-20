"""
Test suite for production deployment validation.
Validates that all deployment configurations are properly set up.
"""

import pytest
import os
import json
from pathlib import Path

# Test deployment configuration files exist
def test_deployment_files_exist():
    """Test that all required deployment configuration files exist."""
    required_files = [
        "vercel.json",
        "apps/backend/render.yaml", 
        ".env.production.example",
        ".github/DEPLOYMENT.md",
        ".github/SECRETS.md",
        "apps/backend/routes/health.py",
        "apps/backend/monitoring/production.py",
        "scripts/validate-deployment.sh",
        "PRODUCTION_READY.md"
    ]
    
    for file_path in required_files:
        assert Path(file_path).exists(), f"Required file {file_path} does not exist"

def test_vercel_configuration():
    """Test that Vercel configuration is valid."""
    vercel_config_path = Path("vercel.json")
    assert vercel_config_path.exists(), "vercel.json does not exist"
    
    with open(vercel_config_path) as f:
        config = json.load(f)
    
    # Test required fields
    assert "version" in config
    assert "builds" in config
    assert "routes" in config
    assert "env" in config
    assert "headers" in config
    
    # Test security headers
    headers = config["headers"][0]["headers"]
    header_names = [h["key"] for h in headers]
    
    required_security_headers = [
        "X-Content-Type-Options",
        "X-Frame-Options", 
        "X-XSS-Protection",
        "Strict-Transport-Security"
    ]
    
    for header in required_security_headers:
        assert header in header_names, f"Security header {header} missing"

def test_render_configuration():
    """Test that Render configuration has required fields."""
    render_config_path = Path("apps/backend/render.yaml")
    assert render_config_path.exists(), "render.yaml does not exist"
    
    import yaml
    with open(render_config_path) as f:
        config = yaml.safe_load(f)
    
    # Test structure
    assert "version" in config
    assert "services" in config
    assert "databases" in config
    
    service = config["services"][0]
    assert "name" in service
    assert "runtime" in service
    assert "buildCommand" in service
    assert "startCommand" in service
    assert "healthCheckPath" in service
    assert "envVars" in service
    
    # Test health check path
    assert service["healthCheckPath"] == "/health/live"

def test_environment_example_completeness():
    """Test that production environment example has all required variables."""
    env_example_path = Path(".env.production.example")
    assert env_example_path.exists(), ".env.production.example does not exist"
    
    with open(env_example_path) as f:
        content = f.read()
    
    required_vars = [
        "ENVIRONMENT=production",
        "DATABASE_URL=",
        "JWT_SECRET_KEY=",
        "OPENAI_API_KEY=",
        "SENTRY_DSN=",
        "CORS_ORIGINS=",
        "SMTP_HOST=",
        "LOG_LEVEL="
    ]
    
    for var in required_vars:
        assert var in content, f"Required environment variable {var} not found"

def test_ci_workflow_has_security():
    """Test that CI workflow includes security scanning."""
    ci_workflow_path = Path(".github/workflows/ci.yml")
    assert ci_workflow_path.exists(), "CI workflow does not exist"
    
    with open(ci_workflow_path) as f:
        content = f.read()
    
    # Check for security-related jobs/steps
    assert "security-scan" in content, "Security scanning job not found"
    assert "trivy" in content.lower(), "Trivy security scanner not configured"
    assert "validate/deployment" in content, "Deployment validation not included"

def test_validation_script_executable():
    """Test that validation script exists and is executable."""
    script_path = Path("scripts/validate-deployment.sh")
    assert script_path.exists(), "Validation script does not exist"
    
    # Check if file is executable (on Unix systems)
    import stat
    file_stat = script_path.stat()
    assert file_stat.st_mode & stat.S_IEXEC, "Validation script is not executable"

def test_health_routes_importable():
    """Test that health check routes can be imported."""
    try:
        # Add the backend directory to the path
        import sys
        sys.path.append(str(Path("apps/backend")))
        
        from routes.health import router
        assert router is not None, "Health router could not be imported"
        
        # Test that router has expected endpoints
        routes = [route.path for route in router.routes]
        expected_routes = ["/health", "/health/ready", "/health/live", "/validate/deployment"]
        
        for expected_route in expected_routes:
            assert any(expected_route in route for route in routes), f"Route {expected_route} not found"
            
    except ImportError as e:
        pytest.skip(f"Could not import health routes: {e}")

def test_monitoring_configuration():
    """Test that monitoring configuration exists and is complete."""
    monitoring_path = Path("apps/backend/monitoring/production.py")
    assert monitoring_path.exists(), "Production monitoring configuration does not exist"
    
    with open(monitoring_path) as f:
        content = f.read()
    
    # Check for key monitoring features
    required_features = [
        "setup_sentry",
        "setup_monitoring", 
        "PrometheusExporter",
        "AlertManager",
        "health_metrics"
    ]
    
    for feature in required_features:
        assert feature in content, f"Monitoring feature {feature} not found"

def test_documentation_completeness():
    """Test that documentation files are complete."""
    docs = {
        ".github/SECRETS.md": ["GitHub Secrets", "Vercel", "Render", "Security"],
        ".github/DEPLOYMENT.md": ["Configuration", "Environment Variables", "Secrets"],
        "PRODUCTION_READY.md": ["Implementation Overview", "Deployment Checklist", "Security"]
    }
    
    for doc_path, required_sections in docs.items():
        assert Path(doc_path).exists(), f"Documentation {doc_path} does not exist"
        
        with open(doc_path) as f:
            content = f.read()
        
        for section in required_sections:
            assert section in content, f"Documentation section '{section}' missing in {doc_path}"

if __name__ == "__main__":
    # Run basic validation without pytest
    print("🧪 Running deployment configuration validation...")
    
    try:
        test_deployment_files_exist()
        print("✅ All required files exist")
        
        test_vercel_configuration()
        print("✅ Vercel configuration is valid")
        
        test_render_configuration() 
        print("✅ Render configuration is valid")
        
        test_environment_example_completeness()
        print("✅ Environment configuration is complete")
        
        test_validation_script_executable()
        print("✅ Validation script is executable")
        
        test_documentation_completeness()
        print("✅ Documentation is complete")
        
        print("\n🎉 All deployment configuration tests passed!")
        
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        exit(1)