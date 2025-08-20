/**
 * useWebSocket hook for real-time connection management
 * Provides React integration for WebSocket functionality
 */

import { useEffect, useState, useCallback, useRef } from 'react';
import { 
  WebSocketManager, 
  WebSocketConfig, 
  WebSocketMessage, 
  WebSocketEventHandler,
  WebSocketConnectionHandler,
  createWebSocketManager,
  getWebSocketManager
} from '@/lib/websocket';
import { logger } from '@/lib/logger';

export interface UseWebSocketOptions extends Partial<WebSocketConfig> {
  autoConnect?: boolean;
  onMessage?: (message: WebSocketMessage) => void;
  onOpen?: () => void;
  onClose?: (code: number, reason: string) => void;
  onError?: (error: Event) => void;
  onReconnecting?: (attempt: number) => void;
  onReconnected?: () => void;
  onMaxReconnectAttemptsReached?: () => void;
}

export interface UseWebSocketReturn {
  // Connection state
  isConnected: boolean;
  isConnecting: boolean;
  reconnectAttempts: number;
  queuedMessages: number;
  
  // Actions
  connect: () => Promise<void>;
  disconnect: () => void;
  send: (message: WebSocketMessage) => boolean;
  clearQueue: () => void;
  
  // Event subscription
  subscribe: (messageType: string, handler: WebSocketEventHandler) => () => void;
  
  // Connection status
  getStatus: () => {
    connected: boolean;
    connecting: boolean;
    readyState: number | null;
    reconnectAttempts: number;
    queuedMessages: number;
  };
}

export const useWebSocket = (
  url: string,
  options: UseWebSocketOptions = {}
): UseWebSocketReturn => {
  const {
    autoConnect = false,
    onMessage,
    onOpen,
    onClose,
    onError,
    onReconnecting,
    onReconnected,
    onMaxReconnectAttemptsReached,
    ...config
  } = options;

  // State
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);
  const [queuedMessages, setQueuedMessages] = useState(0);

  // Refs for stable references
  const managerRef = useRef<WebSocketManager | null>(null);
  const handlersRef = useRef<Map<string, Set<WebSocketEventHandler>>>(new Map());

  // Initialize WebSocket manager
  useEffect(() => {
    const wsConfig: WebSocketConfig = {
      url,
      ...config,
    };

    managerRef.current = createWebSocketManager(wsConfig);

    // Set up connection handlers
    const connectionHandlers: WebSocketConnectionHandler = {
      onOpen: () => {
        setIsConnected(true);
        setIsConnecting(false);
        setReconnectAttempts(0);
        onOpen?.();
        
        logger.debug('WebSocket connected in hook', {}, 'websocket-hook');
      },
      
      onClose: (code, reason) => {
        setIsConnected(false);
        setIsConnecting(false);
        onClose?.(code, reason);
        
        logger.debug('WebSocket closed in hook', { code, reason }, 'websocket-hook');
      },
      
      onError: (error) => {
        setIsConnecting(false);
        onError?.(error);
        
        logger.debug('WebSocket error in hook', { error }, 'websocket-hook');
      },
      
      onReconnecting: (attempt) => {
        setIsConnecting(true);
        setReconnectAttempts(attempt);
        onReconnecting?.(attempt);
        
        logger.debug('WebSocket reconnecting in hook', { attempt }, 'websocket-hook');
      },
      
      onReconnected: () => {
        setIsConnected(true);
        setIsConnecting(false);
        onReconnected?.();
        
        logger.debug('WebSocket reconnected in hook', {}, 'websocket-hook');
      },
      
      onMaxReconnectAttemptsReached: () => {
        setIsConnecting(false);
        onMaxReconnectAttemptsReached?.();
        
        logger.debug('WebSocket max reconnect attempts reached in hook', {}, 'websocket-hook');
      },
    };

    managerRef.current.setConnectionHandlers(connectionHandlers);

    // Set up global message handler if provided
    if (onMessage) {
      managerRef.current.on('*', onMessage);
    }

    // Auto-connect if requested
    if (autoConnect) {
      managerRef.current.connect().catch(error => {
        logger.error('Auto-connect failed in WebSocket hook', {
          error: error instanceof Error ? error.message : 'Unknown error'
        }, 'websocket-hook');
      });
    }

    // Status update interval
    const statusInterval = setInterval(() => {
      if (managerRef.current) {
        const status = managerRef.current.getConnectionStatus();
        setIsConnected(status.connected);
        setIsConnecting(status.connecting);
        setReconnectAttempts(status.reconnectAttempts);
        setQueuedMessages(status.queuedMessages);
      }
    }, 1000);

    return () => {
      clearInterval(statusInterval);
      
      // Clean up handlers
      if (managerRef.current && onMessage) {
        managerRef.current.off('*', onMessage);
      }
      
      // Disconnect on unmount
      managerRef.current?.disconnect();
    };
  }, [url, autoConnect]); // Re-initialize if URL changes

  // Connect function
  const connect = useCallback(async (): Promise<void> => {
    if (!managerRef.current) {
      throw new Error('WebSocket manager not initialized');
    }

    setIsConnecting(true);
    
    try {
      await managerRef.current.connect();
      logger.info('Connected via WebSocket hook', {}, 'websocket-hook');
    } catch (error) {
      setIsConnecting(false);
      logger.error('Connection failed in WebSocket hook', {
        error: error instanceof Error ? error.message : 'Unknown error'
      }, 'websocket-hook');
      throw error;
    }
  }, []);

  // Disconnect function
  const disconnect = useCallback((): void => {
    if (!managerRef.current) {
      return;
    }

    managerRef.current.disconnect();
    setIsConnected(false);
    setIsConnecting(false);
    setReconnectAttempts(0);
    
    logger.info('Disconnected via WebSocket hook', {}, 'websocket-hook');
  }, []);

  // Send message function
  const send = useCallback((message: WebSocketMessage): boolean => {
    if (!managerRef.current) {
      logger.warn('Attempted to send message but WebSocket manager not initialized', {
        messageType: message.type
      }, 'websocket-hook');
      return false;
    }

    const success = managerRef.current.send(message);
    
    if (success) {
      logger.debug('Message sent via WebSocket hook', {
        type: message.type,
        id: message.id
      }, 'websocket-hook');
    } else {
      logger.debug('Message queued via WebSocket hook', {
        type: message.type,
        id: message.id
      }, 'websocket-hook');
    }
    
    return success;
  }, []);

  // Clear message queue function
  const clearQueue = useCallback((): void => {
    if (!managerRef.current) {
      return;
    }

    managerRef.current.clearMessageQueue();
    setQueuedMessages(0);
    
    logger.info('Message queue cleared via WebSocket hook', {}, 'websocket-hook');
  }, []);

  // Subscribe to message type
  const subscribe = useCallback((
    messageType: string, 
    handler: WebSocketEventHandler
  ): (() => void) => {
    if (!managerRef.current) {
      logger.warn('Attempted to subscribe but WebSocket manager not initialized', {
        messageType
      }, 'websocket-hook');
      return () => {};
    }

    // Register handler with manager
    managerRef.current.on(messageType, handler);

    // Track handler for cleanup
    if (!handlersRef.current.has(messageType)) {
      handlersRef.current.set(messageType, new Set());
    }
    handlersRef.current.get(messageType)!.add(handler);

    logger.debug('Subscribed to message type via WebSocket hook', {
      messageType,
      totalHandlers: handlersRef.current.get(messageType)!.size
    }, 'websocket-hook');

    // Return unsubscribe function
    return () => {
      if (managerRef.current) {
        managerRef.current.off(messageType, handler);
      }
      
      const handlers = handlersRef.current.get(messageType);
      if (handlers) {
        handlers.delete(handler);
        if (handlers.size === 0) {
          handlersRef.current.delete(messageType);
        }
      }
      
      logger.debug('Unsubscribed from message type via WebSocket hook', {
        messageType
      }, 'websocket-hook');
    };
  }, []);

  // Get connection status
  const getStatus = useCallback(() => {
    if (!managerRef.current) {
      return {
        connected: false,
        connecting: false,
        readyState: null,
        reconnectAttempts: 0,
        queuedMessages: 0,
      };
    }

    return managerRef.current.getConnectionStatus();
  }, []);

  return {
    // State
    isConnected,
    isConnecting,
    reconnectAttempts,
    queuedMessages,
    
    // Actions
    connect,
    disconnect,
    send,
    clearQueue,
    
    // Event subscription
    subscribe,
    
    // Status
    getStatus,
  };
};

/**
 * Hook for subscribing to specific WebSocket message types
 */
export const useWebSocketSubscription = (
  messageType: string,
  handler: WebSocketEventHandler,
  dependencies: React.DependencyList = []
): void => {
  useEffect(() => {
    const manager = getWebSocketManager();
    
    if (!manager) {
      logger.warn('No WebSocket manager available for subscription', {
        messageType
      }, 'websocket-hook');
      return;
    }

    manager.on(messageType, handler);
    
    logger.debug('WebSocket subscription established', {
      messageType
    }, 'websocket-hook');

    return () => {
      manager.off(messageType, handler);
      
      logger.debug('WebSocket subscription cleaned up', {
        messageType
      }, 'websocket-hook');
    };
  }, [messageType, ...dependencies]);
};

/**
 * Hook for WebSocket connection status only
 */
export const useWebSocketStatus = (): {
  isConnected: boolean;
  isConnecting: boolean;
  reconnectAttempts: number;
  queuedMessages: number;
} => {
  const [status, setStatus] = useState({
    isConnected: false,
    isConnecting: false,
    reconnectAttempts: 0,
    queuedMessages: 0,
  });

  useEffect(() => {
    const updateStatus = () => {
      const manager = getWebSocketManager();
      
      if (manager) {
        const currentStatus = manager.getConnectionStatus();
        setStatus({
          isConnected: currentStatus.connected,
          isConnecting: currentStatus.connecting,
          reconnectAttempts: currentStatus.reconnectAttempts,
          queuedMessages: currentStatus.queuedMessages,
        });
      }
    };

    // Update immediately
    updateStatus();

    // Update periodically
    const interval = setInterval(updateStatus, 1000);

    return () => clearInterval(interval);
  }, []);

  return status;
};