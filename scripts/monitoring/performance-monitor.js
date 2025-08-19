#!/usr/bin/env node

/**
 * Performance Monitoring Script for La Vida Luca
 * Monitors application performance and generates reports
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Configuration
const config = {
  endpoints: [
    {
      name: 'Web Application',
      url: process.env.VERCEL_PRODUCTION_URL || 'https://la-vida-luca.vercel.app',
      critical: true
    },
    {
      name: 'IA API',
      url: process.env.RENDER_SERVICE_URL || 'https://lavidaluca-ia-api.onrender.com',
      critical: true
    },
    {
      name: 'IA API Health',
      url: (process.env.RENDER_SERVICE_URL || 'https://lavidaluca-ia-api.onrender.com') + '/health',
      critical: false
    }
  ],
  timeout: 30000,
  retries: 3,
  outputDir: './monitoring-reports'
};

// Ensure output directory exists
if (!fs.existsSync(config.outputDir)) {
  fs.mkdirSync(config.outputDir, { recursive: true });
}

// Performance monitoring function
async function monitorEndpoint(endpoint) {
  const results = [];
  
  for (let attempt = 1; attempt <= config.retries; attempt++) {
    const startTime = Date.now();
    
    try {
      const result = await makeRequest(endpoint.url, config.timeout);
      const responseTime = Date.now() - startTime;
      
      results.push({
        attempt,
        success: true,
        responseTime,
        statusCode: result.statusCode,
        contentLength: result.contentLength,
        timestamp: new Date().toISOString()
      });
      
      console.log(`✓ ${endpoint.name} - ${responseTime}ms (${result.statusCode})`);
      
    } catch (error) {
      const responseTime = Date.now() - startTime;
      
      results.push({
        attempt,
        success: false,
        responseTime,
        error: error.message,
        timestamp: new Date().toISOString()
      });
      
      console.log(`✗ ${endpoint.name} - Failed: ${error.message}`);
    }
    
    // Wait between retries
    if (attempt < config.retries) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  return {
    endpoint: endpoint.name,
    url: endpoint.url,
    critical: endpoint.critical,
    results,
    summary: calculateSummary(results)
  };
}

// HTTP request function
function makeRequest(url, timeout) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const client = urlObj.protocol === 'https:' ? https : http;
    
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      timeout: timeout,
      headers: {
        'User-Agent': 'LaVidaLuca-Monitor/1.0'
      }
    };
    
    const req = client.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          contentLength: data.length,
          headers: res.headers
        });
      });
    });
    
    req.on('error', (error) => {
      reject(error);
    });
    
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    
    req.end();
  });
}

// Calculate summary statistics
function calculateSummary(results) {
  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);
  
  if (successful.length === 0) {
    return {
      availability: 0,
      avgResponseTime: null,
      minResponseTime: null,
      maxResponseTime: null,
      successCount: 0,
      failureCount: failed.length
    };
  }
  
  const responseTimes = successful.map(r => r.responseTime);
  
  return {
    availability: (successful.length / results.length) * 100,
    avgResponseTime: responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length,
    minResponseTime: Math.min(...responseTimes),
    maxResponseTime: Math.max(...responseTimes),
    successCount: successful.length,
    failureCount: failed.length
  };
}

// Generate HTML report
function generateHTMLReport(monitoringResults) {
  const timestamp = new Date().toISOString();
  const reportDate = new Date().toLocaleDateString('fr-FR');
  
  let html = `
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Monitoring - La Vida Luca</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header { text-align: center; border-bottom: 2px solid #22c55e; padding-bottom: 20px; margin-bottom: 30px; }
        .status-good { color: #22c55e; }
        .status-warning { color: #f59e0b; }
        .status-error { color: #ef4444; }
        .endpoint-card { border: 1px solid #ddd; border-radius: 6px; padding: 15px; margin-bottom: 20px; }
        .metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }
        .metric { background: #f9f9f9; padding: 10px; border-radius: 4px; text-align: center; }
        .metric-value { font-size: 1.5em; font-weight: bold; }
        .timestamp { color: #666; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌱 Rapport de Monitoring - La Vida Luca</h1>
            <p class="timestamp">Généré le ${reportDate} à ${new Date().toLocaleTimeString('fr-FR')}</p>
        </div>
`;

  monitoringResults.forEach(result => {
    const status = result.summary.availability === 100 ? 'good' : 
                  result.summary.availability >= 80 ? 'warning' : 'error';
    
    html += `
        <div class="endpoint-card">
            <h2 class="status-${status}">${result.endpoint}</h2>
            <p><strong>URL:</strong> ${result.url}</p>
            <p><strong>Critique:</strong> ${result.critical ? 'Oui' : 'Non'}</p>
            
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value status-${status}">${result.summary.availability.toFixed(1)}%</div>
                    <div>Disponibilité</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${result.summary.avgResponseTime ? Math.round(result.summary.avgResponseTime) : 'N/A'}ms</div>
                    <div>Temps de réponse moyen</div>
                </div>
                <div class="metric">
                    <div class="metric-value status-good">${result.summary.successCount}</div>
                    <div>Succès</div>
                </div>
                <div class="metric">
                    <div class="metric-value status-error">${result.summary.failureCount}</div>
                    <div>Échecs</div>
                </div>
            </div>
        </div>
    `;
  });

  html += `
        <div class="footer">
            <p class="timestamp">Rapport généré automatiquement par le système de monitoring La Vida Luca</p>
        </div>
    </div>
</body>
</html>
`;

  return html;
}

// Main monitoring function
async function runMonitoring() {
  console.log('🌱 Démarrage du monitoring La Vida Luca...\n');
  
  const results = [];
  
  for (const endpoint of config.endpoints) {
    console.log(`Monitoring ${endpoint.name}...`);
    const result = await monitorEndpoint(endpoint);
    results.push(result);
    console.log('');
  }
  
  // Generate reports
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  
  // JSON report
  const jsonReport = {
    timestamp: new Date().toISOString(),
    results: results,
    summary: {
      totalEndpoints: results.length,
      healthyEndpoints: results.filter(r => r.summary.availability === 100).length,
      criticalIssues: results.filter(r => r.critical && r.summary.availability < 100).length
    }
  };
  
  fs.writeFileSync(
    path.join(config.outputDir, `monitoring-${timestamp}.json`),
    JSON.stringify(jsonReport, null, 2)
  );
  
  // HTML report
  const htmlReport = generateHTMLReport(results);
  fs.writeFileSync(
    path.join(config.outputDir, `monitoring-${timestamp}.html`),
    htmlReport
  );
  
  // Latest report (overwrites previous)
  fs.writeFileSync(
    path.join(config.outputDir, 'latest-monitoring.json'),
    JSON.stringify(jsonReport, null, 2)
  );
  
  fs.writeFileSync(
    path.join(config.outputDir, 'latest-monitoring.html'),
    htmlReport
  );
  
  console.log('📊 Rapports générés:');
  console.log(`  - JSON: monitoring-${timestamp}.json`);
  console.log(`  - HTML: monitoring-${timestamp}.html`);
  console.log(`  - Latest: latest-monitoring.json & latest-monitoring.html`);
  
  // Exit with appropriate code
  const criticalIssues = jsonReport.summary.criticalIssues;
  if (criticalIssues > 0) {
    console.log(`\n❌ ${criticalIssues} problème(s) critique(s) détecté(s)`);
    process.exit(1);
  } else {
    console.log('\n✅ Tous les services critiques sont opérationnels');
    process.exit(0);
  }
}

// Run monitoring
if (require.main === module) {
  runMonitoring().catch(error => {
    console.error('❌ Erreur lors du monitoring:', error);
    process.exit(2);
  });
}

module.exports = { runMonitoring, monitorEndpoint };