import { deleteSession, fetchMySessions } from "@/api/sessions";
import { useHeader } from "@/context/header-context";
import { TrainingSessionDTO } from "@/models/session";
import { useEffect } from "react";
import useSWR from "swr";


const fetcher = () => fetchMySessions({});


export function useSessions() {
    const { setHeader } = useHeader();
    const { data: sessions, mutate, error } = useSWR<TrainingSessionDTO[]>("sessions", fetcher);

    useEffect(() => {
        setHeader("Sessions");
    }, []);


    const onDelete = async (id: number) => {
        try {
            await deleteSession({ sessionId: id });
            mutate();
        } catch {
            console.error("Failed to delete session");
        }
    };

    return {
        sessions: sessions || [],
        error,
        onDelete,
    }
}