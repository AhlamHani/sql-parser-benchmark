/*
tables = ['orders']
columns = []
expected-parsers = ['sql_metadata']
engine = 'mysql'
*/

ALTER TABLE orders ADD INDEX idx_order_id (order_id);
