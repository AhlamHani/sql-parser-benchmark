/*
tables = ['hdl_orders']
columns = []
engine = 'mysql'
*/

UPDATE hdl_orders SET package_id = '-1' WHERE package_id IS NULL;

ALTER TABLE hdl_orders MODIFY `package_id` varchar(64) NOT NULL DEFAULT '-1' COMMENT '[NOT-PII]';

ALTER TABLE hdl_orders DROP INDEX `order_id`;

ALTER TABLE hdl_orders ADD UNIQUE INDEX `uk_order_id_package_id` (`order_id`, `package_id`);
