/**
 * @jest-environment jsdom
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ConnectionStatusIndicator, OfflineNotification, OfflineBanner } from '../../src/components/ConnectionStatus';

// Mock the connection status hook
jest.mock('../../src/hooks/useConnectionStatus', () => ({
  useConnectionStatus: jest.fn(),
}));

// Mock Heroicons
jest.mock('@heroicons/react/24/outline', () => ({
  WifiIcon: ({ className }: { className: string }) => <div data-testid="wifi-icon" className={className} />,
  CloudArrowUpIcon: ({ className }: { className: string }) => <div data-testid="cloud-arrow-up-icon" className={className} />,
  ExclamationTriangleIcon: ({ className }: { className: string }) => <div data-testid="exclamation-triangle-icon" className={className} />,
  ClockIcon: ({ className }: { className: string }) => <div data-testid="clock-icon" className={className} />,
}));

const { useConnectionStatus } = require('../../src/hooks/useConnectionStatus');

describe('ConnectionStatus Components', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('ConnectionStatusIndicator', () => {
    it('should show online status when connected', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: true,
        queueLength: 0,
        isProcessing: false,
        lastOnline: null,
        lastOffline: null,
      });

      render(<ConnectionStatusIndicator />);

      expect(screen.getByText('En ligne')).toBeInTheDocument();
      expect(screen.getByTestId('wifi-icon')).toBeInTheDocument();
      
      const statusContainer = screen.getByText('En ligne').closest('div');
      expect(statusContainer).toHaveClass('text-green-500', 'bg-green-50');
    });

    it('should show synchronization status when online with queue', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: true,
        queueLength: 3,
        isProcessing: true,
        lastOnline: null,
        lastOffline: null,
      });

      render(<ConnectionStatusIndicator />);

      expect(screen.getByText('Synchronisation')).toBeInTheDocument();
      expect(screen.getByText('3')).toBeInTheDocument(); // Queue count badge
      expect(screen.getByTestId('cloud-arrow-up-icon')).toBeInTheDocument();
      
      const statusContainer = screen.getByText('Synchronisation').closest('div');
      expect(statusContainer).toHaveClass('text-yellow-500', 'bg-yellow-50');
    });

    it('should show offline status when disconnected', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: false,
        queueLength: 2,
        isProcessing: false,
        lastOnline: new Date(Date.now() - 60000), // 1 minute ago
        lastOffline: new Date(),
      });

      render(<ConnectionStatusIndicator />);

      expect(screen.getByText('Hors ligne')).toBeInTheDocument();
      expect(screen.getByText('2')).toBeInTheDocument(); // Queue count badge
      expect(screen.getByTestId('exclamation-triangle-icon')).toBeInTheDocument();
      
      const statusContainer = screen.getByText('Hors ligne').closest('div');
      expect(statusContainer).toHaveClass('text-red-500', 'bg-red-50');
    });

    it('should show processing spinner when syncing', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: true,
        queueLength: 1,
        isProcessing: true,
        lastOnline: null,
        lastOffline: null,
      });

      render(<ConnectionStatusIndicator />);

      // Check for spinner element
      const spinner = document.querySelector('.animate-spin');
      expect(spinner).toBeInTheDocument();
    });

    it('should show details when showDetails is true', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: false,
        queueLength: 5,
        isProcessing: false,
        lastOnline: new Date(Date.now() - 3600000), // 1 hour ago
        lastOffline: new Date(),
      });

      render(<ConnectionStatusIndicator showDetails={true} />);

      expect(screen.getByText(/Dernière connexion: Il y a/)).toBeInTheDocument();
      expect(screen.getByText('5 action(s) en file d\'attente')).toBeInTheDocument();
    });
  });

  describe('OfflineNotification', () => {
    it('should not render when online with empty queue', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: true,
        queueLength: 0,
        isProcessing: false,
      });

      const { container } = render(<OfflineNotification />);
      expect(container.firstChild).toBeNull();
    });

    it('should show synchronization notification when online with queue', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: true,
        queueLength: 3,
        isProcessing: true,
      });

      render(<OfflineNotification />);

      expect(screen.getByText('Synchronisation en cours')).toBeInTheDocument();
      expect(screen.getByText(/3 action\(s\) en cours de synchronisation/)).toBeInTheDocument();
    });

    it('should show offline notification when disconnected', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: false,
        queueLength: 2,
        isProcessing: false,
      });

      render(<OfflineNotification />);

      expect(screen.getByText('Mode hors ligne')).toBeInTheDocument();
      expect(screen.getByText(/Vous êtes hors ligne/)).toBeInTheDocument();
      expect(screen.getByText(/2 action\(s\) seront synchronisées/)).toBeInTheDocument();
    });

    it('should call onRetry when retry button is clicked', () => {
      const onRetry = jest.fn();
      
      useConnectionStatus.mockReturnValue({
        isOnline: false,
        queueLength: 1,
        isProcessing: false,
      });

      render(<OfflineNotification onRetry={onRetry} />);

      const retryButton = screen.getByText('Réessayer la connexion');
      fireEvent.click(retryButton);

      expect(onRetry).toHaveBeenCalled();
    });

    it('should call onDismiss when dismiss button is clicked', () => {
      const onDismiss = jest.fn();
      
      useConnectionStatus.mockReturnValue({
        isOnline: false,
        queueLength: 1,
        isProcessing: false,
      });

      render(<OfflineNotification onDismiss={onDismiss} />);

      const dismissButton = screen.getByRole('button', { name: /fermer/i });
      fireEvent.click(dismissButton);

      expect(onDismiss).toHaveBeenCalled();
    });
  });

  describe('OfflineBanner', () => {
    it('should not render when online', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: true,
        queueLength: 0,
        isProcessing: false,
      });

      const { container } = render(<OfflineBanner />);
      expect(container.firstChild).toBeNull();
    });

    it('should render offline banner when disconnected', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: false,
        queueLength: 4,
        isProcessing: false,
      });

      render(<OfflineBanner />);

      expect(screen.getByText(/Mode hors ligne activé/)).toBeInTheDocument();
      expect(screen.getByText(/4 action\(s\) en attente/)).toBeInTheDocument();
    });

    it('should call onSync when sync button is clicked', () => {
      const onSync = jest.fn();
      
      useConnectionStatus.mockReturnValue({
        isOnline: false,
        queueLength: 2,
        isProcessing: false,
      });

      render(<OfflineBanner onSync={onSync} />);

      const syncButton = screen.getByText('Synchroniser maintenant');
      fireEvent.click(syncButton);

      expect(onSync).toHaveBeenCalled();
    });

    it('should not show sync button when onSync is not provided', () => {
      useConnectionStatus.mockReturnValue({
        isOnline: false,
        queueLength: 2,
        isProcessing: false,
      });

      render(<OfflineBanner />);

      expect(screen.queryByText('Synchroniser maintenant')).not.toBeInTheDocument();
    });
  });
});