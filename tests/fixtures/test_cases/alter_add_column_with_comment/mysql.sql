/*
tables = ['hdl_orders']
columns = []
expected-parsers = ['sql_metadata', 'sqlglot']
engine = 'mysql'
*/

ALTER TABLE hdl_orders ADD COLUMN captain_id BIGINT UNSIGNED NULL COMMENT '[NOT-PII]';
