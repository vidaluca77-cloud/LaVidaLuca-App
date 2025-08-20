import { EnhancedMonitoringDashboard } from '@/components/EnhancedMonitoringDashboard';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Enhanced Monitoring Dashboard',
  description: 'Tableau de bord de surveillance avancé avec métriques PWA et mode hors ligne',
};

export default function MonitoringPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <EnhancedMonitoringDashboard />
    </div>
  );
}