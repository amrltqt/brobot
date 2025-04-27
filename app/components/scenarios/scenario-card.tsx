"use client";

import React from "react";
import {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    CardFooter,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Play, Trash2, BookOpen } from "lucide-react";
import { ScenarioRead } from "@/models/scenario";

interface ScenarioCardProps {
    scenario: ScenarioRead;
    onStart: () => void;
    onDelete: () => void;
}

export function ScenarioCard({
    scenario,
    onStart,
    onDelete,
}: ScenarioCardProps) {
    const { title, description, chapters } = scenario;
    const chaptersCount = chapters?.length ?? 0;

    return (
        <Card className="rounded-md">
            <CardHeader className="flex items-center justify-between pb-2">
                <CardTitle className="text-2xl font-bold tracking-tight">{title}</CardTitle>
                <Badge variant="secondary" className="flex items-center space-x-1">
                    <BookOpen className="h-4 w-4" />
                    <span>{chaptersCount}</span>
                </Badge>
            </CardHeader>

            <CardContent className="text-muted-foreground">
                {description}

            </CardContent>

            <CardFooter className="mt-2 flex flex-row gap-4">
                <Button onClick={onStart}>
                    <Play className="mr-1 h-4 w-4" />
                    Start
                </Button>
                <Button variant="destructive" onClick={onDelete}>
                    <Trash2 className="mr-1 h-4 w-4" />
                    Delete
                </Button>
            </CardFooter>
        </Card>
    );
}