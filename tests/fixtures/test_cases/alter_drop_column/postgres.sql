/*
tables = ['rides']
columns = ['activity_id']
expected-parsers = ['sqlglot']
engine = 'postgres'
*/

ALTER TABLE rides DROP COLUMN activity_id;
