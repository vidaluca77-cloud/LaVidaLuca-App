'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { 
  createWebSocketManager, 
  getWebSocketManager,
  type WebSocketStatus, 
  type WebSocketMessage, 
  type WebSocketConfig,
  type WebSocketListener 
} from '@/lib/websocket';
import { logger } from '@/lib/logger';

export interface UseWebSocketReturn {
  status: WebSocketStatus;
  lastMessage: WebSocketMessage | null;
  connectionTime: Date | null;
  isConnected: boolean;
  error: string | null;
  
  // Actions
  connect: () => void;
  disconnect: () => void;
  sendMessage: (message: WebSocketMessage) => boolean;
  
  // Message handling
  subscribe: (type: string, handler: (payload: any) => void) => () => void;
}

interface UseWebSocketOptions {
  autoConnect?: boolean;
  url?: string;
  protocols?: string[];
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
}

/**
 * Hook for WebSocket connection management and real-time messaging
 */
export const useWebSocket = (options: UseWebSocketOptions = {}): UseWebSocketReturn => {
  const {
    autoConnect = true,
    url = process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:8001/ws',
    protocols,
    reconnectInterval = 5000,
    maxReconnectAttempts = 10,
  } = options;

  const [status, setStatus] = useState<WebSocketStatus>('disconnected');
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const [connectionTime, setConnectionTime] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  const messageHandlersRef = useRef<Map<string, ((payload: any) => void)[]>>(new Map());
  const wsManagerRef = useRef<ReturnType<typeof createWebSocketManager> | null>(null);

  // Initialize WebSocket manager
  useEffect(() => {
    try {
      const config: WebSocketConfig = {
        url,
        protocols,
        reconnectInterval,
        maxReconnectAttempts,
      };

      wsManagerRef.current = createWebSocketManager(config);
      
      // Subscribe to WebSocket events
      const unsubscribe = wsManagerRef.current.subscribe({
        onStatusChange: (newStatus) => {
          setStatus(newStatus);
          
          if (newStatus === 'connected') {
            setConnectionTime(new Date());
            setError(null);
          } else if (newStatus === 'error') {
            setError('Erreur de connexion WebSocket');
          }
        },
        
        onMessage: (message) => {
          setLastMessage(message);
          
          // Handle typed message handlers
          const handlers = messageHandlersRef.current.get(message.type);
          if (handlers) {
            handlers.forEach(handler => {
              try {
                handler(message.payload);
              } catch (error) {
                logger.error('Error in WebSocket message handler', { error, messageType: message.type });
              }
            });
          }
        },
        
        onError: (event) => {
          setError('Erreur de connexion WebSocket');
          logger.error('WebSocket error in hook', { event });
        },
      });

      // Auto-connect if enabled
      if (autoConnect) {
        wsManagerRef.current.connect();
      }

      return unsubscribe;
    } catch (err) {
      logger.error('Error initializing WebSocket hook', { error: err });
      setError('Erreur d\'initialisation WebSocket');
    }
  }, [url, protocols, reconnectInterval, maxReconnectAttempts, autoConnect]);

  // Connect function
  const connect = useCallback(() => {
    if (wsManagerRef.current) {
      wsManagerRef.current.connect();
    }
  }, []);

  // Disconnect function
  const disconnect = useCallback(() => {
    if (wsManagerRef.current) {
      wsManagerRef.current.disconnect();
      setConnectionTime(null);
    }
  }, []);

  // Send message function
  const sendMessage = useCallback((message: WebSocketMessage): boolean => {
    if (wsManagerRef.current) {
      return wsManagerRef.current.send(message);
    }
    return false;
  }, []);

  // Subscribe to specific message types
  const subscribe = useCallback((type: string, handler: (payload: any) => void): () => void => {
    const handlers = messageHandlersRef.current.get(type) || [];
    handlers.push(handler);
    messageHandlersRef.current.set(type, handlers);

    // Return unsubscribe function
    return () => {
      const currentHandlers = messageHandlersRef.current.get(type) || [];
      const index = currentHandlers.indexOf(handler);
      if (index > -1) {
        currentHandlers.splice(index, 1);
        if (currentHandlers.length === 0) {
          messageHandlersRef.current.delete(type);
        } else {
          messageHandlersRef.current.set(type, currentHandlers);
        }
      }
    };
  }, []);

  const isConnected = status === 'connected';

  return {
    status,
    lastMessage,
    connectionTime,
    isConnected,
    error,
    
    // Actions
    connect,
    disconnect,
    sendMessage,
    
    // Message handling
    subscribe,
  };
};

/**
 * Hook for simplified WebSocket messaging without connection management
 */
export const useWebSocketMessage = (messageType: string) => {
  const [messages, setMessages] = useState<any[]>([]);
  const [lastMessage, setLastMessage] = useState<any>(null);

  useEffect(() => {
    try {
      const wsManager = getWebSocketManager();
      
      const unsubscribe = wsManager.subscribe({
        onMessage: (message) => {
          if (message.type === messageType) {
            setLastMessage(message.payload);
            setMessages(prev => [...prev.slice(-49), message.payload]); // Keep last 50 messages
          }
        },
      });

      return unsubscribe;
    } catch (error) {
      logger.error('Error in useWebSocketMessage hook', { error, messageType });
    }
  }, [messageType]);

  const sendMessage = useCallback((payload: any) => {
    try {
      const wsManager = getWebSocketManager();
      return wsManager.send({
        type: messageType,
        payload,
      });
    } catch (error) {
      logger.error('Error sending WebSocket message', { error, messageType });
      return false;
    }
  }, [messageType]);

  return {
    messages,
    lastMessage,
    sendMessage,
  };
};

/**
 * Hook for real-time collaborative features
 */
export const useRealTimeCollaboration = (roomId: string) => {
  const { sendMessage, subscribe } = useWebSocket();
  const [participants, setParticipants] = useState<string[]>([]);
  const [activity, setActivity] = useState<any[]>([]);

  useEffect(() => {
    // Join room
    sendMessage({
      type: 'join_room',
      payload: { roomId },
    });

    // Subscribe to room events
    const unsubscribeParticipants = subscribe('room_participants', (payload) => {
      setParticipants(payload.participants || []);
    });

    const unsubscribeActivity = subscribe('room_activity', (payload) => {
      setActivity(prev => [...prev.slice(-19), payload]); // Keep last 20 activities
    });

    // Leave room on cleanup
    return () => {
      sendMessage({
        type: 'leave_room',
        payload: { roomId },
      });
      unsubscribeParticipants();
      unsubscribeActivity();
    };
  }, [roomId, sendMessage, subscribe]);

  const broadcastActivity = useCallback((action: string, data: any) => {
    sendMessage({
      type: 'room_activity',
      payload: {
        roomId,
        action,
        data,
        timestamp: new Date().toISOString(),
      },
    });
  }, [roomId, sendMessage]);

  return {
    participants,
    activity,
    broadcastActivity,
  };
};