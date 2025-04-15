import { useState } from "react"
import { ArrowUpIcon } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip"
import { TooltipProvider } from "@/components/ui/tooltip"
import { AutoResizeTextarea } from "@/components/autoresize-textarea"

export function ChatInput({ sendMessage }: { sendMessage: (message: string) => void }) {
    const [input, setInput] = useState("")

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault()
        if (!input.trim()) return
        sendMessage(input)
        setInput("")
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            // On peut appeler handleSubmit en simulant un événement de formulaire
            handleSubmit(e as unknown as React.FormEvent<HTMLFormElement>)
        }
    }

    return (
        <form
            onSubmit={handleSubmit}
            className="h-fit border-input bg-background focus-within:ring-ring/10 relative mx-6 mb-6 flex items-center rounded-[16px] border px-3 py-1.5 pr-8 text-sm focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-0"
        >
            <AutoResizeTextarea
                onKeyDown={handleKeyDown}
                onInputChange={setInput}
                value={input}
                placeholder="Entrez un message"
                className="placeholder:text-muted-foreground flex-1 bg-transparent focus:outline-none"
            />
            <TooltipProvider>
                <Tooltip>
                    <TooltipTrigger asChild>
                        <Button
                            type="submit"
                            variant="ghost"
                            size="sm"
                            className="absolute bottom-1 right-1 size-6 rounded-full"
                            disabled={!input.trim()}
                        >
                            <ArrowUpIcon size={16} />
                        </Button>
                    </TooltipTrigger>
                    <TooltipContent sideOffset={12}>Envoyer</TooltipContent>
                </Tooltip>
            </TooltipProvider>
        </form>
    )
}