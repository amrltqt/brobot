"use client";

import { ScenarioCard } from "@/components/scenarios/scenario-card";
import { Loading } from "@/components/common/loading";
import { ErrorDisplay } from "@/components/common/error";
import { Empty } from "@/components/common/empty";

import { useScenarios } from "@/hooks/use-scenarios";

export default function Page() {
    const {
        scenarios,
        isLoading,
        isError,
        deleteScenario,
        startScenario,
    } = useScenarios();

    if (isLoading) return <Loading message="Loading scenarios..." />;
    if (isError) return <ErrorDisplay message={isError.message} />;
    if (scenarios.length === 0) return <Empty message="No scenarios available" />;

    return (
        <div className="space-y-4">
            <h1 className="text-2xl font-bold">Training hub</h1>
            <p className="text-lg">Start learning today</p>
            <div className="grid gap-4">
                {scenarios.map((scenario) => (
                    <ScenarioCard
                        key={scenario.id}
                        scenario={scenario}
                        onStart={() => startScenario(scenario.id)}
                        onDelete={() => deleteScenario(scenario.id)}
                    />
                ))}
            </div>
        </div>
    );
}