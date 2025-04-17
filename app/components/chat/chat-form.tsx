"use client"

import { ChatMessages } from "./chat-messages"
import { ChatInput } from "./chat-input"
import { SessionMessageDTO } from "@/models/session"
import { BouncingDots } from "./bouncing-dots"


export interface ChatFormProps {
    connectionStatus: string,
    messages: SessionMessageDTO[] | null,
    sendMessage: (message: string) => void,
    typing?: boolean,
}

export function ChatForm({ messages, sendMessage, typing }: ChatFormProps) {

    if (!messages) {
        return (
            <div className="flex h-full flex-col gap-4 p-4 border-l">
                <div className="flex items-center justify-center h-full">
                    <span>Please wait ...</span>
                </div>
            </div>
        )
    }

    return (
        <main className="ring-none mx-auto flex w-full h-full flex-col items-stretch border-none">
            <ChatMessages messages={messages} />
            {typing && <div className="flex-grow my-4 flex flex-col gap-4 content-center px-6">
                <div className="self-start max-w-[80%] rounded-xl px-3 py-2 text-sm bg-gray-100 text-black prose prose-stone">
                    <BouncingDots />
                </div>
            </div>}

            <ChatInput sendMessage={sendMessage} />
        </main >
    )
}
