import { useState, useCallback, useEffect } from "react";
import useSWR, { mutate } from "swr";
import { fetchSession } from "@/api/sessions";
import { useWebsocket } from "./use-websocket";
import type {
    SessionMessageDTO,
    TrainingSessionWithScenarioAndMessagesDTO,
} from "@/models/session";
import { upsertAndSortMessages } from "@/utils/messages";

export function useChatService(
    userId: string,
    sessionId: number
) {
    // Local state for chat messages
    const [messages, setMessages] = useState<SessionMessageDTO[]>([]);
    const [typing, setTyping] = useState(false);

    // Fetch session metadata & history
    const { data: session, error: restError } = useSWR<TrainingSessionWithScenarioAndMessagesDTO>(
        sessionId.toString(),
        () => fetchSession({ sessionId })
    );

    // Connection status: connecting | connected | reconnecting
    const [connectionStatus, setConnectionStatus] = useState<
        "connecting" | "connected" | "reconnecting"
    >("connecting");

    // Handler when a message arrives via WebSocket
    const handleWsMessage = useCallback((data: string) => {
        if (!data?.trim()) return;
        try {
            const parsed = JSON.parse(data);

            if (parsed.type === "typing") {
                setTyping(parsed.status === "start");
                return;
            }

            const msg: SessionMessageDTO = parsed;
            if (!msg.id) return;

            setMessages((prev) => upsertAndSortMessages(prev, msg));
        } catch (err) {
            console.error("Invalid WS message format:", err, data);
        }
    }, []);

    // Called on initial open and every reconnect
    const handleWsOpen = useCallback(() => {
        console.info("WebSocket open/reconnected, refreshing session");
        setMessages([]);
        setConnectionStatus("connected");
        // Revalidate REST cache without re-fetching data for React
        mutate(
            sessionId.toString(),
            fetchSession({ sessionId }),
            false
        );
    }, [sessionId, userId]);

    // Initialize resilient WebSocket
    const { send, readyState } = useWebsocket(
        `ws://localhost:8000/sessions/ws/${sessionId}`,
        { onMessage: handleWsMessage }
    );

    // Map readyState to our connectionStatus and handle opens
    useEffect(() => {
        switch (readyState) {
            case "OPEN":
                handleWsOpen();
                break;
            case "CONNECTING":
                setConnectionStatus("connecting");
                break;
            case "CLOSING":
            case "CLOSED":
                setConnectionStatus("reconnecting");
                break;
        }
    }, [readyState, handleWsOpen]);

    // Public send function
    const sendMessage = useCallback(
        (content: string) => {
            const payload = { role: "user", content };
            send(JSON.stringify(payload));
        },
        [send]
    );

    // Aggregate error/loading state
    const error = restError;
    const isLoading = !session && !error;

    return {
        typing,
        messages,
        session,
        isLoading,
        connectionStatus,
        error,
        sendMessage,
    };
}
