import { useState, useCallback, useEffect } from "react";
import useSWR, { mutate } from "swr";
import { fetchSession } from "@/api/sessions";
import { useWebSocket } from "./use-websocket";
import type { SessionMessageDTO, TrainingSessionWithScenarioAndMessagesDTO } from "@/models/session";

export function useChatService(userId: string, sessionId: number) {

    const [messages, setMessages] = useState<SessionMessageDTO[]>([]);

    const { data: session, error: restError } = useSWR<TrainingSessionWithScenarioAndMessagesDTO>(
        sessionId.toString(),
        () => fetchSession({ sessionId, userId })
    );

    const [wsStatus, setWsStatus] = useState<"connecting" | "connected" | "reconnecting" | "error">("connecting");
    const [wsError, setWsError] = useState<any>(null);
    const [wsLog, setWsLog] = useState<string | null>();

    const handleWsMessage = useCallback((msg: SessionMessageDTO) => {
        if (msg.id) {
            setMessages((prevMessages) => [...prevMessages, msg]);
        }
    }, []);

    const handleWsReconnect = useCallback(() => {
        console.log("WebSocket reconnecté, rafraîchissement de la session");
        setMessages([]);
        setWsError(null);
        setWsStatus("connected");
        mutate(sessionId.toString(), fetchSession({
            sessionId,
            userId,
        }), false);
    }, [sessionId]);

    const handleWsError = useCallback((error: any) => {
        console.error("Erreur signalée par WS:", error);
        setWsError(error);
        setWsStatus("error");
    }, []);

    const { isConnected, sendMessage } = useWebSocket(
        `http://localhost:8000/ws/${sessionId}`,
        handleWsMessage,
        handleWsReconnect,
        handleWsError
    );

    useEffect(() => {
        if (isConnected) {
            setWsStatus("connected");
        } else {
            if (wsStatus !== "error") {
                setWsStatus("reconnecting");
            }
        }
    }, [isConnected, wsStatus]);

    const sendChatMessage = useCallback((message: string) => {
        sendMessage(message);
    }, [sendMessage]);

    const error = wsError || restError || null;
    const isLoading = !session && !error;

    return {
        messages,
        session,
        isLoading,
        connectionStatus: wsStatus,
        error,
        sendMessage: sendChatMessage,
    };
}