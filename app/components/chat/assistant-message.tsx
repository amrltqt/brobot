import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

interface AssistantMessageProps {
    content: string
    className?: string
}

export function AssistantMessage({ content }: AssistantMessageProps) {
    return (
        <div className="self-start max-w-[80%] rounded-xl px-3 py-2 text-sm bg-gray-100 text-black prose prose-stone">
            <Markdown remarkPlugins={[remarkGfm]}>{content}</Markdown>
        </div>
    )
}
