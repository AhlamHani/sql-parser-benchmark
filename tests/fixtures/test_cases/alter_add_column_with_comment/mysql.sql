/*
tables = ['orders']
columns = []
expected-parsers = ['sql_metadata', 'sqlglot']
engine = 'mysql'
*/

ALTER TABLE orders ADD COLUMN user_id BIGINT UNSIGNED NULL COMMENT '[NOT-PII]';
