/*
tables = ['transactions']
columns = []
expected-parsers = ['sqlglot', 'sql_metadata']
engine = 'mysql'
*/

ALTER TABLE transactions
    ADD COLUMN entity_id bigint unsigned DEFAULT NULL AFTER description,
    ADD COLUMN entity_type tinyint unsigned DEFAULT NULL AFTER entity_id
