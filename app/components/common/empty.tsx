import React from "react";

interface EmptyProps {
    message?: string;
    action?: React.ReactNode;
}

export function Empty({ message = "No items found", action = null }: EmptyProps) {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen">
            <h1 className="text-4xl font-bold text-muted-foreground">{message}</h1>
            {action && <div className="mt-4">{action}</div>}
        </div>
    );
}