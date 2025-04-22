import { Loader2Icon, MessageSquare, RotateCcwIcon, Trash2 } from "lucide-react";
import { Button } from "../ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "../ui/card";
import { TrainingSessionDTO } from "@/models/session";
import ChapterCompletions from "./chapter-completions";
import { Badge } from "../ui/badge";
import Link from "next/link";

interface SessionCardProps {
    session: TrainingSessionDTO;
    onDelete: (id: number) => void;
}

export default function SessionCard({ session, onDelete }: SessionCardProps) {

    // Need to revamp a bit the chapter 
    const chapters = session.scenario.chapters.map((chapter) => {
        const completion = session.completions.find((c) => c.chapter_id === chapter.id);
        return {
            ...chapter,
            completed: !!completion,
            completed_at: completion ? completion.completed_at : null,
        };
    });

    return <Card key={session.id} className="p-4">
        <CardHeader className="flex items-center justify-between pb-2">
            <CardTitle className="text-lg">{session.scenario.title}</CardTitle>
            <Badge variant="secondary" className="flex items-center space-x-1">
                <MessageSquare className="h-4 w-4" />
                <span>{session.messages.length}</span>
            </Badge>
        </CardHeader>

        <CardContent className="flex flex-col gap-4">
            <p className="text-muted-foreground">{session.scenario.description}</p>
            <ChapterCompletions chapters={chapters} />
        </CardContent>

        <CardFooter className="flex justify-between items-center">
            <span>Started: {new Date(session.scenario.created_at).toLocaleDateString()}</span>

            <div className="space-x-2 flex items-center">
                <Button variant="destructive" onClick={() => onDelete(session.id)}>
                    <Trash2 className="mr-1 h-4 w-4" />
                    Delete
                </Button>
                <Button asChild>
                    <Link href={`/sessions/${session.id}`} passHref>
                        <RotateCcwIcon className="mr-1 h-4 w-4" />
                        Continue
                    </Link>
                </Button>
            </div>
        </CardFooter>
    </Card>
}