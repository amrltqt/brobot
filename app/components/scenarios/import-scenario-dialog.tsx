import { Button } from "@/components/ui/button"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { PlusIcon } from "lucide-react"
import React, { useState, ChangeEvent } from "react"


interface ImportScenarioDialogProps {
    onImport: (slug: string, url: string) => void;
}

export function ImportScenarioDialog({ onImport }: ImportScenarioDialogProps) {

    const [slug, setSlug] = useState<string>("");
    const [url, setUrl] = useState<string>("");

    const handleImport = () => {
        onImport(slug, url);
    };

    return (
        <Dialog>
            <DialogTrigger asChild>
                <Button >
                    <PlusIcon className="ml-2 h-4 w-4" />
                    Import Scenario
                </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-4xl">
                <DialogHeader>
                    <DialogTitle>Import scenario</DialogTitle>
                    <DialogDescription>
                        Provide a github url to import a scenario.
                    </DialogDescription>
                </DialogHeader>
                <form onSubmit={(event) => {
                    event.preventDefault();
                    handleImport();
                }}>
                    <div className="grid gap-4 py-4">
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="slug" className="text-right">
                                Name
                            </Label>
                            <Input
                                id="slug"
                                value={slug}
                                onChange={(event: ChangeEvent<HTMLInputElement>) => setSlug(event.target.value)}
                                className="col-span-3"
                                placeholder="introduction-sql"
                            />
                        </div>
                        <div className="grid grid-cols-4 items-center gap-4">
                            <Label htmlFor="url" className="text-right">
                                URL
                            </Label>
                            <Input
                                id="url"
                                value={url}
                                onChange={(event: ChangeEvent<HTMLInputElement>) => setUrl(event.target.value)}
                                className="col-span-3"
                                placeholder="https://github.com/amrltqt/brobot/blob/master/data/scenarios/introduction-sql.json"
                            />
                        </div>
                    </div>
                    <DialogFooter>
                        <Button type="submit">Import</Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    )
}
