"use client";

import { ScenarioCard } from "@/components/scenarios/scenario-card";
import { Loading } from "@/components/common/loading";
import { ErrorDisplay } from "@/components/common/error-display";
import { Empty } from "@/components/common/empty";

import { useScenarios } from "@/hooks/use-scenarios";
import { ImportScenarioDialog } from "@/components/scenarios/import-scenario-dialog";

export default function Page() {
    const {
        scenarios,
        isLoading,
        isError,
        deleteScenario,
        startScenario,
        importScenario,
    } = useScenarios();

    if (isLoading) return <Loading message="Loading scenarios..." />;
    if (isError) return <ErrorDisplay message={isError.message} />;
    if (scenarios.length === 0) return <Empty message="No scenarios available" action={
        <ImportScenarioDialog onImport={importScenario} />
    } />;

    return (
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
    );
}