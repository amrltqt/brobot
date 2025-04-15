-- Table: scenario
CREATE TABLE scenario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table: chapter
CREATE TABLE scenario_chapter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scenario_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    "order" INTEGER NOT NULL,
    meta JSON,
    FOREIGN KEY (scenario_id) REFERENCES scenario (id)
);

-- Table: conversation_session
CREATE TABLE training_session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    scenario_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, scenario_id),
    FOREIGN KEY (scenario_id) REFERENCES scenario (id)
);

-- Table: conversation_message
CREATE TABLE session_message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES conversation_session (id)
);