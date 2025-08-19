#!/usr/bin/env python3
"""
Script de monitoring pour La Vida Luca
Vérifie la santé des services déployés et envoie des alertes si nécessaire.
"""

import os
import sys
import time
import json
import requests
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class HealthCheck:
    """Représente un test de santé"""
    name: str
    url: str
    expected_status: int = 200
    timeout: int = 10
    critical: bool = True


@dataclass
class HealthResult:
    """Résultat d'un test de santé"""
    check: HealthCheck
    success: bool
    response_time: float
    status_code: Optional[int] = None
    error: Optional[str] = None


class Monitor:
    """Gestionnaire de monitoring"""
    
    def __init__(self):
        self.web_url = os.getenv('WEB_URL', 'https://la-vida-luca.vercel.app')
        self.api_url = os.getenv('API_URL', 'https://la-vida-luca-api.onrender.com')
        self.discord_webhook = os.getenv('DISCORD_WEBHOOK_URL')
        self.environment = os.getenv('ENVIRONMENT', 'production')
        
        # Configuration des tests de santé
        self.health_checks = [
            # Frontend checks
            HealthCheck(
                name="Site Web - Page d'accueil",
                url=f"{self.web_url}/",
                critical=True
            ),
            HealthCheck(
                name="Site Web - Catalogue",
                url=f"{self.web_url}/catalogue",
                critical=True
            ),
            HealthCheck(
                name="Site Web - Contact",
                url=f"{self.web_url}/contact",
                critical=False
            ),
            
            # Backend API checks
            HealthCheck(
                name="API - Health Check",
                url=f"{self.api_url}/health",
                critical=True
            ),
            HealthCheck(
                name="API - Activités",
                url=f"{self.api_url}/api/v1/activities",
                critical=True
            ),
            HealthCheck(
                name="API - Documentation",
                url=f"{self.api_url}/docs",
                critical=False
            ),
        ]
    
    def run_health_check(self, check: HealthCheck) -> HealthResult:
        """Exécute un test de santé individuel"""
        start_time = time.time()
        
        try:
            response = requests.get(
                check.url,
                timeout=check.timeout,
                headers={'User-Agent': 'LaVidaLuca-Monitor/1.0'}
            )
            
            response_time = time.time() - start_time
            success = response.status_code == check.expected_status
            
            return HealthResult(
                check=check,
                success=success,
                response_time=response_time,
                status_code=response.status_code
            )
            
        except requests.exceptions.RequestException as e:
            response_time = time.time() - start_time
            return HealthResult(
                check=check,
                success=False,
                response_time=response_time,
                error=str(e)
            )
    
    def run_all_checks(self) -> List[HealthResult]:
        """Exécute tous les tests de santé"""
        results = []
        
        print(f"🏥 Début des tests de santé - {datetime.now(timezone.utc).isoformat()}")
        print(f"Environment: {self.environment}")
        print(f"Web URL: {self.web_url}")
        print(f"API URL: {self.api_url}")
        print("-" * 60)
        
        for check in self.health_checks:
            print(f"🔍 Test: {check.name}")
            result = self.run_health_check(check)
            results.append(result)
            
            if result.success:
                print(f"✅ OK ({result.response_time:.2f}s)")
            else:
                status = f" - Status: {result.status_code}" if result.status_code else ""
                error = f" - Error: {result.error}" if result.error else ""
                print(f"❌ ÉCHEC ({result.response_time:.2f}s){status}{error}")
            
            # Petit délai entre les tests
            time.sleep(1)
        
        return results
    
    def generate_report(self, results: List[HealthResult]) -> Dict:
        """Génère un rapport des résultats"""
        total_checks = len(results)
        successful_checks = sum(1 for r in results if r.success)
        failed_checks = total_checks - successful_checks
        critical_failures = sum(1 for r in results if not r.success and r.check.critical)
        
        avg_response_time = sum(r.response_time for r in results) / total_checks
        
        report = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'environment': self.environment,
            'summary': {
                'total_checks': total_checks,
                'successful': successful_checks,
                'failed': failed_checks,
                'critical_failures': critical_failures,
                'success_rate': (successful_checks / total_checks) * 100,
                'avg_response_time': avg_response_time
            },
            'details': []
        }
        
        for result in results:
            detail = {
                'name': result.check.name,
                'url': result.check.url,
                'success': result.success,
                'critical': result.check.critical,
                'response_time': result.response_time,
                'status_code': result.status_code,
                'error': result.error
            }
            report['details'].append(detail)
        
        return report
    
    def send_discord_notification(self, report: Dict):
        """Envoie une notification Discord"""
        if not self.discord_webhook:
            return
        
        summary = report['summary']
        critical_failures = summary['critical_failures']
        
        # Déterminer la couleur et l'emoji
        if critical_failures > 0:
            color = 0xFF0000  # Rouge
            emoji = "🚨"
            status = "CRITIQUE"
        elif summary['failed'] > 0:
            color = 0xFFA500  # Orange
            emoji = "⚠️"
            status = "ATTENTION"
        else:
            color = 0x00FF00  # Vert
            emoji = "✅"
            status = "OK"
        
        embed = {
            "title": f"{emoji} Monitoring La Vida Luca - {status}",
            "description": f"Rapport de santé - {self.environment}",
            "color": color,
            "timestamp": report['timestamp'],
            "fields": [
                {
                    "name": "📊 Résumé",
                    "value": f"**{summary['successful']}/{summary['total_checks']}** tests réussis\n"
                             f"Taux de succès: **{summary['success_rate']:.1f}%**\n"
                             f"Temps de réponse moyen: **{summary['avg_response_time']:.2f}s**",
                    "inline": True
                }
            ]
        }
        
        # Ajouter les détails des échecs
        failed_details = [d for d in report['details'] if not d['success']]
        if failed_details:
            failures_text = "\n".join([
                f"❌ {detail['name']}" + 
                (f" (Status: {detail['status_code']})" if detail['status_code'] else "") +
                (f" - {detail['error'][:100]}..." if detail['error'] else "")
                for detail in failed_details[:5]  # Limiter à 5 échecs
            ])
            
            embed["fields"].append({
                "name": "❌ Échecs détectés",
                "value": failures_text,
                "inline": False
            })
        
        payload = {
            "embeds": [embed]
        }
        
        try:
            response = requests.post(self.discord_webhook, json=payload, timeout=10)
            response.raise_for_status()
            print("📢 Notification Discord envoyée")
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur envoi Discord: {e}")
    
    def save_report(self, report: Dict):
        """Sauvegarde le rapport en JSON"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"monitoring_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📄 Rapport sauvegardé: {filename}")
        except Exception as e:
            print(f"❌ Erreur sauvegarde rapport: {e}")
    
    def run(self) -> int:
        """Exécute le monitoring complet"""
        try:
            results = self.run_all_checks()
            report = self.generate_report(results)
            
            print("\n" + "=" * 60)
            print("📊 RÉSUMÉ")
            print("=" * 60)
            
            summary = report['summary']
            print(f"Total des tests: {summary['total_checks']}")
            print(f"Réussis: {summary['successful']}")
            print(f"Échecs: {summary['failed']}")
            print(f"Échecs critiques: {summary['critical_failures']}")
            print(f"Taux de succès: {summary['success_rate']:.1f}%")
            print(f"Temps de réponse moyen: {summary['avg_response_time']:.2f}s")
            
            # Envoyer notifications
            self.send_discord_notification(report)
            
            # Sauvegarder le rapport en mode CI
            if os.getenv('CI'):
                self.save_report(report)
            
            # Code de retour
            if summary['critical_failures'] > 0:
                print("\n❌ Des échecs critiques ont été détectés!")
                return 1
            elif summary['failed'] > 0:
                print("\n⚠️ Des échecs non-critiques ont été détectés.")
                return 0
            else:
                print("\n✅ Tous les tests de santé sont OK!")
                return 0
                
        except Exception as e:
            print(f"\n💥 Erreur fatale dans le monitoring: {e}")
            return 1


def main():
    """Point d'entrée principal"""
    monitor = Monitor()
    exit_code = monitor.run()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()