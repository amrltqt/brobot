import { useEffect, useRef, useCallback, useState } from 'react';

// Type for WebSocket ready state
export type ReadyState = 'CONNECTING' | 'OPEN' | 'CLOSING' | 'CLOSED';

// Options for the hook
export interface UseResilientWebSocketOptions {
    /** Callback when a message is received */
    onMessage?: (data: string) => void;
    /** Optional protocols string or array */
    protocols?: string | string[];
}

/**
 * React hook establishing a resilient WebSocket connection with:
 * - Auto-reconnect with exponential back-off
 * - Outgoing message queue when disconnected
 * - Heartbeat ping to keep connection alive
 * 
 * @param url WebSocket URL
 * @param options Configuration callbacks and protocols
 * @returns { send, readyState }
 */
export function useWebsocket(
    url: string,
    { onMessage, protocols }: UseResilientWebSocketOptions = {}
) {
    const socketRef = useRef<WebSocket | null>(null);
    const queueRef = useRef<string[]>([]);
    const attemptsRef = useRef<number>(0);
    const heartbeatRef = useRef<number | null>(null);
    const [readyState, setReadyState] = useState<ReadyState>('CONNECTING');

    // Cleanup socket and heartbeat
    const cleanup = useCallback(() => {
        if (heartbeatRef.current !== null) {
            clearInterval(heartbeatRef.current);
            heartbeatRef.current = null;
        }
        try {
            socketRef.current?.close();
        } catch {
            /* ignored */
        }
        socketRef.current = null;
    }, []);

    // Establish connection and handlers
    const connect = useCallback(() => {
        const ws = new WebSocket(url, protocols);
        socketRef.current = ws;
        setReadyState('CONNECTING');

        ws.onopen = () => {
            setReadyState('OPEN');
            attemptsRef.current = 0;
            // Heartbeat every 25s to keep proxies alive
            heartbeatRef.current = window.setInterval(() => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(''); // empty ping or JSON.stringify({ type: 'ping' })
                }
            }, 25000);
            // Flush queued messages
            queueRef.current.forEach(msg => ws.send(msg));
            queueRef.current = [];
        };

        ws.onmessage = event => {
            onMessage?.(event.data);
        };

        ws.onclose = () => {
            setReadyState('CLOSED');
            cleanup();
            // Schedule reconnect with exponential back-off
            const delay = Math.min(1000 * 2 ** attemptsRef.current, 30000);
            attemptsRef.current += 1;
            setTimeout(connect, delay);
        };

        ws.onerror = () => {
            // Let onclose handle reconnection
        };
    }, [url, protocols, onMessage, cleanup]);

    // Initialize on mount and cleanup on unmount
    useEffect(() => {
        connect();
        return () => {
            cleanup();
        };
    }, [connect, cleanup]);

    /**
     * Send a message or enqueue if not open
     * @param message stringified payload
     */
    const send = useCallback((message: string) => {
        const ws = socketRef.current;
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(message);
        } else {
            queueRef.current.push(message);
        }
    }, []);

    return { send, readyState };
}