"use client";

import { useRouter } from "next/navigation";
import useSWR from "swr";
import { useCallback } from "react";
import { ScenarioRead } from "@/models/scenario";
import { API_BASE, fetcher } from "@/utils/api";



export function useScenarios() {
    const router = useRouter();
    const { data, error, mutate } = useSWR<ScenarioRead[]>(
        `${API_BASE}/scenarios`,
        fetcher
    );

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
            router.push(`/sessions/${id}`);
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