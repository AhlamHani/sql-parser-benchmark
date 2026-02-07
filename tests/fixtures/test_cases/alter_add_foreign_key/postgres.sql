/*
tables = ['merchants', 'zones']
columns = []
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

ALTER TABLE merchants ADD CONSTRAINT fk_zone_id FOREIGN KEY (zone_id) REFERENCES zones (id);
