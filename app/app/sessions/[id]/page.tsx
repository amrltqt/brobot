"use client";

import React from "react";
import { ChatForm } from "@/components/chat/chat-form";
import { useChatService } from "@/hooks/use-chat-service";
import { ErrorDisplay } from "@/components/common/error-display";
import { Loading } from "@/components/common/loading";

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

    if (error) return <ErrorDisplay message={error.message} />;
    if (!session || isLoading) return <Loading message="Loading session..." />;

    return (
        <div className="flex flex-col h-full py-2">
            <ChatForm connectionStatus={connectionStatus} messages={messages} sendMessage={handleSendMessage} typing={typing} />
        </div>
    );
}
