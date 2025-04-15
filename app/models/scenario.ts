export interface ScenarioBase {
    title: string;
    description: string;
}

export interface Scenario extends ScenarioBase {
    /**
     * Represents a Scenario entity with its database-specific fields.
     */
    id?: number;
    chapters: Chapter[];
}

export interface ScenarioCreate extends ScenarioBase {
    /**
     * Schema for creating a new Scenario.
     */
}

export interface ScenarioRead extends ScenarioBase {
    /**
     * Schema for reading a Scenario, including its chapters.
     */
    id: number;
    chapters: ChapterRead[];
}

export interface ChapterBase {
    title: string;
    content?: string | null;
    order: number;
    meta?: Record<string, any>;
}

export interface Chapter extends ChapterBase {
    /**
     * Represents a Chapter entity with its database-specific fields.
     */
    id?: number;
    scenario_id: number;
    scenario?: Scenario;
}

export interface ChapterCreate extends ChapterBase {
    /**
     * Schema for creating a new Chapter.
     */
    scenario_id: number;
}

export interface ChapterRead extends ChapterBase {
    /**
     * Schema for reading a Chapter.
     */
    id: number;
    scenario_id: number;
}

export interface ScenarioChapterDTO {
    /**
     * DTO for scenario chapters.
     */
    id: number;
    title: string;
    content?: string | null;
    order: number;
    meta?: Record<string, any>;
}

export interface ScenarioWithChapterDTO {
    /**
     * DTO for a scenario with its associated chapters.
     */
    id: number;
    title: string;
    description: string;
    created_at: string; // ISO 8601 string
    chapters: ScenarioChapterWithoutContentDTO[];
}

export interface ScenarioChapterWithoutContentDTO {
    /**
     * DTO for scenario chapters without content.
     */
    id: number;
    title: string;
    order: number;
}
