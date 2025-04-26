-- Table: scenario
CREATE TABLE IF NOT EXISTS scenario (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: scenario_chapter
CREATE TABLE IF NOT EXISTS scenario_chapter (
    id INTEGER PRIMARY KEY,
    scenario_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    "order" INTEGER NOT NULL,
    meta JSON,
    FOREIGN KEY (scenario_id) REFERENCES scenario (id)
);

-- Table: training_session
CREATE TABLE IF NOT EXISTS training_session (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,

    scenario_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, scenario_id),
    FOREIGN KEY (scenario_id) REFERENCES scenario (id)
);

-- Table: session_message
CREATE TABLE IF NOT EXISTS session_message (
    id INTEGER PRIMARY KEY,
    session_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES training_session (id)
);

-- Table: chapter_completion
CREATE TABLE IF NOT EXISTS chapter_completion (
    id INTEGER PRIMARY KEY,
    session_id INTEGER NOT NULL,
    chapter_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id)   REFERENCES training_session    (id),
    FOREIGN KEY (chapter_id)   REFERENCES scenario_chapter   (id),
    FOREIGN KEY (message_id)   REFERENCES session_message    (id),
    UNIQUE (session_id, chapter_id)
);