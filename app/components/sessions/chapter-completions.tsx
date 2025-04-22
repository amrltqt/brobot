import { CheckCircle2 } from "lucide-react";

export interface ChapterCompletionsProps {
    chapters: {
        id: number;
        completed: boolean;
        title: string;
        completed_at: string | null;
    }[];
}

export default function ChapterCompletions({ chapters }: ChapterCompletionsProps) {
    return (
        <div className="flex flex-col gap-2">
            {chapters.map((chapter, i) => {
                return (
                    <div key={chapter.id} className="flex items-center gap-4">
                        <div className="z-10">
                            {chapter.completed ? (
                                <div className="rounded-full bg-green-500 p-1.5">
                                    <CheckCircle2 className="h-5 w-5 text-primary-foreground" />
                                </div>
                            ) : (
                                <div
                                    className={
                                        "rounded-full border-2 h-8 w-8 flex items-center justify-center border-primary text-primary"
                                    }
                                >
                                    <span className="text-xs font-medium">{i + 1}</span>
                                </div>
                            )}

                        </div>
                        <div>
                            {chapter.title}
                        </div>
                        {chapter.completed_at && (
                            <div className="text-sm text-gray-500">
                                Completed at: {new Date(chapter.completed_at).toLocaleString()}
                            </div>
                        )}
                    </div>
                );
            })}
        </div>
    );
}