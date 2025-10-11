// hooks/useWebSocket.ts
'use client';

import { useEffect, useState, useCallback, useRef } from 'react';

export interface AgentMessage {
  type: string;
  timestamp: string;
  data: Record<string, any>;
}

export function useWebSocket(url: string) {
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<AgentMessage[]>([]);
  const socketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url);

      ws.onopen = () => {
        console.log('🟢 WebSocket connected');
        setIsConnected(true);
        socketRef.current = ws;

        // Send subscribe message
        ws.send(JSON.stringify({ type: 'subscribe' }));
      };

      ws.onmessage = (event) => {
        try {
          const message: AgentMessage = JSON.parse(event.data);
          console.log('📨 Message received:', message.type);
          setMessages((prev) => [...prev, message]);
        } catch (error) {
          console.error('Failed to parse message:', error);
        }
      };

      ws.onclose = () => {
        console.log('🔴 WebSocket disconnected');
        setIsConnected(false);
        socketRef.current = null;

        // Attempt to reconnect after 3 seconds
        reconnectTimeoutRef.current = setTimeout(() => {
          console.log('🔄 Attempting to reconnect...');
          connect();
        }, 3000);
      };

      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
      };

      socketRef.current = ws;
    } catch (error) {
      console.error('Failed to create WebSocket:', error);
    }
  }, [url]);

  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, [connect]);

  const sendMessage = useCallback((message: any) => {
    if (socketRef.current && isConnected) {
      socketRef.current.send(JSON.stringify(message));
    } else {
      console.warn('Cannot send message: WebSocket not connected');
    }
  }, [isConnected]);

  const clearMessages = useCallback(() => {
    setMessages([]);
  }, []);

  return { isConnected, messages, sendMessage, clearMessages };
}
