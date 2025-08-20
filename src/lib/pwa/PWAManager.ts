/**
 * PWA Utilities for Service Worker and Push Notifications
 * Handles service worker registration, updates, and push notification setup
 */

export interface PWAInstallPrompt {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
}

export interface PushSubscriptionOptions {
  userVisibleOnly: boolean;
  applicationServerKey: string;
}

export class PWAManager {
  private static instance: PWAManager;
  private swRegistration: ServiceWorkerRegistration | null = null;
  private installPromptEvent: PWAInstallPrompt | null = null;
  private updateAvailable = false;

  static getInstance(): PWAManager {
    if (!PWAManager.instance) {
      PWAManager.instance = new PWAManager();
    }
    return PWAManager.instance;
  }

  /**
   * Initialize PWA features
   */
  async init(): Promise<void> {
    if (typeof window === 'undefined' || !('serviceWorker' in navigator)) {
      console.warn('Service Worker not supported');
      return;
    }

    try {
      // Register service worker
      await this.registerServiceWorker();
      
      // Set up install prompt listener
      this.setupInstallPrompt();
      
      // Set up update detection
      this.setupUpdateDetection();
      
      console.log('PWA Manager initialized successfully');
    } catch (error) {
      console.error('PWA initialization failed:', error);
    }
  }

  /**
   * Register the service worker
   */
  private async registerServiceWorker(): Promise<void> {
    try {
      this.swRegistration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/'
      });

      console.log('Service Worker registered successfully:', this.swRegistration.scope);

      // Listen for messages from service worker
      navigator.serviceWorker.addEventListener('message', this.handleServiceWorkerMessage.bind(this));

      // Check for updates on registration
      this.swRegistration.addEventListener('updatefound', () => {
        console.log('Service Worker update found');
        this.handleServiceWorkerUpdate();
      });

    } catch (error) {
      console.error('Service Worker registration failed:', error);
      throw error;
    }
  }

  /**
   * Handle service worker messages
   */
  private handleServiceWorkerMessage(event: MessageEvent): void {
    const { data } = event;
    
    if (data.type === 'BACKGROUND_SYNC') {
      // Handle background sync requests
      console.log('Background sync requested by service worker');
      window.dispatchEvent(new CustomEvent('sw-background-sync', { detail: data.payload }));
    }
  }

  /**
   * Handle service worker updates
   */
  private handleServiceWorkerUpdate(): void {
    if (!this.swRegistration) return;

    const newWorker = this.swRegistration.installing;
    if (!newWorker) return;

    newWorker.addEventListener('statechange', () => {
      if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
        // New version available
        this.updateAvailable = true;
        console.log('New version of the app is available');
        
        // Dispatch custom event for UI to handle
        window.dispatchEvent(new CustomEvent('sw-update-available'));
      }
    });
  }

  /**
   * Apply pending service worker update
   */
  async applyUpdate(): Promise<void> {
    if (!this.swRegistration || !this.updateAvailable) {
      console.log('No update available');
      return;
    }

    try {
      // Tell the waiting service worker to skip waiting
      if (this.swRegistration.waiting) {
        this.swRegistration.waiting.postMessage({ type: 'SKIP_WAITING' });
      }

      // Listen for the controlling service worker to change
      navigator.serviceWorker.addEventListener('controllerchange', () => {
        console.log('New service worker activated, reloading page');
        window.location.reload();
      });

    } catch (error) {
      console.error('Failed to apply update:', error);
    }
  }

  /**
   * Check if update is available
   */
  isUpdateAvailable(): boolean {
    return this.updateAvailable;
  }

  /**
   * Set up install prompt handling
   */
  private setupInstallPrompt(): void {
    window.addEventListener('beforeinstallprompt', (event) => {
      console.log('PWA install prompt available');
      
      // Prevent the default mini-infobar from appearing
      event.preventDefault();
      
      // Save the event for later use
      this.installPromptEvent = event as unknown as PWAInstallPrompt;
      
      // Dispatch custom event for UI to handle
      window.dispatchEvent(new CustomEvent('pwa-install-available'));
    });

    // Listen for successful installation
    window.addEventListener('appinstalled', () => {
      console.log('PWA installed successfully');
      this.installPromptEvent = null;
      window.dispatchEvent(new CustomEvent('pwa-installed'));
    });
  }

  /**
   * Show PWA install prompt
   */
  async showInstallPrompt(): Promise<'accepted' | 'dismissed' | 'unavailable'> {
    if (!this.installPromptEvent) {
      console.log('Install prompt not available');
      return 'unavailable';
    }

    try {
      // Show the install prompt
      await this.installPromptEvent.prompt();
      
      // Wait for user choice
      const choiceResult = await this.installPromptEvent.userChoice;
      
      console.log('Install prompt result:', choiceResult.outcome);
      
      if (choiceResult.outcome === 'accepted') {
        this.installPromptEvent = null;
      }
      
      return choiceResult.outcome;
    } catch (error) {
      console.error('Error showing install prompt:', error);
      return 'unavailable';
    }
  }

  /**
   * Check if PWA install prompt is available
   */
  isInstallPromptAvailable(): boolean {
    return this.installPromptEvent !== null;
  }

  /**
   * Check if app is running as PWA
   */
  isPWA(): boolean {
    if (typeof window === 'undefined') return false;
    
    return window.matchMedia('(display-mode: standalone)').matches ||
           (window.navigator as any).standalone === true;
  }

  /**
   * Set up push notifications
   */
  async setupPushNotifications(): Promise<boolean> {
    if (!this.swRegistration) {
      console.error('Service Worker not registered');
      return false;
    }

    if (!('PushManager' in window)) {
      console.warn('Push messaging not supported');
      return false;
    }

    try {
      // Request notification permission
      const permission = await Notification.requestPermission();
      
      if (permission !== 'granted') {
        console.log('Notification permission denied');
        return false;
      }

      console.log('Push notifications enabled');
      return true;
    } catch (error) {
      console.error('Error setting up push notifications:', error);
      return false;
    }
  }

  /**
   * Subscribe to push notifications
   */
  async subscribeToPush(applicationServerKey: string): Promise<PushSubscription | null> {
    if (!this.swRegistration) {
      console.error('Service Worker not registered');
      return null;
    }

    try {
      const subscription = await this.swRegistration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: this.urlB64ToUint8Array(applicationServerKey) as BufferSource
      });

      console.log('Push subscription successful:', subscription);
      return subscription;
    } catch (error) {
      console.error('Push subscription failed:', error);
      return null;
    }
  }

  /**
   * Get current push subscription
   */
  async getPushSubscription(): Promise<PushSubscription | null> {
    if (!this.swRegistration) {
      return null;
    }

    try {
      return await this.swRegistration.pushManager.getSubscription();
    } catch (error) {
      console.error('Error getting push subscription:', error);
      return null;
    }
  }

  /**
   * Unsubscribe from push notifications
   */
  async unsubscribeFromPush(): Promise<boolean> {
    try {
      const subscription = await this.getPushSubscription();
      if (subscription) {
        await subscription.unsubscribe();
        console.log('Unsubscribed from push notifications');
        return true;
      }
      return false;
    } catch (error) {
      console.error('Error unsubscribing from push:', error);
      return false;
    }
  }

  /**
   * Convert base64 URL to Uint8Array
   */
  private urlB64ToUint8Array(base64String: string): Uint8Array {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
      .replace(/-/g, '+')
      .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);

    for (let i = 0; i < rawData.length; ++i) {
      outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
  }

  /**
   * Register for background sync
   */
  async registerBackgroundSync(tag: string): Promise<boolean> {
    if (!this.swRegistration) {
      console.error('Service Worker not registered');
      return false;
    }

    if (!('sync' in window.ServiceWorkerRegistration.prototype)) {
      console.warn('Background sync not supported');
      return false;
    }

    try {
      await (this.swRegistration as any).sync.register(tag);
      console.log('Background sync registered:', tag);
      return true;
    } catch (error) {
      console.error('Background sync registration failed:', error);
      return false;
    }
  }

  /**
   * Get service worker registration
   */
  getRegistration(): ServiceWorkerRegistration | null {
    return this.swRegistration;
  }

  /**
   * Get app version from service worker
   */
  async getVersion(): Promise<string | null> {
    if (!this.swRegistration || !this.swRegistration.active) {
      return null;
    }

    return new Promise((resolve) => {
      const messageChannel = new MessageChannel();
      
      messageChannel.port1.onmessage = (event) => {
        resolve(event.data.version || null);
      };

      this.swRegistration!.active!.postMessage(
        { type: 'GET_VERSION' },
        [messageChannel.port2]
      );
      
      // Timeout after 5 seconds
      setTimeout(() => resolve(null), 5000);
    });
  }

  /**
   * Setup update detection
   */
  private setupUpdateDetection(): void {
    // Check for updates every 30 minutes
    setInterval(async () => {
      if (this.swRegistration) {
        try {
          await this.swRegistration.update();
        } catch (error) {
          console.error('Update check failed:', error);
        }
      }
    }, 30 * 60 * 1000);
  }
}

export const pwaManager = PWAManager.getInstance();