/*
tables = []
columns = []
expected-parsers = ['sqlglot', 'sql_metadata', 'sqlparse']
engine = 'postgres'
*/

DO $$
BEGIN
    CREATE TABLE case_management.case_queue (
        id UUID NOT NULL,
        name VARCHAR(255) NOT NULL
    );
END
$$;
