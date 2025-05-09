import { TrainingSessionDTO } from "../models/session";
import { API_URL } from "@/utils/api";

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

    if (response.status === 204) {
        return {} as T; // No content
    }

    return response.json();
}

interface FetchSessionOptions {
    sessionId: number;
}

export async function fetchSession(
    { sessionId }: FetchSessionOptions
): Promise<TrainingSessionDTO> {
    return apiRequest<TrainingSessionDTO>(`/sessions/${sessionId}`, {
        method: "GET",
    });
}

interface FetchMySessionsOptions { }

export async function fetchMySessions(
    { }: FetchMySessionsOptions
): Promise<TrainingSessionDTO[]> {
    return apiRequest<TrainingSessionDTO[]>(`/sessions`, {
        method: "GET",
    });
}

interface DeleteSessionOptions {
    sessionId: number;
}

export async function deleteSession(
    { sessionId }: DeleteSessionOptions
): Promise<void> {
    await apiRequest<void>(`/sessions/${sessionId}`, {
        method: "DELETE",
    });
}