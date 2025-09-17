/**
 * WebSocket Hook for Real-time Updates
 * 
 * This hook provides WebSocket connectivity for real-time dashboard updates.
 */

import { useState, useEffect, useRef, useCallback } from 'react';

// ============================================================================
// INTERFACES
// ============================================================================

interface WebSocketMessage {
  type: string;
  data: any;
  timestamp: string;
}

interface UseWebSocketOptions {
  reconnectInterval?: number;
  maxReconnectAttempts?: number;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
  onMessage?: (message: WebSocketMessage) => void;
}

interface UseWebSocketReturn {
  isConnected: boolean;
  lastMessage: WebSocketMessage | null;
  sendMessage: (message: any) => void;
  reconnect: () => void;
  disconnect: () => void;
}

// ============================================================================
// HOOK IMPLEMENTATION
// ============================================================================

export const useWebSocket = (
  url: string,
  options: UseWebSocketOptions = {}
): UseWebSocketReturn => {
  const {
    reconnectInterval = 5000,
    maxReconnectAttempts = 5,
    onOpen,
    onClose,
    onError,
    onMessage
  } = options;

  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttemptsRef = useRef(0);
  const shouldReconnectRef = useRef(true);

  // Get WebSocket URL
  const getWebSocketUrl = useCallback(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.host;
    return `${protocol}//${host}${url}`;
  }, [url]);

  // Connect to WebSocket
  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    try {
      const wsUrl = getWebSocketUrl();
      wsRef.current = new WebSocket(wsUrl);

      wsRef.current.onopen = () => {
        setIsConnected(true);
        reconnectAttemptsRef.current = 0;
        onOpen?.();
      };

      wsRef.current.onclose = (event) => {
        setIsConnected(false);
        onClose?.();

        // Attempt to reconnect if not manually closed
        if (shouldReconnectRef.current && reconnectAttemptsRef.current < maxReconnectAttempts) {
          reconnectAttemptsRef.current++;
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, reconnectInterval);
        }
      };

      wsRef.current.onerror = (error) => {
        onError?.(error);
      };

      wsRef.current.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          setLastMessage(message);
          onMessage?.(message);
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error);
        }
      };
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error);
    }
  }, [getWebSocketUrl, reconnectInterval, maxReconnectAttempts, onOpen, onClose, onError, onMessage]);

  // Disconnect from WebSocket
  const disconnect = useCallback(() => {
    shouldReconnectRef.current = false;
    
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
      reconnectTimeoutRef.current = null;
    }

    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    
    setIsConnected(false);
  }, []);

  // Reconnect to WebSocket
  const reconnect = useCallback(() => {
    disconnect();
    shouldReconnectRef.current = true;
    reconnectAttemptsRef.current = 0;
    connect();
  }, [disconnect, connect]);

  // Send message through WebSocket
  const sendMessage = useCallback((message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected. Cannot send message.');
    }
  }, []);

  // Initialize connection
  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  return {
    isConnected,
    lastMessage,
    sendMessage,
    reconnect,
    disconnect
  };
};

// ============================================================================
// UTILITY HOOKS
// ============================================================================

/**
 * Hook for dashboard-specific WebSocket updates
 */
export const useDashboardWebSocket = (tenantId?: string) => {
  const [dashboardUpdates, setDashboardUpdates] = useState<any>(null);

  const { isConnected, lastMessage, sendMessage } = useWebSocket('/ws/dashboard', {
    onMessage: (message) => {
      if (message.type === 'dashboard_update') {
        setDashboardUpdates(message.data);
      }
    }
  });

  // Send tenant-specific subscription
  useEffect(() => {
    if (isConnected && tenantId) {
      sendMessage({
        type: 'subscribe',
        data: { tenant_id: tenantId }
      });
    }
  }, [isConnected, tenantId, sendMessage]);

  return {
    isConnected,
    dashboardUpdates,
    lastMessage
  };
};

/**
 * Hook for usage tracking WebSocket updates
 */
export const useUsageTrackingWebSocket = (tenantId?: string) => {
  const [usageUpdates, setUsageUpdates] = useState<any>(null);

  const { isConnected, lastMessage, sendMessage } = useWebSocket('/ws/usage', {
    onMessage: (message) => {
      if (message.type === 'usage_update') {
        setUsageUpdates(message.data);
      }
    }
  });

  // Send tenant-specific subscription
  useEffect(() => {
    if (isConnected && tenantId) {
      sendMessage({
        type: 'subscribe',
        data: { tenant_id: tenantId }
      });
    }
  }, [isConnected, tenantId, sendMessage]);

  return {
    isConnected,
    usageUpdates,
    lastMessage
  };
};

/**
 * Hook for billing WebSocket updates
 */
export const useBillingWebSocket = (tenantId?: string) => {
  const [billingUpdates, setBillingUpdates] = useState<any>(null);

  const { isConnected, lastMessage, sendMessage } = useWebSocket('/ws/billing', {
    onMessage: (message) => {
      if (message.type === 'billing_update') {
        setBillingUpdates(message.data);
      }
    }
  });

  // Send tenant-specific subscription
  useEffect(() => {
    if (isConnected && tenantId) {
      sendMessage({
        type: 'subscribe',
        data: { tenant_id: tenantId }
      });
    }
  }, [isConnected, tenantId, sendMessage]);

  return {
    isConnected,
    billingUpdates,
    lastMessage
  };
};
