"use client";

import { useRouter } from "next/navigation";
import useSWR from "swr";
import { useCallback, useEffect } from "react";
import { ScenarioRead } from "@/models/scenario";
import { API_BASE, fetcher } from "@/utils/api";
import { TrainingSessionDTO } from "@/models/session";
import { useHeader } from "@/context/header-context";


export function useScenarios() {
    const router = useRouter();
    const { setHeader } = useHeader();
    const { data, error, mutate } = useSWR<ScenarioRead[]>(
        `${API_BASE}/scenarios`,
        fetcher
    );

    useEffect(() => {
        setHeader("Home");
    }, []);

    const deleteScenario = useCallback(
        async (id: number) => {
            // Optimistic update
            const next = data?.filter((s) => s.id !== id) || [];
            mutate(next, { optimisticData: next, rollbackOnError: true });

            const res = await fetch(`${API_BASE}/scenarios/${id}`, {
                method: "DELETE",
            });
            if (!res.ok) {
                throw new Error("Failed to delete");
            }
            // Revalidation
            mutate();
        },
        [data, mutate]
    );

    const startScenario = useCallback(
        async (id: number) => {
            const res = await fetch(`${API_BASE}/sessions/${id}`, {
                method: "POST",
            });

            if (!res.ok) {
                throw new Error("Failed to create session");
            }

            // Revalidation
            const session: TrainingSessionDTO = await res.json();

            router.push(`/sessions/${session.id}`);
        },
        [router]
    );

    return {
        scenarios: data || [],
        isLoading: !error && !data,
        isError: error,
        deleteScenario,
        startScenario,
    };
}