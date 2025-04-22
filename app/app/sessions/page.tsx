"use client";

import SessionCard from "@/components/sessions/session-card";
import { Empty } from "@/components/common/empty";
import { Loading } from "@/components/common/loading";
import { ErrorDisplay } from "@/components/common/error-display";
import { useSessions } from "@/hooks/use-sessions";


export default function Page() {

    const { sessions, error, onDelete } = useSessions();

    if (error) return <ErrorDisplay message="Failed to load sessions" />;
    if (!sessions) return <Loading message="Loading sessions..." />;
    if (sessions.length === 0) return <Empty message="You have no sessions yet." />;

    return (
        <div className="flex flex-col min-h-screen py-4 space-y-4">
            <header>
                <h1 className="text-2xl font-bold">Sessions</h1>
                <p className="text-lg">Engaged scenarios</p>
            </header>

            {sessions.map((session) => <SessionCard key={session.id} session={session} onDelete={onDelete} />)}
        </div>
    );
}
