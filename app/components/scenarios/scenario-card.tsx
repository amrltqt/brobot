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
        <Card className="w-full">
            <CardHeader className="flex items-center justify-between pb-2">
                <CardTitle className="text-lg">{title}</CardTitle>
                <Badge variant="secondary" className="flex items-center space-x-1">
                    <BookOpen className="h-4 w-4" />
                    <span>{chaptersCount}</span>
                </Badge>
            </CardHeader>

            <CardContent className="p-2">
                <p className="text-sm text-muted-foreground">
                    {description}
                </p>
            </CardContent>

            <CardFooter className="flex justify-end space-x-2 p-2">
                <Button size="sm" onClick={onStart}>
                    <Play className="mr-1 h-4 w-4" />
                    Start
                </Button>
                <Button size="sm" variant="destructive" onClick={onDelete}>
                    <Trash2 className="mr-1 h-4 w-4" />
                    Delete
                </Button>
            </CardFooter>
        </Card>
    );
}