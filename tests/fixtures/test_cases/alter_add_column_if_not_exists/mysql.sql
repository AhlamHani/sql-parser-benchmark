/*
tables = ['config_groups']
columns = []
expected-parsers = ['sql_metadata', 'sqlglot']
engine = 'mysql'
*/

ALTER TABLE config_groups ADD COLUMN IF NOT EXISTS config_template_id BIGINT
