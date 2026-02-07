/*
tables = ['hdl_orders']
columns = []
expected-parsers = ['sql_metadata']
engine = 'mysql'
*/

ALTER TABLE hdl_orders ADD INDEX idx_order_id (order_id);
