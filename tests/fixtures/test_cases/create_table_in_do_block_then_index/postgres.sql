/*
tables = ['interaction']
columns = ['status']
expected-parsers = []
engine = 'postgres'
*/

DO $$
DECLARE
    migration_name CONSTANT text := 'create-interaction-table.sql';
BEGIN
    IF EXISTS (SELECT 1 FROM public.applied_migrations WHERE name = migration_name) THEN
        RETURN;
    END IF;

    CREATE TABLE case_management.interaction (
        id UUID NOT NULL,
        status VARCHAR(32) NOT NULL,
        PRIMARY KEY (id)
    ) PARTITION BY RANGE (id);

    INSERT INTO public.applied_migrations (name) VALUES (migration_name);
END
$$;

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_interaction_status ON case_management.interaction (status);
