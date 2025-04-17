"use client";

import useSWR from "swr";

import { fetchMySessions, deleteSession } from "@/api/sessions";
import { TrainingSessionWithScenarioAndMessagesDTO } from "@/models/session";
import Link from "next/link";
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";


export default function Page() {

    const { data: sessions, mutate } = useSWR<TrainingSessionWithScenarioAndMessagesDTO[]>(
        "1", () => fetchMySessions({})
    );


    const handleDeleteSession = async (sessionId: number) => {
        try {
            await deleteSession({ sessionId });
        } catch (error) {
            console.error("Failed to delete session:", error);
        }
    };

    return (
        <div className="flex flex-col min-h-screen py-2">
            <h1 className="text-4xl font-bold">Chat</h1>
            <p className="text-lg">Engaged scenarios</p>
            <div className="flex flex-col gap-4">
                {sessions?.map((session) => (
                    <Card key={session.id} className="p-4 border rounded-md">
                        <CardHeader>
                            <h2 className="text-xl font-semibold">{session.scenario.title}</h2>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground">{session.scenario.description}</p>
                            <div className="">
                                <ul className="list-disc list-inside">
                                    {session.scenario.chapters.map((chapter) => (
                                        <li key={chapter.id} className="text-muted-foreground">
                                            {chapter.title}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </CardContent>
                        <CardFooter className="flex justify-between">
                            <div>Started: {session.scenario.created_at}</div>
                            <div>Number of messages: {session.messages.length}</div>

                            <div>
                                <Button variant="destructive" size="sm" onClick={() => handleDeleteSession(session.id)}>
                                    Delete
                                </Button>
                                <Link href={`/sessions/${session.id}`}>
                                    <Button variant="outline" size="sm">
                                        Continue
                                    </Button>
                                </Link>
                            </div>
                        </CardFooter>
                    </Card>
                ))}
                {!sessions && (
                    <div className="flex items-center justify-center h-full">
                        <span>Loading...</span>
                    </div>
                )}
                {sessions?.length === 0 && (
                    <div className="flex items-center justify-center h-full">
                        <span>No sessions found</span>
                    </div>
                )}
            </div>
        </div>
    );
}