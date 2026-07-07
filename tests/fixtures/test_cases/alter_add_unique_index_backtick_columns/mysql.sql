/*
tables = ['hdl_orders']
columns = []
engine = 'mysql'
*/

ALTER TABLE hdl_orders ADD UNIQUE INDEX `uk_order_id_package_id` (`order_id`, `package_id`);
