/**
 * Deferred Actions Manager for handling offline operations
 * Queues actions to be executed when connection is restored
 */

import { indexedDBManager } from './IndexedDBManager';
import { localStorageManager } from './LocalStorageManager';

export interface DeferredAction {
  id: string;
  type: 'api_call' | 'form_submission' | 'file_upload' | 'user_action';
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  data?: any;
  headers?: Record<string, string>;
  timestamp: number;
  retryCount: number;
  maxRetries: number;
  priority: 'low' | 'medium' | 'high';
  onSuccess?: string; // Callback identifier
  onError?: string; // Callback identifier
}

export interface ActionResult {
  success: boolean;
  response?: any;
  error?: string;
}

export class DeferredActionsManager {
  private static instance: DeferredActionsManager;
  private isProcessing = false;
  private readonly maxRetries = 3;
  private readonly retryDelays = [1000, 5000, 15000]; // Progressive delay
  private callbacks: Map<string, (result: ActionResult) => void> = new Map();

  static getInstance(): DeferredActionsManager {
    if (!DeferredActionsManager.instance) {
      DeferredActionsManager.instance = new DeferredActionsManager();
    }
    return DeferredActionsManager.instance;
  }

  /**
   * Add a deferred action to the queue
   */
  async addAction(
    type: DeferredAction['type'],
    endpoint: string,
    method: DeferredAction['method'],
    data?: any,
    options: {
      headers?: Record<string, string>;
      priority?: DeferredAction['priority'];
      maxRetries?: number;
      onSuccess?: (result: ActionResult) => void;
      onError?: (result: ActionResult) => void;
    } = {}
  ): Promise<string> {
    const actionId = `action_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    const action: DeferredAction = {
      id: actionId,
      type,
      endpoint,
      method,
      data,
      headers: options.headers,
      timestamp: Date.now(),
      retryCount: 0,
      maxRetries: options.maxRetries || this.maxRetries,
      priority: options.priority || 'medium',
      onSuccess: options.onSuccess ? actionId + '_success' : undefined,
      onError: options.onError ? actionId + '_error' : undefined
    };

    // Store callbacks
    if (options.onSuccess) {
      this.callbacks.set(actionId + '_success', options.onSuccess);
    }
    if (options.onError) {
      this.callbacks.set(actionId + '_error', options.onError);
    }

    try {
      await indexedDBManager.setItem('deferredActions', actionId, action);
    } catch (error) {
      // Fallback to localStorage for smaller actions
      console.warn('IndexedDB not available, falling back to localStorage');
      localStorageManager.setItem(`deferred_${actionId}`, action);
    }

    console.log(`Deferred action queued: ${type} ${method} ${endpoint}`);
    return actionId;
  }

  /**
   * Get all pending actions sorted by priority and timestamp
   */
  async getPendingActions(): Promise<DeferredAction[]> {
    let actions: DeferredAction[] = [];

    try {
      const indexedActions = await indexedDBManager.getAllItems<DeferredAction>('deferredActions');
      actions = indexedActions.map(item => item.data);
    } catch (error) {
      // Fallback to localStorage
      const keys = localStorageManager.getAllKeys();
      const deferredKeys = keys.filter(key => key.startsWith('deferred_'));
      
      actions = deferredKeys
        .map(key => localStorageManager.getItem<DeferredAction>(key))
        .filter((action): action is DeferredAction => action !== null);
    }

    // Sort by priority and timestamp
    const priorityOrder = { high: 3, medium: 2, low: 1 };
    return actions.sort((a, b) => {
      const priorityDiff = priorityOrder[b.priority] - priorityOrder[a.priority];
      if (priorityDiff !== 0) return priorityDiff;
      return a.timestamp - b.timestamp;
    });
  }

  /**
   * Execute a single deferred action
   */
  async executeAction(action: DeferredAction): Promise<ActionResult> {
    try {
      const response = await fetch(action.endpoint, {
        method: action.method,
        headers: {
          'Content-Type': 'application/json',
          ...action.headers
        },
        body: action.data ? JSON.stringify(action.data) : undefined
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();
      
      // Remove action from storage on success
      await this.removeAction(action.id);

      // Execute success callback
      if (action.onSuccess && this.callbacks.has(action.onSuccess)) {
        const callback = this.callbacks.get(action.onSuccess)!;
        callback({ success: true, response: result });
        this.callbacks.delete(action.onSuccess);
      }

      return { success: true, response: result };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      
      // Increment retry count
      action.retryCount++;

      if (action.retryCount >= action.maxRetries) {
        // Max retries reached, remove action and call error callback
        await this.removeAction(action.id);

        if (action.onError && this.callbacks.has(action.onError)) {
          const callback = this.callbacks.get(action.onError)!;
          callback({ success: false, error: errorMessage });
          this.callbacks.delete(action.onError);
        }

        return { success: false, error: `Max retries reached: ${errorMessage}` };
      } else {
        // Update action with new retry count
        try {
          await indexedDBManager.setItem('deferredActions', action.id, action);
        } catch {
          localStorageManager.setItem(`deferred_${action.id}`, action);
        }

        return { success: false, error: errorMessage };
      }
    }
  }

  /**
   * Process all pending actions
   */
  async processActions(): Promise<{ processed: number; successful: number; failed: number }> {
    if (this.isProcessing) {
      console.log('Actions already being processed');
      return { processed: 0, successful: 0, failed: 0 };
    }

    this.isProcessing = true;
    const actions = await this.getPendingActions();
    let successful = 0;
    let failed = 0;

    console.log(`Processing ${actions.length} deferred actions`);

    for (const action of actions) {
      try {
        const result = await this.executeAction(action);
        if (result.success) {
          successful++;
          console.log(`✓ Successfully executed: ${action.type} ${action.method} ${action.endpoint}`);
        } else {
          failed++;
          console.warn(`✗ Failed to execute: ${action.type} ${action.method} ${action.endpoint} - ${result.error}`);
          
          // Add delay before next retry if action will be retried
          if (action.retryCount < action.maxRetries) {
            const delay = this.retryDelays[Math.min(action.retryCount - 1, this.retryDelays.length - 1)];
            await new Promise(resolve => setTimeout(resolve, delay));
          }
        }
      } catch (error) {
        failed++;
        console.error(`Error processing action ${action.id}:`, error);
      }
    }

    this.isProcessing = false;
    
    const result = { processed: actions.length, successful, failed };
    console.log(`Action processing complete:`, result);
    
    return result;
  }

  /**
   * Remove a specific action from storage
   */
  private async removeAction(actionId: string): Promise<void> {
    try {
      await indexedDBManager.removeItem('deferredActions', actionId);
    } catch {
      localStorageManager.removeItem(`deferred_${actionId}`);
    }

    // Clean up any remaining callbacks
    this.callbacks.delete(actionId + '_success');
    this.callbacks.delete(actionId + '_error');
  }

  /**
   * Clear all pending actions
   */
  async clearActions(): Promise<void> {
    try {
      await indexedDBManager.clearStore('deferredActions');
    } catch {
      const keys = localStorageManager.getAllKeys();
      const deferredKeys = keys.filter(key => key.startsWith('deferred_'));
      deferredKeys.forEach(key => localStorageManager.removeItem(key));
    }

    this.callbacks.clear();
    console.log('All deferred actions cleared');
  }

  /**
   * Get action statistics
   */
  async getStats(): Promise<{
    total: number;
    byType: Record<string, number>;
    byPriority: Record<string, number>;
    oldestAction?: Date;
  }> {
    const actions = await this.getPendingActions();
    
    const byType: Record<string, number> = {};
    const byPriority: Record<string, number> = {};
    let oldestTimestamp = Date.now();

    actions.forEach(action => {
      byType[action.type] = (byType[action.type] || 0) + 1;
      byPriority[action.priority] = (byPriority[action.priority] || 0) + 1;
      oldestTimestamp = Math.min(oldestTimestamp, action.timestamp);
    });

    return {
      total: actions.length,
      byType,
      byPriority,
      oldestAction: actions.length > 0 ? new Date(oldestTimestamp) : undefined
    };
  }
}

export const deferredActionsManager = DeferredActionsManager.getInstance();