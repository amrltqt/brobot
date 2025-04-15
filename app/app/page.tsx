"use client";

import useSWR from 'swr';
import { ScenarioRead } from '../models/scenario';
import { ScenarioCard } from '@/components/scenarios/scenario-card';

const fetcher = (url: string): Promise<ScenarioRead[]> => fetch(url).then((res) => {
    if (!res.ok) {
        throw new Error('Failed to fetch scenarios');
    }
    return res.json();
});


export default function Page() {
    const { data: scenarios, error } = useSWR<ScenarioRead[]>('http://localhost:8000/scenarios', fetcher);

    if (!scenarios && !error) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen py-2">
                <h1 className="text-4xl font-bold">Loading scenarios...</h1>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen py-2">
                <h1 className="text-4xl font-bold">Error</h1>
                <p>{error.message}</p>
            </div>
        );
    }

    if (scenarios && scenarios.length === 0) {
        return (
            <div className="flex flex-col items-center justify-center min-h-screen py-2">
                <h1 className="text-4xl font-bold text-muted-foreground">No scenarios available</h1>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            <h2 className="text-lg font-semibold">Scénarios disponibles</h2>
            <div className="grid gap-4">
                {(scenarios ?? []).map((scenario) => (
                    <div key={scenario.id} className="flex items-center justify-between">
                        <ScenarioCard scenario={scenario} />

                    </div>
                ))}
            </div>
        </div>
    );
}