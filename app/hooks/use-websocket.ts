import { useEffect, useRef, useState, useCallback } from "react";

const WS_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws/";

export function useWebSocket(
    url: string = WS_URL,
    onMessageCallback?: (message: any) => void,
    onReconnectCallback?: () => void,
    onErrorCallback?: (error: any) => void
) {
    const [isConnected, setIsConnected] = useState<boolean>(false);
    const wsRef = useRef<WebSocket | null>(null);
    const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
    const reconnectAttemptsRef = useRef<number>(0);

    const connect = useCallback(() => {
        const ws = new WebSocket(url);
        wsRef.current = ws;

        ws.onopen = () => {
            console.log("WebSocket connecté");
            setIsConnected(true);
            reconnectAttemptsRef.current = 0;
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
                reconnectTimeoutRef.current = null;
            }

            if (onReconnectCallback) {
                onReconnectCallback();
            }
        };

        ws.onmessage = (event) => {
            if (onMessageCallback) {
                try {
                    const data = JSON.parse(event.data);
                    onMessageCallback(data);
                } catch (error) {
                    console.error("Erreur lors de la parsing du message WebSocket :", error);
                }
            } else {
                console.log("Message reçu :", event.data);
            }
        };

        ws.onclose = () => {
            console.warn("Connexion WebSocket fermée, tentative de reconnexion...");
            setIsConnected(false);
            attemptReconnect();
        };

        ws.onerror = (error) => {
            console.error("Erreur WebSocket :", error);
            if (onErrorCallback) {
                onErrorCallback(error);
            }

            ws.close();
        };
    }, [url, onMessageCallback, onReconnectCallback, onErrorCallback]);

    const attemptReconnect = useCallback(() => {
        if (reconnectTimeoutRef.current) return;
        reconnectAttemptsRef.current += 1;

        const timeout = Math.min(1000 * reconnectAttemptsRef.current, 10000);
        reconnectTimeoutRef.current = setTimeout(() => {
            console.log(`Tentative de reconnexion, essai n°${reconnectAttemptsRef.current}`);
            connect();
        }, timeout);
    }, [connect]);

    useEffect(() => {
        connect();

        return () => {
            if (wsRef.current) {
                wsRef.current.close();
            }
            if (reconnectTimeoutRef.current) {
                clearTimeout(reconnectTimeoutRef.current);
            }
        };
    }, [connect]);

    const sendMessage = useCallback((message: string) => {
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(message);
        } else {
            console.error("Websocket is not opened. Message haven't been sent.");
        }
    }, []);

    return { isConnected, sendMessage };
}