import { TrainingSessionWithScenarioAndMessagesDTO } from "../models/session";

const API_URL = "http://localhost:8000/sessions";

const BASE_HEADERS = {
    "Content-Type": "application/json",
};

// Utility function for API requests
async function apiRequest<T>(
    endpoint: string,
    options: RequestInit
): Promise<T> {
    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
            ...BASE_HEADERS,
            ...options.headers,
        },
    });

    if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
    }

    return response.json();
}

interface FetchSessionOptions {
    sessionId: number;
}

export async function fetchSession(
    { sessionId }: FetchSessionOptions
): Promise<TrainingSessionWithScenarioAndMessagesDTO> {
    return apiRequest<TrainingSessionWithScenarioAndMessagesDTO>(`/${sessionId}`, {
        method: "GET",
    });
}

interface FetchMySessionsOptions { }

export async function fetchMySessions(
    { }: FetchMySessionsOptions
): Promise<TrainingSessionWithScenarioAndMessagesDTO[]> {
    return apiRequest<TrainingSessionWithScenarioAndMessagesDTO[]>(`/`, {
        method: "GET",
    });
}

interface DeleteSessionOptions {
    sessionId: number;
}

export async function deleteSession(
    { sessionId }: DeleteSessionOptions
): Promise<void> {
    await apiRequest<void>(`/${sessionId}`, {
        method: "DELETE",
    });
}