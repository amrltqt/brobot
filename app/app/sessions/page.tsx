"use client";

import useSWR from "swr";
import { fetchMySessions, deleteSession } from "@/api/sessions";
import { TrainingSessionDTO } from "@/models/session";
import SessionCard from "@/components/sessions/session-card";

const fetcher = () => fetchMySessions({});


export default function Page() {
    const { data: sessions, mutate } = useSWR<TrainingSessionDTO[]>("sessions", fetcher);

    const onDelete = async (id: number) => {
        try {
            await deleteSession({ sessionId: id });
            mutate();
        } catch {
            console.error("Erreur suppression");
        }
    };

    if (!sessions) return <div className="flex justify-center py-10">Loading...</div>;
    if (sessions.length === 0) return <div className="flex justify-center py-10">Aucune session</div>;

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
