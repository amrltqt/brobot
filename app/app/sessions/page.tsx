"use client";

import useSWR from "swr";
import { fetchMySessions, deleteSession } from "@/api/sessions";
import { TrainingSessionDTO } from "@/models/session";
import SessionCard from "@/components/sessions/session-card";
import { Empty } from "@/components/common/empty";
import { Loading } from "@/components/common/loading";
import { ErrorDisplay } from "@/components/common/error-display";

const fetcher = () => fetchMySessions({});


export default function Page() {
    const { data: sessions, mutate, error } = useSWR<TrainingSessionDTO[]>("sessions", fetcher);

    const onDelete = async (id: number) => {
        try {
            await deleteSession({ sessionId: id });
            mutate();
        } catch {
            console.error("Failed to delete session");
        }
    };

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
