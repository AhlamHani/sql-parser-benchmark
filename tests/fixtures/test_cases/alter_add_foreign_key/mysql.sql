/*
tables = ['hdl_merchants', 'hdl_zone']
columns = []
expected-parsers = ['sqlglot']
engine = 'mysql'
*/

ALTER TABLE hdl_merchants ADD CONSTRAINT fk_hdl_id FOREIGN KEY (hdl_id) REFERENCES hdl_zone (id);
