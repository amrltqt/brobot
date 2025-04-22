"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Scenario } from "@/lib/models"

export interface RightMenuProps {
    scenario: Scenario | null;
    connectionStatus: string;
}

export function RightMenu({ scenario, connectionStatus }: RightMenuProps) {
    if (!scenario) {
        return (
            <div className="flex h-full flex-col gap-4 p-4 border-l">
                <Card>
                    <CardHeader className="pb-2">
                        <CardTitle className="text-lg">Chargement...</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center justify-center h-full">
                            <span>Veuillez patienter</span>
                        </div>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <div className="flex h-full flex-col gap-4 p-4 border-l">
            <Card>
                <CardHeader className="pb-2">
                    <CardTitle className="text-lg">{scenario.title}</CardTitle>
                    <CardDescription>SQL / Introduction</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        <div className="flex items-center gap-2">
                            {scenario.description}
                        </div>
                        <div className="flex items-center justify-center h-full">
                            <span>Statut de la connexion : {connectionStatus}</span>
                        </div>

                    </div>
                </CardContent>
            </Card>
        </div>
    )
}

