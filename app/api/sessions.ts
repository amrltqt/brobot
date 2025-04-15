import { TrainingSessionWithScenarioAndMessagesDTO } from "../models/session";

interface FetchSessionOptions {
    sessionId: number;
    userId: string;
}

export async function fetchSession(
    options: FetchSessionOptions
): Promise<TrainingSessionWithScenarioAndMessagesDTO> {
    const { sessionId, userId } = options;

    const response = await fetch(`http://localhost:8000/sessions/${sessionId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch conversation with ID ${sessionId}`);
    }
    return response.json();
}

interface FetchMySessionsOptions {
    userId: string;
}

export async function fetchMySessions(options: FetchMySessionsOptions): Promise<TrainingSessionWithScenarioAndMessagesDTO[]> {
    const response = await fetch(`http://localhost:8000/sessions`);
    if (!response.ok) {
        throw new Error(`Failed to fetch conversations`);
    }
    return response.json();
}