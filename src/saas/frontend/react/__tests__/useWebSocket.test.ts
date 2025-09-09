/**
 * WebSocket Hook Tests
 * 
 * Unit tests for the useWebSocket hook.
 */

import { renderHook, act } from '@testing-library/react';
import { useWebSocket, useDashboardWebSocket, useUsageTrackingWebSocket, useBillingWebSocket } from '../hooks/useWebSocket';

// Mock WebSocket
const mockWebSocket = {
  close: jest.fn(),
  send: jest.fn(),
  addEventListener: jest.fn(),
  removeEventListener: jest.fn(),
  readyState: WebSocket.OPEN
};

// Mock global WebSocket
global.WebSocket = jest.fn(() => mockWebSocket) as any;

// ============================================================================
// TESTS
// ============================================================================

describe('useWebSocket Hook', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    (global.WebSocket as jest.Mock).mockImplementation(() => mockWebSocket);
  });

  it('initializes with disconnected state', () => {
    const { result } = renderHook(() => useWebSocket('/ws/test'));
    
    expect(result.current.isConnected).toBe(false);
    expect(result.current.lastMessage).toBeNull();
  });

  it('connects to WebSocket on mount', () => {
    renderHook(() => useWebSocket('/ws/test'));
    
    expect(global.WebSocket).toHaveBeenCalledWith('ws://localhost/ws/test');
  });

  it('calls onOpen when WebSocket opens', () => {
    const onOpen = jest.fn();
    renderHook(() => useWebSocket('/ws/test', { onOpen }));
    
    // Simulate WebSocket open event
    const openHandler = mockWebSocket.addEventListener.mock.calls.find(
      call => call[0] === 'open'
    )?.[1];
    
    if (openHandler) {
      act(() => {
        openHandler();
      });
    }
    
    expect(onOpen).toHaveBeenCalled();
  });

  it('calls onClose when WebSocket closes', () => {
    const onClose = jest.fn();
    renderHook(() => useWebSocket('/ws/test', { onClose }));
    
    // Simulate WebSocket close event
    const closeHandler = mockWebSocket.addEventListener.mock.calls.find(
      call => call[0] === 'close'
    )?.[1];
    
    if (closeHandler) {
      act(() => {
        closeHandler();
      });
    }
    
    expect(onClose).toHaveBeenCalled();
  });

  it('calls onError when WebSocket errors', () => {
    const onError = jest.fn();
    renderHook(() => useWebSocket('/ws/test', { onError }));
    
    // Simulate WebSocket error event
    const errorHandler = mockWebSocket.addEventListener.mock.calls.find(
      call => call[0] === 'error'
    )?.[1];
    
    if (errorHandler) {
      act(() => {
        errorHandler();
      });
    }
    
    expect(onError).toHaveBeenCalled();
  });

  it('calls onMessage when WebSocket receives message', () => {
    const onMessage = jest.fn();
    const { result } = renderHook(() => useWebSocket('/ws/test', { onMessage }));
    
    // Simulate WebSocket message event
    const messageHandler = mockWebSocket.addEventListener.mock.calls.find(
      call => call[0] === 'message'
    )?.[1];
    
    const testMessage = { data: JSON.stringify({ type: 'test', data: 'test' }) };
    
    if (messageHandler) {
      act(() => {
        messageHandler(testMessage);
      });
    }
    
    expect(onMessage).toHaveBeenCalledWith({ type: 'test', data: 'test' });
    expect(result.current.lastMessage).toEqual({ type: 'test', data: 'test' });
  });

  it('sends message through WebSocket', () => {
    const { result } = renderHook(() => useWebSocket('/ws/test'));
    
    act(() => {
      result.current.sendMessage({ type: 'test', data: 'test' });
    });
    
    expect(mockWebSocket.send).toHaveBeenCalledWith(JSON.stringify({ type: 'test', data: 'test' }));
  });

  it('disconnects WebSocket on unmount', () => {
    const { unmount } = renderHook(() => useWebSocket('/ws/test'));
    
    unmount();
    
    expect(mockWebSocket.close).toHaveBeenCalled();
  });

  it('reconnects when connection is lost', () => {
    const { result } = renderHook(() => useWebSocket('/ws/test', { maxReconnectAttempts: 3 }));
    
    // Simulate WebSocket close event
    const closeHandler = mockWebSocket.addEventListener.mock.calls.find(
      call => call[0] === 'close'
    )?.[1];
    
    if (closeHandler) {
      act(() => {
        closeHandler();
      });
    }
    
    // Should attempt to reconnect
    expect(global.WebSocket).toHaveBeenCalledTimes(2);
  });
});

describe('useDashboardWebSocket Hook', () => {
  it('subscribes to dashboard updates', () => {
    const { result } = renderHook(() => useDashboardWebSocket('tenant-1'));
    
    expect(result.current.isConnected).toBe(false);
    expect(result.current.dashboardUpdates).toBeNull();
  });
});

describe('useUsageTrackingWebSocket Hook', () => {
  it('subscribes to usage updates', () => {
    const { result } = renderHook(() => useUsageTrackingWebSocket('tenant-1'));
    
    expect(result.current.isConnected).toBe(false);
    expect(result.current.usageUpdates).toBeNull();
  });
});

describe('useBillingWebSocket Hook', () => {
  it('subscribes to billing updates', () => {
    const { result } = renderHook(() => useBillingWebSocket('tenant-1'));
    
    expect(result.current.isConnected).toBe(false);
    expect(result.current.billingUpdates).toBeNull();
  });
});
