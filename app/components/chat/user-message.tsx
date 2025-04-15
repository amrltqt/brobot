import { cn } from "@/lib/utils"

interface UserMessageProps {
    content: string
    className?: string
}

export function UserMessage({ content, className }: UserMessageProps) {
    return (
        <div className={cn("self-end max-w-[80%] rounded-xl px-3 py-2 text-sm bg-primary text-primary-foreground", className)}>
            {content}
        </div>
    )
}

