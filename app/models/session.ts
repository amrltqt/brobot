import { ScenarioWithChapterDTO } from "./scenario";



export interface SessionMessageDTO {
    /**
     * DTO for session messages.
     */
    id: number;
    created_at: string; // ISO 8601 string
    content: string;
    role: string; // e.g., "user" or "assistant"
}

export interface TrainingSessionWithScenarioAndMessagesDTO {
    /**
     * DTO for a training session with its associated scenario and messages.
     */
    id: number;
    created_at: string; // ISO 8601 string
    scenario: ScenarioWithChapterDTO;
    messages: SessionMessageDTO[];
}
