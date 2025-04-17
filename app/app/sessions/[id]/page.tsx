"use client";

import React from "react";
import { ChatForm } from "@/components/chat/chat-form";
import { useChatService } from "@/hooks/use-chat-service";

interface ChatPageProps {
    params: Promise<{ id: string }>;
}

export default function Page({ params }: ChatPageProps) {
    const { id } = React.use(params)
    const {
        typing,
        messages,
        session,
        isLoading,
        connectionStatus,
        error,
        sendMessage
    } = useChatService("1", parseInt(id, 10));

    const handleSendMessage = (message: string) => {
        sendMessage(message);
    };

    if (error) return <div>Error loading conversation</div>;
    if (!session || isLoading) return <div>Loading...</div>;

    return (
        <div className="flex flex-col h-full py-2">
            <ChatForm connectionStatus={connectionStatus} messages={messages} sendMessage={handleSendMessage} typing={typing} />
        </div>
    );
}
