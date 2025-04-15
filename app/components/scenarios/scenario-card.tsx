import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { BookOpen } from 'lucide-react'
import React from "react"
import { Button } from "../ui/button"
import { ScenarioRead } from "@/models/scenario"
import { redirect } from "next/navigation"



interface ScenarioCardProps {
    scenario: ScenarioRead
}

const deleteScenario = async (id: number) => {
    try {
        const response = await fetch(`http://localhost:8000/scenarios/${id}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error('Failed to delete scenario');
        }
        window.location.reload(); // Refresh the page after deletion
    } catch (error) {
        console.error(error);
        alert('Error while deleting the scenario');
    }
};

const createScenario = async (id: number) => {
    try {
        const response = await fetch(`http://localhost:8000/sessions/${id}`, {
            method: 'POST',
        });
        if (!response.ok) {
            throw new Error('Failed to create scenario');
        }
        redirect(`/sessions/${id}`);
    } catch (error) {
        console.error(error);
        alert('Error while creating the scenario');
    }
}

export function ScenarioCard({ scenario }: ScenarioCardProps) {

    // Truncate the description to 500 characters
    const truncatedDescription =
        scenario.description.length > 500
            ? `${scenario.description.substring(0, 500)}...`
            : scenario.description

    return (
        <Card className="overflow-hidden">
            <CardHeader className="p-4 pb-2">
                <CardTitle className="text-lg">{scenario.title}</CardTitle>
                <div className="flex items-center gap-1 text-xs text-muted-foreground">
                    <BookOpen className="h-3 w-3" />
                    <span>12 chapters</span>
                </div>
            </CardHeader>
            <CardContent className="p-4 pt-0">
                <CardDescription className="text-xs line-clamp-4">
                    {truncatedDescription}
                </CardDescription>
            </CardContent>
            <CardFooter className="p-4 pt-0">
                <Button onClick={() => createScenario(scenario.id)}>
                    Start
                </Button>
                <Button variant="destructive" className="ml-2" size="sm" onClick={() => deleteScenario(scenario.id)}>
                    Supprimer
                </Button>
            </CardFooter>
        </Card>
    )
}
