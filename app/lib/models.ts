export interface PartDescription {
    content: string;
    create_instructions: string[];
    insert_instructions: string[];
}

export interface Part {
    id: number;
    scenario_id: number;
    order: number;
    title: string;
    description: PartDescription;
}

export interface Scenario {
    id: number;
    title: string;
    description: string;
    parts: Part[];
}


export interface Message {
    id: number;
    role: string;
    content: string;
}

export interface Session {
    id: number;
    started_at: string;
    messages: Message[];
}

