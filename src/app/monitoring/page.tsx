import { MonitoringDashboard } from '@/components/MonitoringDashboard';
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Monitoring Dashboard',
  description: 'Tableau de bord de surveillance et métriques de performance',
};

export default function MonitoringPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <MonitoringDashboard />
    </div>
  );
}