/*
tables = ['customization_group']
columns = []
expected-parsers = ['sql_metadata', 'sqlglot']
engine = 'postgres'
*/

ALTER TABLE customization_group ADD COLUMN IF NOT EXISTS customization_group_template_id BIGINT
