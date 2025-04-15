"use client"

import { cn } from "@/lib/utils"
import React, { useRef, useEffect, type TextareaHTMLAttributes } from "react"

interface AutoResizeTextareaProps extends Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, "value" | "onChange"> {
    value: string
    onInputChange: (value: string) => void
}

export function AutoResizeTextarea({ className, value, onInputChange, ...props }: AutoResizeTextareaProps) {
    const textareaRef = useRef<HTMLTextAreaElement>(null)

    const resizeTextarea = () => {
        const textarea = textareaRef.current
        if (textarea) {
            textarea.style.height = "auto"
            textarea.style.height = `${textarea.scrollHeight}px`
        }
    }

    useEffect(() => {
        resizeTextarea()
    }, [value])

    return (
        <textarea
            {...props}
            value={value}
            ref={textareaRef}
            rows={1}
            onChange={(e) => {
                onInputChange(e.target.value)
                resizeTextarea()
            }}
            className={cn("resize-none min-h-4 max-h-80", className)}
        />
    )
}

