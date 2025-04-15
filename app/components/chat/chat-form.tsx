"use client"

import { ChatMessages } from "./chat-messages"
import { ChatInput } from "./chat-input"
import { SessionMessageRead } from "@/models/session"


export interface ChatFormProps {
    messages: SessionMessageRead[] | null,
    sendMessage: (message: string) => void
}

export function ChatForm({ messages, sendMessage }: ChatFormProps) {

    if (!messages) {
        return (
            <div className="flex h-full flex-col gap-4 p-4 border-l">
                <div className="flex items-center justify-center h-full">
                    <span>Veuillez patienter</span>
                </div>
            </div>
        )
    }

    return (
        <main className="ring-none mx-auto flex w-full h-full flex-col items-stretch border-none">
            <ChatMessages messages={messages} />
            <ChatInput sendMessage={sendMessage} />
        </main>
    )
}
