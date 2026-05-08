CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.stage_events (
    id              SERIAL PRIMARY KEY,
    area_key        VARCHAR(50) NOT NULL,
    area_name       VARCHAR(100) NOT NULL,
    stage           INTEGER NOT NULL,
    stage_updated   TIMESTAMPTZ NOT NULL,
    next_stages     JSONB,
    retrieved_at    TIMESTAMPTZ NOT NULL,
    CONSTRAINT unique_area_stage_update UNIQUE (area_key, stage_updated)
);