import { useEffect, useRef } from "react"
import { UserMessage } from "./user-message"
import { AssistantMessage } from "./assistant-message"

export function ChatMessages({ messages }: { messages: any[] }) {
    const endOfMessagesRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages.length])

    return (
        <div className="flex-grow my-4 flex flex-col gap-4 content-center px-6" >
            {
                messages.map(message =>
                    message.role === "user" ? (
                        <UserMessage key={message.id} content={message.content} />
                    ) : (
                        <AssistantMessage key={message.id} content={message.content} />
                    )
                )
            }
            <div ref={endOfMessagesRef} />
        </div>
    )
}