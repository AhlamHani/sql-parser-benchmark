/*
tables = ['transaction']
columns = []
expected-parsers = ['sqlglot', 'sql_metadata']
engine = 'mysql'
*/

ALTER TABLE transaction
    ADD COLUMN source_entity_id bigint unsigned DEFAULT NULL AFTER description,
    ADD COLUMN source_entity_type tinyint unsigned DEFAULT NULL AFTER source_entity_id
